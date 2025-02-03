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