from typing import List
from app.models import Profile
from app.repositories import ProfileRepository

repository = ProfileRepository()


class ProfileService:

    def __init__(self):
        pass

    def save(self, profile: Profile) -> Profile:
        repository.save(profile)
        return profile

    def update(self, profile: Profile, id: int) -> Profile:
        repository.update(profile, id)
        return profile

    def delete(self, profile: Profile) -> None:
        repository.delete(profile)

    def all(self) -> List[Profile]:
        return repository.all()

    def find(self, id: int) -> Profile:
        return repository.find(id)
