SSU Chatbot Documentation
===

Using:
- Docker and Docker Compose
- Python 3.12
- [Poetry](https://python-poetry.org/) for dependency management
- [Dependency Injector](http://python-dependency-injector.ets-labs.org/) for dependency injection
- [LangChain](https://python.langchain.com/v0.2/docs/langchain/)
- [FastAPI](https://fastapi.tiangolo.com/) for:
  - REST API
    - [LangServe](https://python.langchain.com/v0.2/docs/langserve/)
  - Chatbot
    - jQuery
    - Bootstrap

---

Chatbot CLI - build the vector database
```
docker compose exec chatbot bash
poetry run chatbot-cli
```



## Notes on deploying to a server (Rocky Linux 9) for demo
````bash
dnf update
dnf install -y dnf-utils
dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
systemctl start docker
yum install git
# add deployment key to github
git clone git@github.com:ssu-carlsoni/chatbot.git /srv/chatbot
cd /srv/chatbot
vi /srv/chatbot/chatbot/config.yml # add api keys
docker compose build
docker compose up -d
firewall-cmd --zone=public --add-port=8000/tcp --permanent
firewall-cmd --reload
````

```shell
docker compose exec chatbot bash

curl \
-X POST \
-H "Content-Type: application/json" \
-d '{
     "id": "20250220"
    }' \
http://weaviate:8080/v1/backups/filesystem

exit

scp -r ./weaviate/backups/20250220 root@172.235.37.212:/srv/chatbot/weaviate/backups/

ssh root@172.235.37.212
cd /srv/chatbot
docker compose exec chatbot bash

curl http://weaviate:8080/v1/backups/filesystem/20250220/

curl \
-X POST \
-H "Content-Type: application/json" \
-d '{
     "id": "20250220"
    }' \
http://weaviate:8080/v1/backups/filesystem/20250220/restore

curl http://weaviate:8080/v1/backups/filesystem/20250220/restore

# if fails becasue Ssu_chatbot already exists
curl -X DELETE http://weaviate:8080/v1/schema/Ssu_chatbot


```