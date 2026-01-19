from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app.extensions import db
from app.models.project import Project
from app.models.brief import BriefResponse
from app.models.commment import Comment
from services.mail_service import enviar_mail
from .role_required import role_required

data_bp = Blueprint("data", __name__, url_prefix="/data")



# Dashboard Data

@data_bp.route("/dashboard")
@login_required
@role_required("data")
def dashboard():
    proyectos = current_user.proyectos_asignados
    return render_template("data/dashboard.html", proyectos=proyectos)



# Revisión de Brief

@data_bp.route("/proyecto/<int:project_id>/revision", methods=["GET", "POST"])
@login_required
@role_required("data")
def revisar_brief(project_id):
    proyecto = Project.query.get_or_404(project_id)
    briefs = BriefResponse.query.filter_by(project_id=project_id).all()

    if request.method == "POST":
        for brief in briefs:
            accion = request.form.get(f"accion_{brief.id}")
            comentario_texto = request.form.get(f"comentario_{brief.id}")

            if accion == "aprobar":
                brief.estado = "aprobado"

            elif accion == "observar" and comentario_texto:
                brief.estado = "observado"

                comentario = Comment(
                    brief_id=brief.id,
                    autor_id=current_user.id,
                    comentario=comentario_texto
                )
                db.session.add(comentario)

        
        # Estado del proyecto
        
        todo_aprobado = all(b.estado == "aprobado" for b in briefs)
        hubo_observaciones = any(b.estado == "observado" for b in briefs)

        if todo_aprobado:
            proyecto.estado = "aprobado"
            
            # PROTECCIÓN DE MAIL PARA APROBACIÓN
            try:
                enviar_mail(
                    asunto="Proyecto aprobado",
                    destinatarios=[proyecto.creado_por.email],
                    cuerpo=f"El proyecto '{proyecto.nombre}' fue aprobado.\n\nYa se puede avanzar sin reuniones 🚀"
                )
            except Exception as e:
                print(f"ALERTA: Proyecto aprobado pero falló el mail: {e}")

        elif hubo_observaciones:
            proyecto.estado = "observado"

            # PROTECCIÓN DE MAIL PARA OBSERVACIONES
            try:
                enviar_mail(
                    asunto="Correcciones necesarias en el brief",
                    destinatarios=[proyecto.creado_por.email],
                    cuerpo=f"El proyecto '{proyecto.nombre}' tiene observaciones.\n\nIngresá al sistema para ver los comentarios."
                )
            except Exception as e:
                print(f"ALERTA: Proyecto observado pero falló el mail: {e}")
        else:
            proyecto.estado = "en_revision"

        # Ahora el commit se ejecutará siempre, haya mail o no
        db.session.commit()
        return redirect(url_for("data.dashboard"))

    return render_template(
        "data/revisar_brief.html",
        proyecto=proyecto,
        briefs=briefs
    )




