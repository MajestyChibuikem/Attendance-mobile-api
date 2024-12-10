from routes.auth import auth_blueprint
from routes.attendance import Attendance_blueprint
from routes.users import user_blueprint

def register_routes(app):
    """
    Registers all blueprints with their respective URL prefixes.
    """
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(Attendance_blueprint, url_prefix='/attendance')
    app.register_blueprint(user_blueprint, url_prefix='/users')
