
# 🧠 Social API

Uma API RESTful escalável desenvolvida com Django REST Framework, com autenticação via JWT, criação de posts, curtidas, seguidores e cache com Redis.

## 🚀 Tecnologias

- Python 3
- Django + Django REST Framework
- PostgreSQL
- Redis (cache)
- Docker + docker-compose
- JWT (SimpleJWT)
- Postman (documentação e testes)

---

## ⚙️ Setup com Docker

1. Clone o repositório:

```bash
git clone https://github.com/kiograco/mini-twitter.git
cd mini-twitter
```

2. Crie o arquivo `.env` (se necessário):

```env
DEBUG=1
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost 127.0.0.1
POSTGRES_DB=social_db
POSTGRES_USER=social_user
POSTGRES_PASSWORD=supersecret
```

3. Suba os containers com Docker Compose:

```bash
docker-compose up --build
```

A API estará disponível em: [http://localhost:8000](http://localhost:8000)

---

## 🔐 Autenticação

A autenticação usa JWT via `djangorestframework-simplejwt`.

### Endpoints:

- `POST /api/token/`: Obter access e refresh token
- `POST /api/token/refresh/`: Obter novo access token usando refresh

---

## 📦 Postman

Importe os seguintes arquivos no Postman para testar rapidamente a API:

- [📄 Coleção Postman](./social_api_8000.postman_collection.json)
- [🌐 Ambiente Postman](./social_api_localhost_8000_environment.postman_environment.json)

> Após importar, configure o token com a variável `{{token}}` no ambiente.

---

## 🧪 Testes

Execute os testes com:

```bash
docker-compose exec backend python manage.py test
```

---

## 🛠 Funcionalidades

- [x] Autenticação JWT
- [x] CRUD de posts
- [x] Like em posts
- [x] Seguir e listar seguidores
- [x] Paginação nos posts
- [x] Cache do feed com Redis
- [x] Contadores em cache (seguidores, curtidas)
- [x] Documentação no Postman
- [x] Testes com `APITestCase`

---

## 📂 Estrutura do Projeto

```
.
├── docker-compose.yml
├── Dockerfile
├── core/              # App principal
│   ├── views.py         # Lógica da API
│   ├── serializers.py
│   ├── models.py
│   ├── urls.py
│   ├── tests.py
├── social_api/          # Configurações do Django
│   ├── settings.py
│   ├── urls.py
├── social_api_8000.postman_collection.json
├── social_api_localhost_8000_environment.postman_environment.json
```

---

## 📜 Licença

Este projeto está sob a licença MIT.