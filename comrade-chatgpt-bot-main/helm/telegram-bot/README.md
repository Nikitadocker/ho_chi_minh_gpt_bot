helm install telegramm-bot ./telegram-bot -f values.yaml

helm upgrade --install  --namespace comrade-ho-chi-minh telegramm-bot --set image.tag=f49b716 ./telegram-bot