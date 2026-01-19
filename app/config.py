import os

class Config:
    SECRET_KEY = "dev-secret"

    SQLALCHEMY_DATABASE_URI = "sqlite:///brief.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "tucorreo@gmail.com"
    MAIL_PASSWORD = "password-app-gmail"
    MAIL_DEFAULT_SENDER = "Brief System <tucorreo@gmail.com>"

