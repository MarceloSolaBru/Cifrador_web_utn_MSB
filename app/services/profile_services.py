from typing import List
from app.models import Profile
from app.repositories import ProfileRepository

repository = ProfileRepository()


class ProfileService:
    """
    This class represents a service for managing profiles.
    """

    def __init__(self):
        pass

    def save(self, profile: Profile) -> Profile:
        """
        Saves a profile.

        Args:
            profile (Profile): The profile to be saved.

        Returns:
            Profile: The saved profile.
        """
        repository.save(profile)
        return profile

    def update(self, profile: Profile, id: int) -> Profile:
        """
        Updates a profile.

        Args:
            profile (Profile): The updated profile.
            id (int): The ID of the profile to be updated.

        Returns:
            Profile: The updated profile.
        """
        repository.update(profile, id)
        return profile

    def delete(self, profile: Profile) -> None:
        """
        Deletes a profile.

        Args:
            profile (Profile): The profile to be deleted.
        """
        repository.delete(profile)

    def all(self) -> List[Profile]:
        """
        Retrieves all profiles.

        Returns:
            List[Profile]: A list of all profiles.
        """
        return repository.all()

    def find(self, id: int) -> Profile:
        """
        Finds a profile by ID.

        Args:
            id (int): The ID of the profile to find.

        Returns:
            Profile: The found profile.
        """
        return repository.find(id)
