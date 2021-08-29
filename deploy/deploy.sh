echo $(date ++%x-%r)  "#### Stasting deploy.sh" >> mylog.txt

echo $(date ++%x-%r)  "---> Cleaning Docker" >> mylog.txt
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker image rm $(docker image ls -aq)

echo $(date ++%x-%r)  "---> Login docker to ECR" >> mylog.txt
aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin $ECR_DNS

echo $(date ++%x-%r)  "---> Pulling image" >> mylog.txt
docker pull $ECR_DNS:latest

echo $(date ++%x-%r)  "---> Running Django migrations on Docker." >> mylog.txt
docker run --env-file .env --rm $ECR_DNS:latest python manage.py migrate --noinput

echo $(date ++%x-%r)  "---> Running Django collectstatic on Docker." >> mylog.txt
docker run --env-file .env --rm $ECR_DNS:latest python manage.py collectstatic --noinput

echo $(date ++%x-%r)  "---> Running Django Server." >> mylog.txt
docker run --env-file .env -p 80:8080 -d -name genesis_web $ECR_DNS:latest

echo $(date ++%x-%r)  "---> Running Celery Worker." >> mylog.txt
docker run --env-file .env -d --name genesis_worker $ECR_DNS:latest celery -A celery_app worker -l info

echo $(date ++%x-%r)  "#### Finish deploy.sh" >> mylog.txt
