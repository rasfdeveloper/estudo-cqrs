"""Write Service (lado COMMAND do CQRS).

Recebe comandos ("cadastre produto", "mude o preco", "mude o estoque"),
grava no banco de ESCRITA e publica um evento no SNS.

Na vida real seria uma API HTTP (ex.: POST /produtos). Aqui e um CLI
para ficar facil de demonstrar ao vivo.

Uso:
  python write_service.py criar   --id p1 --nome "Teclado" --preco 199.90 --estoque 40
  python write_service.py preco   --id p1 --preco 149.90
  python write_service.py estoque --id p1 --estoque 35
"""
import argparse, json, os, re, sys, time
import boto3

ENDPOINT = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

ddb = boto3.client("dynamodb", endpoint_url=ENDPOINT, region_name=REGION,
                   aws_access_key_id="test", aws_secret_access_key="test")
sns = boto3.client("sns", endpoint_url=ENDPOINT, region_name=REGION,
                   aws_access_key_id="test", aws_secret_access_key="test")

TOPIC_ARN = sns.create_topic(Name="product-events")["TopicArn"]


def publish(event_type, product_id, data):
    event = {"event_type": event_type, "product_id": product_id,
             "data": data, "ts": time.time()}
    sns.publish(TopicArn=TOPIC_ARN, Message=json.dumps(event))
    print(f"[write] evento publicado no SNS: {event_type} -> {json.dumps(data)}")


def get_current(product_id):
    r = ddb.get_item(TableName="products-write", Key={"product_id": {"S": product_id}})
    return {k: list(v.values())[0] for k, v in r.get("Item", {}).items()}


def save(product_id, fields):
    item = {"product_id": {"S": product_id}}
    for k, v in fields.items():
        if k == "product_id":
            continue
        numeric = isinstance(v, (int, float)) or (isinstance(v, str) and re.fullmatch(r"-?\d+(\.\d+)?", v))
        item[k] = {"N": str(v)} if numeric else {"S": str(v)}
    ddb.put_item(TableName="products-write", Item=item)
    print(f"[write] gravado no products-write: {product_id} -> {fields}")


def cmd_criar(a):
    save(a.id, {"nome": a.nome, "preco": a.preco, "estoque": a.estoque})
    publish("ProductCreated", a.id, {"nome": a.nome, "preco": a.preco, "estoque": a.estoque})


def cmd_preco(a):
    cur = get_current(a.id)
    if not cur:
        sys.exit(f"produto {a.id} nao existe — crie primeiro")
    cur["preco"] = a.preco
    save(a.id, cur)
    publish("PriceUpdated", a.id, {"preco": a.preco})


def cmd_estoque(a):
    cur = get_current(a.id)
    if not cur:
        sys.exit(f"produto {a.id} nao existe — crie primeiro")
    cur["estoque"] = a.estoque
    save(a.id, cur)
    publish("StockUpdated", a.id, {"estoque": a.estoque})


p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="cmd", required=True)
c = sub.add_parser("criar");   c.add_argument("--id", required=True); c.add_argument("--nome", required=True); c.add_argument("--preco", type=float, required=True); c.add_argument("--estoque", type=int, required=True)
c = sub.add_parser("preco");   c.add_argument("--id", required=True); c.add_argument("--preco", type=float, required=True)
c = sub.add_parser("estoque"); c.add_argument("--id", required=True); c.add_argument("--estoque", type=int, required=True)
a = p.parse_args()
{"criar": cmd_criar, "preco": cmd_preco, "estoque": cmd_estoque}[a.cmd](a)
