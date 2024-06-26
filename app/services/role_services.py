from typing import List
from app.models import Role
from app.repositories import RoleRepository

repository = RoleRepository()


class RoleService:
    def __init__(self):
        pass

    def save(self, role: Role) -> Role:
        repository.save(role)
        return role

    def update(self, role: Role, id: int) -> Role:
        repository.update(role, id)
        return role

    def delete(self, role: Role) -> None:
        repository.delete(role)

    def all(self) -> List[Role]:
        return repository.all()

    def find(self, id: int) -> Role:
        return repository.find(id)

    def find_by_name(self, name: str) -> Role:
        return repository.find_by_name(name=name)
