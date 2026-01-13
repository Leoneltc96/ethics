# Complaints AI System

Este proyecto es un sistema de gestión de denuncias (Complaints) potenciado por Inteligencia Artificial (Gemini) para procesar y estructurar la información de las denuncias recibidas.

## Características

- **API RESTful** construida con Django y Django Rest Framework.
- **Autenticación JWT** para proteger los endpoints.
- **Integración con Google Gemini** para analizar y estructurar denuncias en texto plano a formato JSON.
- **Dockerizado** para fácil despliegue y desarrollo.
- **Base de datos PostgreSQL**.

## Requisitos Previos

- Docker y Docker Compose instalados.
- Una API Key de Google Gemini.

## Instalación y Configuración

1. **Clonar el repositorio:**

   ```bash
   git clone <url-del-repositorio>
   cd complaints
   ```

2. **Configurar variables de entorno:**

   Crea un archivo `.env` en la raíz del proyecto basándote en el siguiente ejemplo:

   ```env
   # .env
   GEMINI_API_KEY=tu_api_key_de_gemini_aqui
   POSTGRES_DB=complaints
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   ```

3. **Levantar los servicios con Docker:**

   ```bash
   docker-compose up -d --build
   ```

   Esto iniciará la base de datos PostgreSQL y el servidor web Django en `http://localhost:8000`.

4. **Aplicar migraciones (primera vez):**

   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Crear un superusuario (para acceder al admin y obtener tokens):**

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Uso de la API

### Autenticación

El sistema usa JWT. Primero debes obtener un token.

- **Login (Obtener Token):**
  - **URL:** `/auth/login/`
  - **Método:** `POST`
  - **Body:**
    ```json
    {
      "username": "tu_usuario",
      "password": "tu_password"
    }
    ```
  - **Respuesta:** Recibirás `access` y `refresh` tokens.

**Nota:** Para todas las peticiones siguientes, debes incluir el header `Authorization`:
```
Authorization: Bearer <tu_token_access>
```

### Endpoints Principales

#### 1. Procesar Denuncia (Parseo con IA)
Envía una denuncia en texto plano y recibe un JSON estructurado.

- **URL:** `/save_complaint/`
- **Método:** `POST`
- **Body:**
  ```json
  {
    "complaint": "El gerente de ventas está robando material del almacén los fines de semana..."
  }
  ```
- **Respuesta:** JSON estructurado con los detalles de la denuncia (implicados, fechas, tipo de incidente, etc.).

#### 3. Generar Denuncia de Prueba
Genera un ejemplo de denuncia aleatoria.

- **URL:** `/get_complaint/`
- **Método:** `GET`

## Estructura del Proyecto

- `complaints/`: Aplicación principal con la lógica de negocio.
  - `views.py`: Controladores de la API.
  - `services.py`: Lógica de integración con Gemini AI.
  - `urls.py`: Rutas de la aplicación.
- `config/`: Configuración global de Django.
- `Users/`: Gestión de usuarios y autenticación.
- `docker-compose.yml`: Orquestación de contenedores.
