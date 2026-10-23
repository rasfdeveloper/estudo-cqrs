#!/bin/sh
# Idempotente: pode rodar quantas vezes quiser.
echo "==> Garantindo infraestrutura CQRS no Floci (AWS local)..."

for t in products-write products-read; do
  if aws dynamodb describe-table --table-name "$t" >/dev/null 2>&1; then
    echo "    tabela $t ja existe"
  else
    aws dynamodb create-table \
      --table-name "$t" \
      --attribute-definitions AttributeName=product_id,AttributeType=S \
      --key-schema AttributeName=product_id,KeyType=HASH \
      --billing-mode PAY_PER_REQUEST >/dev/null
    echo "    tabela $t criada"
  fi
done

TOPIC_ARN=$(aws sns create-topic --name product-events --query TopicArn --output text)
QUEUE_URL=$(aws sqs create-queue --queue-name product-events-queue --query QueueUrl --output text)
QUEUE_ARN=$(aws sqs get-queue-attributes --queue-url "$QUEUE_URL" --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)

aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol sqs --notification-endpoint "$QUEUE_ARN" > /dev/null 2>&1 || true

aws sqs set-queue-attributes --queue-url "$QUEUE_URL" --attributes '{
  "Policy": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":\"*\",\"Action\":\"sqs:SendMessage\",\"Resource\":\"'$QUEUE_ARN'\",\"Condition\":{\"ArnEquals\":{\"aws:SourceArn\":\"'$TOPIC_ARN'\"}}}]}"
}'

echo ""
echo "==> Infra pronta:"
echo "    products-write (modelo de escrita)"
echo "    products-read  (modelo de leitura desnormalizado)"
echo "    SNS topic:     $TOPIC_ARN"
echo "    SQS queue:     $QUEUE_URL"
