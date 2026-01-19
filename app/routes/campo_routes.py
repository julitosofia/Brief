from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from .role_required import role_required
from app.extensions import db
from app.models.project import Project
from app.models.user import User
from app.models.brief import BriefResponse, SECCIONES_BRIEF
from services.mail_service import enviar_mail

campo_bp = Blueprint("campo", __name__, url_prefix="/campo")

# Dashboard Campo
@campo_bp.route("/dashboard")
@login_required
@role_required("campo")
def dashboard():
    proyectos = Project.query.filter_by(creado_por_id=current_user.id).all()
    return render_template(
        "campo/dashboard.html",
        proyectos=proyectos
    )

# NUEVO: Borrar Proyectos
@campo_bp.route("/proyectos/borrar", methods=["POST"])
@login_required
@role_required("campo")
def borrar_proyectos():
    # Recibimos la lista de IDs desde los checkboxes del HTML
    proyecto_ids = request.form.getlist('proyecto_ids')
    
    if proyecto_ids:
        # Buscamos los proyectos que pertenecen al usuario actual para seguridad
        proyectos_a_borrar = Project.query.filter(
            Project.id.in_(proyecto_ids),
            Project.creado_por_id == current_user.id
        ).all()
        
        for p in proyectos_a_borrar:
            
            BriefResponse.query.filter_by(project_id=p.id).delete()
            db.session.delete(p)
            
        db.session.commit()
    
    return redirect(url_for("campo.dashboard"))

# =========================
# Editar / Completar Brief
# =========================
@campo_bp.route("/proyecto/<int:project_id>/brief", methods=["GET", "POST"])
@login_required
@role_required("campo")
def editar_brief(project_id):
    proyecto = Project.query.get_or_404(project_id)

    if proyecto.creado_por_id != current_user.id:
        abort(403)

    briefs = BriefResponse.query.filter_by(project_id=project_id).all()

    if request.method == "POST":
        for brief in briefs:
            campo = f"seccion_{brief.id}"
            if campo in request.form:
                brief.respuesta = request.form[campo].strip()
                brief.estado = "pendiente"

        proyecto.estado = "en_revision"
        db.session.commit()

        return redirect(url_for("campo.dashboard"))

    return render_template(
        "campo/editar_brief.html",
        proyecto=proyecto,
        briefs=briefs
    )

# Crear Proyecto

@campo_bp.route("/proyecto/nuevo", methods=["GET", "POST"])
@login_required
@role_required("campo")
def crear_proyecto():
    data_users = User.query.filter_by(rol="data").all()

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        data_ids = request.form.getlist("data_users")

        proyecto = Project(
            nombre=nombre,
            descripcion=descripcion,
            creado_por=current_user,
            estado="borrador"
        )

        for uid in data_ids:
            user = User.query.get(int(uid))
            if user:
                proyecto.data_users.append(user)

        db.session.add(proyecto)
        db.session.commit()

        for seccion in SECCIONES_BRIEF:
            brief = BriefResponse(
                project_id=proyecto.id,
                seccion=seccion,
                estado="pendiente",
                respuesta=""
            )
            db.session.add(brief)

        db.session.commit()

        
        emails_data = [u.email for u in proyecto.data_users]
        if emails_data:
            try:
                enviar_mail(
                    asunto="Nuevo proyecto asignado",
                    destinatarios=emails_data,
                    cuerpo=f"Se te asignó el proyecto: {proyecto.nombre}\n\nIngresá al sistema para revisar el brief."
                )
            except Exception as e:
                
                print(f"ALERTA: El proyecto se creó pero el mail no se envió. Error: {e}")

        return redirect(
            url_for("campo.editar_brief", project_id=proyecto.id)
        )

    return render_template(
        "campo/crear_proyecto.html",
        data_users=data_users
    )


