helm upgrade --install  --namespace comrade-ho-chi-minh user-manager --set image.tag=${{ env.COMMIT_HASH }} ./user-manager 
      helm \
        --namespace comrade-chatgpt-bot \
        upgrade --install \
        telegram-bot \
        --set image.tag=${{ env.COMMIT_HASH }} \
        --wait \
        ./telegram-bot


        helm --namespace comrade-chatgpt-bot upgrade --install user-manager --set image.tag=${{ env.COMMIT_HASH }} --wait ./user-manager