from flask_login import current_user
from flask import redirect,url_for
from functools import wraps

def role_required(rol):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args,**kwargs):
            if current_user.rol != rol:
                return redirect(url_for("auth.login"))
            return fn(*args,**kwargs)
        return decorated_view
    return wrapper
