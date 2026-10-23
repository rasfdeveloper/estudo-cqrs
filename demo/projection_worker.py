"""Projection Worker (o "consumidor do Kafka" do video).

Fica escutando a fila SQS. Para cada evento do lado de escrita,
monta/atualiza a visao DESNORMALIZADA no banco de leitura.

E aqui que mora a "consistencia eventual": entre o evento ser
publicado e o worker projetar, o lado de leitura fica alguns
milissegundos (ou segundos) "atrasado" — propositalmente.
"""
import json, os, time
import boto3

ENDPOINT = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

sqs = boto3.client("sqs", endpoint_url=ENDPOINT, region_name=REGION,
                   aws_access_key_id="test", aws_secret_access_key="test")
ddb = boto3.client("dynamodb", endpoint_url=ENDPOINT, region_name=REGION,
                   aws_access_key_id="test", aws_secret_access_key="test")

QUEUE_URL = sqs.get_queue_url(QueueName="product-events-queue")["QueueUrl"]
print(f"[worker] escutando {QUEUE_URL}")


def project(product_id, patch):
    r = ddb.get_item(TableName="products-read", Key={"product_id": {"S": product_id}})
    item = {k: list(v.values())[0] for k, v in r.get("Item", {}).items()}
    item.update(patch)
    item["product_id"] = product_id
    item["projetado_em"] = str(time.time())

    put = {"product_id": {"S": product_id}, "projetado_em": {"S": item["projetado_em"]}}
    for k in ("nome", "categoria"):
        if k in item: put[k] = {"S": str(item[k])}
    for k in ("preco", "estoque"):
        if k in item: put[k] = {"N": str(item[k])}
    ddb.put_item(TableName="products-read", Item=put)
    print(f"[worker] read-model atualizado: {product_id} -> {patch}")


while True:
    resp = sqs.receive_message(QueueUrl=QUEUE_URL, WaitTimeSeconds=10, MaxNumberOfMessages=10)
    for msg in resp.get("Messages", []):
        try:
            body = json.loads(msg["Body"])
            event = json.loads(body["Message"]) if "Message" in body else body
            project(event["product_id"], event["data"])
            sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg["ReceiptHandle"])
        except Exception as e:
            print(f"[worker] erro processando mensagem: {e} — {msg['Body'][:200]}")
