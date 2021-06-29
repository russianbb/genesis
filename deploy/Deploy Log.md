

### Pre-configuracao do EC2
- Instalar docker
- Instalar awscli e fazer login


### Atribuir IAM Role com acesso ao ECR na instancia EC2 algo
- Foi necessário criar uma policie
- Foi necessário criar uma role com a policie atachada


### Travis
- Antes de chamar o script de deploy precisa salvar a tag da image

### Script de Deploy
- Ficará disponível sempre no repositório
- Só consegue executar o `docker pull` devido ao login
- Login:
    - `aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 413370623743.dkr.ecr.sa-east-1.amazonaws.com`
- Faz o pull da image:
    - `docker pull 413370623743.dkr.ecr.sa-east-1.amazonaws.com/genesis:$TRAVIS_BUILD_ID`
- Acessa a EC2 via ssh
    - Travis precisa de uma chave criptografada: [https://oncletom.io/2016/travis-ssh-deploy/]