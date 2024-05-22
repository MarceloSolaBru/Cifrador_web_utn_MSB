from app.models import Role, User, UserData
from app import db


def create_admin_role():
    role = Role.query.filter_by(name="admin").first()
    if role:
        pass
    else:
        role = Role()
        role.name = "admin"
        role.description = "Administrador"
        role.save()

def create_user_role():
    role = Role.query.filter_by(name="user").first()
    if role:
        pass
    else:
        role = Role()
        role.name = "user"
        role.description = "Usuario"
        role.save()

# def create_admin_user():
#     user = User(username = "admin",password="admin_password", email="admin@example.com")
#     user.role_id = 1
#     user.save()