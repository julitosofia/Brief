from app.extensions import db

class BriefResponse(db.Model):
    __tablename__ = "brief_responses"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    seccion = db.Column(db.String(50), nullable=False)

    respuesta = db.Column(db.Text, nullable=True)
    estado = db.Column(db.String(20), default="pendiente")

    #feedback de datos
    revision_estado = db.Column(db.String(20), default="sin_revisar")
    revision_comentario = db.Column(db.Text, nullable=True)

    ultima_actualizacion = db.Column(
        db.DateTime,
        onupdate=db.func.now()
    )

    project = db.relationship("Project", backref="briefs")

    def __repr__(self):
        return f"<Brief {self.seccion} - {self.estado}>"

SECCIONES_BRIEF = [
    "Número del proyecto",
    "Cliente",
    "Ejecutivo/s de cuentas a cargo del proyecto",
    "Descripción breve del proyecto",
    "¿A quién va dirigido?",
    "Plazos de entrega – Equipo IT",
    "Plazos de entrega – Equipo Data",
    "Plazos de entrega – Equipo de Diseño",
    "Entrega al cliente",
    "Detalles a tener en cuenta (Data / IT)"
]

