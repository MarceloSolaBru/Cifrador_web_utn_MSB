from dataclasses import dataclass
from app import db
from app.models.audit_mixin import AuditMixin
from app.models.soft_delete import SoftDeleteMixin


@dataclass(init=False, repr=True, eq=True)
class Profile(SoftDeleteMixin, AuditMixin, db.Model):
    """
    Model class representing a user profile.
    Attributes:
        id (int): The unique identifier of the profile.
        name (str): The name of the profile.
        data (list[UserData]): The list of user data associated with the profile.
    """
    __tablename__ = "profiles"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)

    # Relación Uno a Muchos bidireccional con UserData
    data = db.relationship(
        "UserData", back_populates="profile", foreign_keys="[UserData.profile_id]"
    )