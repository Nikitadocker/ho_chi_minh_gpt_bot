helm upgrade --install --namespace ingress-controller nginx-ingress ingress-nginx/ingress-nginx --set controller.publishService.enabled=true

helm upgrade --install  --namespace comrade-ho-chi-minh user-manager --set image.tag=${{ env.COMMIT_HASH }} ./user-manager 


kubectl create secret generic user-manager-auth-secret --from-file=auth --namespace comrade-ho-chi-minh 


um.comrade-ho-chi-minh.com