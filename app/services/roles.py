from app.models import Role, User, UserData
from app import db
from app.services import UserService

user_service = UserService()


def create_admin_role():
    """
    Creates an admin role if it doesn't already exist.

    This function checks if an admin role with the name "admin" already exists in the database.
    If it doesn't exist, a new Role object is created with the name "admin" and description "Administrador",
    and it is saved to the database.
    """
    role = Role.query.filter_by(name="admin").first()
    if role:
        pass
    else:
        role = Role()
        role.name = "admin"
        role.description = "Administrador"
        role.save()


def create_user_role():
    """
    Creates a user role if it doesn't already exist.

    This function checks if a user role with the name "user" already exists in the database.
    If it doesn't exist, a new Role object is created with the name "user" and description "Usuario",
    and it is saved to the database.
    """
    role = Role.query.filter_by(name="user").first()
    if role:
        pass
    else:
        role = Role()
        role.name = "user"
        role.description = "Usuario"
        role.save()


def create_admin_user():
    """
    Creates an admin user if it doesn't already exist.

    This function checks if an admin user with the username "admin" already exists in the database.
    If it doesn't exist, a new UserData object is created with the necessary user data,
    and a new User object is created with the email, username, password, role_id, and the UserData object.
    The User object is then saved to the database using the user_service.
    """
    user = User.query.filter_by(username="admin").first()
    if user:
        pass
    else:
        data = UserData()
        data.firstname = "Administrador"
        data.lastname = "Administrador"
        data.address = "Admin Address"
        data.city = "Admin Adress"
        data.country = "Admin Country"
        data.phone = "123456789"

        user = User(data)
        user.email = "admin@gmail.com"
        user.username = "admin"
        user.password = "admin"
        user.role_id = 1

        user_service.save(user)
