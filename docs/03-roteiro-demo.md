# Roteiro da demo ao vivo — CQRS com Floci

> Roteiro pensado para apresentar em ~20–30 min. Cada etapa tem o que fazer,
> o que mostrar e a pergunta para a mentoranda.

## 0. Setup (antes de apresentar, ou junto)

```bash
git clone <este-repo> && cd mentoria-cqrs
docker compose up -d          # sobe floci + init (cria infra) + worker
docker logs -f cqrs-worker    # deixe num terminal visível: "[worker] escutando..."
```

No host (onde vamos rodar os comandos):

```bash
pip install boto3
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1
```

> Sem Python no host? Dá pra fazer tudo via container: `docker exec -it cqrs-worker`
> ou trocar os comandos por `aws --endpoint-url=http://localhost:4566 ...`
> (o roteiro traz os equivalentes CLI no final).

**Mostrar**: `http://localhost:4566/_floci/ui` — o console web com as 2 tabelas
DynamoDB, o tópico SNS e a fila SQS. É a "infra da AWS" local.

## 1. O "antes" — tradicional num banco só

Mostrar `docs/frames/01-arquitetura-tradicional.png`.

> Pergunta: *"se o SELECT de dashboard trava o banco, quem sofre?"* (as escritas).

## 2. Criar um produto (lado COMMAND)

```bash
python demo/write_service.py criar --id p1 --nome "Teclado Mecanico" --preco 199.90 --estoque 40
```

Saída esperada:

```
[write] gravado no products-write: p1 -> {...}
[write] evento publicado no SNS: ProductCreated -> {...}
```

Terminal do worker mostra quase na hora:

```
[worker] read-model atualizado: p1 -> {'nome': 'Teclado Mecanico', ...}
```

**Narrativa**: o comando gravou no banco de escrita e *avisou o mundo* via
evento. Ninguém consultou o banco de escrita para ler.

## 3. Consultar (lado QUERY)

```bash
python demo/read_service.py get --id p1
# p1: Teclado Mecanico | R$ 199.9 | estoque 40
```

**Mostrar**: `products-read` é uma linha só, pronta pra tela — sem JOIN.
O `read_service.py` nem sabe que existe `products-write`.

## 4. Demonstrar a consistência eventual (o momento "uau")

```bash
python demo/write_service.py preco --id p1 --preco 149.90 && python demo/read_service.py get --id p1
```

Se for rápido demais, o preço ainda aparece `199.9` — **isso é a janela de
inconsistência**. Rode a consulta de novo ~1s depois: `149.9`.

> Pergunta: *"e se a tela de admin precisar ver o preço novo na hora?"*
> (discussão: read-your-writes — polling, ler do write model, ou esperar)

## 5. O encanto da fila (opcional, forte pedagogicamente)

```bash
docker stop cqrs-worker                      # "derruba" a projeção
python demo/write_service.py estoque --id p1 --estoque 5
python demo/read_service.py get --id p1      # ainda mostra estoque antigo!
docker start cqrs-worker                     # worker volta
python demo/read_service.py get --id p1      # agora mostra 5 — a fila guardou o evento
```

**Lição**: a fila desacopla. O lado de leitura pode ficar fora do ar sem perder
eventos — é resiliência embutida no padrão (e também o motivo da consistência
ser eventual).

## 6. Fechamento

- Mostrar `docs/frames/07-cqrs-diagrama-completo.png` ao lado do
  `docker compose ps` — cada caixinha do diagrama existe na demo.
- Ler o checklist "quando não usar" em `02-para-experientes.md`.

## Apêndice — equivalente via AWS CLI (sem Python)

```bash
AWS="aws --endpoint-url=http://localhost:4566"

# escrever no write model
$AWS dynamodb put-item --table-name products-write --item \
  '{"product_id":{"S":"p2"},"nome":{"S":"Mouse"},"preco":{"N":"89.9"},"estoque":{"N":"10"}}'

# publicar o evento
$AWS sns publish --topic-arn arn:aws:sns:us-east-1:000000000000:product-events \
  --message '{"event_type":"ProductCreated","product_id":"p2","data":{"nome":"Mouse","preco":89.9,"estoque":10}}'

# ler do read model (depois do worker projetar)
$AWS dynamodb get-item --table-name products-read --key '{"product_id":{"S":"p2"}}'

# espiar a fila crua (antes do worker consumir, se parar o worker)
$AWS sqs receive-message --queue-url http://localhost:4566/000000000000/product-events-queue
```

## Troubleshooting

| Sintoma | Causa | Fix |
|---|---|---|
| `localhost:4566` recusa | floci não subiu | `docker compose ps`, `docker logs cqrs-floci` |
| worker não projeta | init falhou / fila não existe | `docker compose up init` de novo (é idempotente), `docker logs cqrs-init` |
| leitura vazia | consistência eventual ou evento sem `product_id` | esperar ~1s e repetir; conferir `docker logs cqrs-worker` |
| sujeira de testes | estado persistiu | `docker compose down -v && docker compose up -d` |
