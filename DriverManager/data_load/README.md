# login_data.json

Este archivo contiene credenciales de prueba y selectores de elementos para páginas de login utilizadas en los tests de automatización.

## Estructura:
- `id`: Texto breve que identifica la página.
- `url`: La URL de la página de inicio de sesión.
- `username_selector`: XPath o selector del campo de nombre de usuario.
- `password_selector`: XPath o selector del campo de contraseña.
- `login_button_selector`: XPath o selector del botón de inicio de sesión.
- `credentials`: Un objeto que contiene:
  - `username`: El nombre de usuario para iniciar sesión.
  - `password`: La contraseña para iniciar sesión.

## Ejemplo:
```json
[
  {
    "id": "EJEMPLO"
    "url": "https://example.com/login",
    "username_selector": "//*[@id='username']",
    "password_selector": "//*[@id='password']",
    "login_button_selector": "//*[@id='submit']",
    "credentials": {
      "username": "admin",
      "password": "password123"
    }
  }
]