# Sistema de Biblioteca Universitaria (Arquitectura SOA + REST con Flask y Docker)

## Descripción
Este proyecto implementa una arquitectura orientada a servicios (SOA) basada en microservicios REST con Flask y PostgreSQL, orquestados mediante Docker Compose. Incluye los servicios:
- user-service
- equipment-service
- loan-service
- gateway-service (API Gateway)
Todos los servicios comparten una base de datos PostgreSQL llamada `poli`.

## Estructura del Proyecto
```
.
├── docker-compose.yml
├── user-service/
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   └── Dockerfile
├── equipment-service/
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   └── Dockerfile
├── loan-service/
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   └── Dockerfile
├── gateway-service/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── README.md
```

## Requisitos Previos
- Docker y Docker Compose instalados
- Git instalado
- Python 3.10+ (para desarrollo local opcional)
- Postman (para pruebas)

## Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone git@github.com:julianrugeles/library-repository.git
cd library-repository
```

### 2. Construir e iniciar los servicios
```bash
docker-compose up --build
```
Esto levantará todos los contenedores: PostgreSQL, los tres microservicios y el gateway.

### 3. Acceso a los servicios
- **User Service** → http://localhost:13000/users
- **Equipment Service** → http://localhost:13002/equipment
- **Loan Service** → http://localhost:13003/loans
- **Gateway Service** → http://localhost:13005/

### 4. Variables de entorno (Docker Compose)
Cada servicio se conecta a la base de datos compartida usando:
```
DATABASE_URL=postgresql://userdb:secret123@postgres:5432/poli
```

### 5. Endpoints principales

#### User Service
- `GET /users` → Lista todos los usuarios
- `POST /users` → Crea un usuario
- `GET /users/{id}` → Obtiene un usuario
- `PUT /users/{id}` → Actualiza usuario
- `DELETE /users/{id}` → Elimina usuario

#### Equipment Service
- `GET /equipment`
- `POST /equipment`
- `GET /equipment/{id}`
- `PUT /equipment/{id}`
- `DELETE /equipment/{id}`

#### Loan Service
- `GET /loans`
- `POST /loans` → Crea un préstamo (requiere IDs válidos de usuario y equipo)
- `PUT /loans/{id}/return` → Marca préstamo como devuelto

#### Gateway Service
- `/api/users/*` → Redirige a user-service
- `/api/equipment/*` → Redirige a equipment-service
- `/api/loans/*` → Redirige a loan-service

### 6. Base de datos
El contenedor `postgres` crea automáticamente la base `poli` con el usuario `userdb` y contraseña `secret123`.

Para acceder manualmente:
```bash
docker exec -it postgres_users psql -U userdb -d poli
```

### 7. Pruebas en Postman
Importa el archivo `library-collection.json` incluido para probar los endpoints de todos los servicios.

### 8. Detener los contenedores
```bash
docker-compose down
```

## Créditos
Proyecto desarrollado como ejercicio académico para la implementación de una arquitectura SOA basada en microservicios Flask.
