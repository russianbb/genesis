echo "--> Cleaning Docker"
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker image rm $(docker image ls -aq)

echo "--> Login docker to ECR"
aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin $ECR_DNS

echo "--> Pulling image $TAG"
docker pull $ECR_DNS:$TAG

echo "--> Running Django migrations on Docker."
docker run --env-file .env --rm $ECR_DNS:$TAG python manage.py migrate

echo "--> Running Django collectstatic on Docker."
docker run --env-file .env --rm $ECR_DNS:$TAG python manage.py collectstatic

echo "--> Running Django Server."
docker run --env-file .env $ECR_DNS:$TAG