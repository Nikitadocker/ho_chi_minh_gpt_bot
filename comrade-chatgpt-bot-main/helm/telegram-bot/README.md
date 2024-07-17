helm install telegramm-bot ./telegram-bot -f values.yaml

helm upgrade --install  --namespace comrade-ho-chi-minh telegramm-bot --set image.tag=ed366d7 ./telegram-bot