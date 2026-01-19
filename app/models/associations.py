from app.extensions import db

project_users = db.Table(
    "project_users",
    db.Column(
        "project_id",
        db.Integer,
        db.ForeignKey("projects.id"),
        primary_key=True
    ),
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id"),  # 👈 OJO ACÁ
        primary_key=True
    )
)

