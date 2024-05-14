helm upgrade --install  --namespace comrade-ho-chi-minh user-manager --set image.tag=${{ env.COMMIT_HASH }} ./user-manager 
      helm \
        --namespace comrade-chatgpt-bot \
        upgrade --install \
        telegram-bot \
        --set image.tag=${{ env.COMMIT_HASH }} \
        --wait \
        ./telegram-bot


        helm --namespace comrade-chatgpt-bot upgrade --install user-manager --set image.tag=${{ env.COMMIT_HASH }} --wait ./user-manager

        helm upgrade --install  --namespace comrade-ho-chi-minh user-manager ./user-manager -f ./user-manager/values.yaml

        helm upgrade --install  --namespace comrade-ho-chi-minh user-manager ./user_manager/ -f ./user_manager/values.yaml




        helm upgrade --install  --namespace comrade-ho-chi-minh telegramm-bot ./telegram-bot/ -f ./telegram-bot/values.yaml