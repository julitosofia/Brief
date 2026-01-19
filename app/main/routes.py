from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.project import Project
from app.extensions import db
from app.models.brief import BriefResponse, SECCIONES_BRIEF

main_bp = Blueprint("main", __name__)

@main_bp.route("/projects/<int:project_id>/brief", methods=["GET", "POST"])
@login_required
def project_brief(project_id):
    proyecto = Project.query.get_or_404(project_id)

    # Crear briefs solo la primera vez
    if request.method == "GET" and not proyecto.briefs:
        for seccion in SECCIONES_BRIEF:
            db.session.add(
                BriefResponse(
                    project_id=proyecto.id,
                    seccion=seccion,
                    estado="pendiente"
                )
            )
        db.session.commit()

    # Guardar respuestas
    if request.method == "POST":
        for brief in proyecto.briefs:
            campo = f"brief_{brief.id}"
            if campo in request.form:
                brief.respuesta = request.form[campo].strip()
                brief.estado = "pendiente"

        proyecto.recalcular_estado()
        db.session.commit()

        return redirect(
            url_for("main.project_brief", project_id=project_id)
        )

    return render_template(
        "projects/brief.html",
        proyecto=proyecto,
        rol=current_user.rol
    )
