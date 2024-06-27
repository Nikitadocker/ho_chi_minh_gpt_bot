helm install telegramm-bot ./telegram-bot -f values.yaml

helm upgrade --install  --namespace comrade-ho-chi-minh telegramm-bot --set image.tag=eaba9e7 ./telegram-bot