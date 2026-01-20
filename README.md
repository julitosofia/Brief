Sistema de Gestión de Briefs de Proyectos

Aplicación web desarrollada en Flask para gestionar el flujo completo de briefs entre el equipo de Campo y el equipo de Data: creación de proyectos, carga de información, revisión por secciones, observaciones, aprobaciones y notificaciones por email.

🚀 Funcionalidades principales
👤 Autenticación y roles

Login de usuarios

Roles soportados:

campo

data

Redirección automática según rol

📁 Gestión de proyectos (Campo)

Crear proyectos

Asignar usuarios del equipo Data

Completar brief estructurado por secciones

Enviar brief a revisión

Ver observaciones y corregir

🧠 Sistema de brief estructurado

Secciones configurables desde backend

Campos de texto y fechas

Estados por sección:

pendiente

observado

aprobado

🔍 Revisión de brief (Data)

Ver proyectos asignados

Revisar cada sección

Aprobar u observar con comentarios

Cambios de estado automáticos del proyecto

📩 Notificaciones por email

Aviso al aprobar proyecto

Aviso al detectar observaciones

Base de datos:
flask db init
flask db migrate
flask db upgrade

Crear usuarios de prueba:
flask shell
from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash

campo = User(
    email="campo@test.com",
    password=generate_password_hash("123456"),
    rol="campo"
)

data = User(
    email="data@test.com",
    password=generate_password_hash("123456"),
    rol="data"
)

db.session.add_all([campo, data])
db.session.commit()

como correr el proyecto:
flask run
http://127.0.0.1:5000/login

Estados del proyecto
Estado	Descripción
pendiente	Brief incompleto
en_revision	Enviado a Data
observado	Tiene comentarios
aprobado	Listo para ejecución
Flujo completo del sistema

Campo crea proyecto

Asigna usuarios Data

Completa brief

Envía a revisión

Data revisa secciones

Aprueba u observa

Sistema notifica por mail

Campo corrige si es necesario

Tecnologías usadas

Python 3.11+

Flask

Flask-Login

Flask-SQLAlchemy

Flask-Mail

Jinja2

SQLite / PostgreSQL

Próximas mejoras

Exportar brief a PDF

Historial de versiones

Notificaciones en tiempo real

Panel de métricas

Control de permisos avanzado

API REST

Autor

Desarrollado por Julian Sofia
