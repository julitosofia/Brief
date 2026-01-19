from app.extensions import db

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    brief_id = db.Column(db.Integer, db.ForeignKey("brief_responses.id"))
    autor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comentario = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, server_default=db.func.now())

    brief = db.relationship("BriefResponse", backref="comentarios")
