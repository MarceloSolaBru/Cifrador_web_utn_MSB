from typing import List, Type
from app.models import Profile
from app import db


class ProfileRepository:
    """Repository class for managing Profile objects."""

    def save(self, profile: Profile) -> Profile:
        """Save a profile object to the database.

        Args:
            profile (Profile): The profile object to be saved.

        Returns:
            Profile: The saved profile object.
        """
        db.session.add(profile)
        db.session.commit()
        return profile

    def update(self, profile: Profile, id: int) -> Profile:
        """Update a profile object in the database.

        Args:
            profile (Profile): The updated profile object.
            id (int): The ID of the profile object to be updated.

        Returns:
            Profile: The updated profile object.
        """
        entity = self.find(id)
        entity.name = profile.name
        db.session.add(entity)
        db.session.commit()
        return entity

    def delete(self, profile: Profile) -> None:
        """Delete a profile object from the database.

        Args:
            profile (Profile): The profile object to be deleted.
        """
        db.session.delete(profile)
        db.session.commit()

    def all(self) -> List[Profile]:
        """Get all profile objects from the database.

        Returns:
            List[Profile]: A list of all profile objects.
        """
        users = db.session.query(Profile).all()
        return users

    def find(self, id: int) -> Profile:
        """Find a profile object by its ID.

        Args:
            id (int): The ID of the profile object to find.

        Returns:
            Profile: The found profile object, or None if not found.
        """
        if id is None or id == 0:
            return None
        try:
            return db.session.query(Profile).filter(Profile.id == id).one()
        except:
            return None
