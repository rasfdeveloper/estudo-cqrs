# Estudo CQRS — Material de Estudo

Material de estudo sobre **CQRS (Command Query Responsibility Segregation)**,
baseado no vídeo [CQRS: O PADRÃO ARQUITETURAL QUE TODO PROGRAMADOR PRECISA CONHECER!](https://www.youtube.com/watch?v=8Z8JAtEEan0)
do Renato Augusto (YouTube), com uma **simulação prática local** usando
[Floci](https://github.com/floci-io/floci) (emulador AWS local, fork livre do LocalStack).

## O que tem aqui

| Caminho | Conteúdo |
|---|---|
| `docs/01-para-leigos.md` | Explicação do CQRS para quem nunca viu o padrão (analogias + figuras do vídeo) |
| `docs/02-para-experientes.md` | Explicação para quem já manja de arquitetura (trade-offs, CDC, Event Sourcing) |
| `docs/03-roteiro-demo.md` | **Roteiro passo a passo** para rodar a demo ao vivo |
| `docs/transcricao.md` | Transcrição completa do vídeo (auto-legendas do YouTube) |
| `docs/frames/` | Capturas dos diagramas de arquitetura do vídeo, em ordem |
| `docker-compose.yml` | Floci + init (cria tabelas/filas) + worker de projeção |
| `demo/` | `write_service.py` (comandos), `projection_worker.py` (SQS→read model), `read_service.py` (queries) |
| `scripts/init.sh` | Cria a infra: 2 tabelas DynamoDB + tópico SNS + fila SQS |

## Arquitetura simulada

```
                 ┌─────────────────┐
   comando ────▶ │  write_service  │────▶ products-write (DynamoDB)
  (criar/preco/  └────────┬────────┘         modelo de ESCRITA
   estoque)               │ publica evento
                          ▼
                     SNS product-events
                          │
                          ▼
                     SQS product-events-queue
                          │
                          ▼
                 ┌─────────────────┐
                 │projection_worker│────▶ products-read (DynamoDB)
                 └─────────────────┘         modelo de LEITURA desnormalizado
                          ▲
   consulta ───▶  read_service
```

O papel do Kafka/Debezium do vídeo é feito aqui por **SNS + SQS**; os bancos
são **DynamoDB** (duas tabelas: uma normalizada para escrita, uma desnormalizada
para leitura). Tudo roda 100% local, sem conta AWS.

## Quick start (5 min)

Pré-requisito: **Docker Desktop** rodando + Python 3 com `pip install boto3`
(ou use o worker em container e rode só os comandos via `amazon/aws-cli`).

```bash
docker compose up -d          # sobe floci + cria infra + worker de projeção
pip install boto3             # para rodar os CLIs do demo/ no host

export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1

# COMANDO (lado de escrita)
python demo/write_service.py criar --id p1 --nome "Teclado" --preco 199.90 --estoque 40

# CONSULTA (lado de leitura — pode demorar ~1s p/ projetar = consistência eventual)
python demo/read_service.py get --id p1

# mude o preço e veja o read-model atualizar sozinho
python demo/write_service.py preco --id p1 --preco 149.90
python demo/read_service.py get --id p1
```

Acompanhe o worker projetando em tempo real:

```bash
docker logs -f cqrs-worker
```

Para resetar tudo: `docker compose down -v` (o init é idempotente, pode subir de novo).

## Console web do Floci

`http://localhost:4566/_floci/ui` — inspeciona tabelas, filas e tópicos no navegador.

## Roteiro sugerido para o estudo

1. `docs/01-para-leigos.md` → entender o problema (por que um banco só não basta)
2. Rodar a demo (`docs/03-roteiro-demo.md`) → ver a segregação acontecendo
3. `docs/02-para-experientes.md` → trade-offs, quando usar e quando NÃO usar
4. Reassistir trechos do vídeo com a transcrição ao lado (`docs/transcricao.md`)
