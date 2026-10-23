"""Read Service (lado QUERY do CQRS).

So le do banco de LEITURA — modelo desnormalizado, uma unica tabela,
sem JOIN nenhum. Repare que aqui nao existe insert/update/delete:
o lado de leitura e literalmente "select simples".

Uso:
  python read_service.py get  --id p1
  python read_service.py list
"""
import argparse, os
import boto3

ENDPOINT = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

ddb = boto3.client("dynamodb", endpoint_url=ENDPOINT, region_name=REGION,
                   aws_access_key_id="test", aws_secret_access_key="test")


def show(item):
    if not item:
        print("  (vazio — o worker ainda nao projetou? confira 'consistencia eventual')")
        return
    flat = {k: list(v.values())[0] for k, v in item.items()}
    print(f"  {flat.get('product_id')}: {flat.get('nome','?')} | R$ {flat.get('preco','?')} | estoque {flat.get('estoque','?')}")


p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="cmd", required=True)
g = sub.add_parser("get");  g.add_argument("--id", required=True)
sub.add_parser("list")
a = p.parse_args()

if a.cmd == "get":
    show(ddb.get_item(TableName="products-read", Key={"product_id": {"S": a.id}}).get("Item"))
else:
    for it in ddb.scan(TableName="products-read").get("Items", []):
        show(it)
