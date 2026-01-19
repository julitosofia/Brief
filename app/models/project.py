from app.extensions import db
from app.models.associations import project_users

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)

    creado_por_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    creado_por = db.relationship("User", backref="proyectos_creados")

    estado = db.Column(
        db.String(30),
        default="pendiente_campo" 
    )

    fecha_creacion = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # usuarios de datos asignados
    data_users = db.relationship(
        "User",
        secondary=project_users,
        backref="proyectos_asignados"
    )

    #MÉTODO DEL MODELO
    def recalcular_estado(self):
        briefs = self.briefs

        if any(b.respuesta in (None, "") for b in briefs):
            self.estado = "pendiente_campo"
            return

        if any(b.revision_estado == "observado" for b in briefs):
            self.estado = "en_revision"
            return

        if all(b.revision_estado == "aprobado" for b in briefs):
            self.estado = "aprobado"
            return

        self.estado = "en_revision"

    def __repr__(self):
        return f"<Project {self.nombre} ({self.estado})>"
