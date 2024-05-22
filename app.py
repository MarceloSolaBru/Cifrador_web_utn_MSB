from app import create_app, db
from flask import Flask
from app.routes.index import index
from app.models import Text, TextHistory, User, Role, UserData
from app.auth.routes import auth as auth_blueprint
from app.routes import index as index_blueprint
from app.resources import home as home_blueprint
from app.services import roles
import os

app = create_app()
app.secret_key = os.environ.get("SECRET_KEY")
app.register_blueprint(auth_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(home_blueprint, url_prefix="/api/v1")  

with app.app_context():
    # Create tables
    db.create_all()
    roles.create_admin_role()
    roles.create_user_role()
    roles.create_admin_user()
# https://flask.palletsprojects.com/en/3.0.x/appcontext/
app.app_context().push()

if __name__ == "__main__":
    """
    Server Startup
    Ref: https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask.run
    Ref: Book Flask Web Development Page 9
    """
    app.run(host="0.0.0.0", port=5000)
