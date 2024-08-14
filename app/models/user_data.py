from dataclasses import dataclass
from app import db
from app.models.audit_mixin import AuditMixin
from app.models.soft_delete import SoftDeleteMixin

@dataclass(init=False, repr=True, eq=True)
class UserData(db.Model, AuditMixin, SoftDeleteMixin):
    """
    Represents user data.
    Attributes:
        id (int): The unique identifier for the user data.
        firstname (str): The first name of the user.
        lastname (str): The last name of the user.
        phone (str): The phone number of the user.
        address (str): The address of the user.
        city (str): The city of the user.
        country (str): The country of the user.
        user_id (int): The foreign key to establish the relationship with the 'users' table.
        user (User): The relationship with the 'User' table, established through the 'user_id' column.
        profile_id (int): The foreign key to establish the many-to-one bidirectional relationship with the 'Profile' table.
        profile (Profile): The relationship with the 'Profile' table, established through the 'profile_id' column.
    """
    __tablename__ = "users_data"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname: str = db.Column(db.String(80), nullable=False)
    lastname: str = db.Column(db.String(80), nullable=False)
    phone: str = db.Column(db.String(120), nullable=False)
    address: str = db.Column(db.String(120), nullable=False)
    city: str = db.Column(db.String(120), nullable=False)
    country: str = db.Column(db.String(120), nullable=False)

    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
    user = db.relationship(
        "User", back_populates="data", foreign_keys=[user_id], uselist=False
    )
    profile_id = db.Column("profile_id", db.Integer, db.ForeignKey("profiles.id"))
    profile = db.relationship(
        "Profile", back_populates="data", foreign_keys=[profile_id]
    )
