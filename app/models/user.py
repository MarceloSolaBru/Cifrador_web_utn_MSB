from dataclasses import dataclass
from .user_data import UserData
from app import db
from app.models.relations import users_roles
from app.models.audit_mixin import AuditMixin
from app.models.soft_delete import SoftDeleteMixin


@dataclass(init=False, repr=True, eq=True)
class User(SoftDeleteMixin, AuditMixin, db.Model):
    """
    User class represents a user in the application.
    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        password (str): The password of the user.
        email (str): The email address of the user.
        role_id (int): The foreign key referencing the role of the user.
    Relationships:
        roles (list): A list of Role objects representing the roles assigned to the user.
        users_rs (list): A list of Text objects associated with the user.
        data (UserData): The UserData object associated with the user.
    Methods:
        __init__(user_data: UserData): Initializes a new User object with the given UserData.
        add_role(role): Adds a role to the user's list of roles.
        remove_role(role): Removes a role from the user's list of roles.
    """
    __tablename__ = "users"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    password: str = db.Column("password", db.String(255), nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    role_id: int = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)

    roles = db.relationship("Role", secondary=users_roles, back_populates="users")
    users_rs = db.relationship("Text", backref="user", lazy=True)
    data = db.relationship(
        "UserData",
        uselist=False,
        back_populates="user",
        foreign_keys="[UserData.user_id]",
    )

    def __init__(self, user_data: UserData):
        """
        Initializes a User object.

        Args:
            user_data (UserData): The user data object containing information about the user.

        Returns:
            None
        """
        self.data = user_data

    def add_role(self, role):
        """
        Adds a role to the user.

        Parameters:
            role (str): The role to be added.

        Returns:
            None
        """
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role):
        """
        Removes a role from the user's roles list.

        Parameters:
        - role (str): The role to be removed.

        Returns:
        None
        """
        if role in self.roles:
            self.roles.remove(role)
