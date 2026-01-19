from flask_mail import Message
from app.extensions import mail

def enviar_mail(asunto, destinatarios, cuerpo):
    if not destinatarios:
        return

    msg = Message(
        subject=asunto,
        recipients=destinatarios,
        body=cuerpo
    )
    mail.send(msg)
