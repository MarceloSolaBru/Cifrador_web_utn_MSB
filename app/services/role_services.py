from typing import List
from app.models import Role
from app.repositories import RoleRepository

repository = RoleRepository()


class RoleService:
    def __init__(self):
        pass

    def save(self, role: Role) -> Role:
        """
        Save a role in the repository.

        Args:
            role (Role): The role to be saved.

        Returns:
            Role: The saved role.
        """
        repository.save(role)
        return role

    def update(self, role: Role, id: int) -> Role:
        """
        Update a role in the repository.

        Args:
            role (Role): The updated role.
            id (int): The ID of the role to be updated.

        Returns:
            Role: The updated role.
        """
        repository.update(role, id)
        return role

    def delete(self, role: Role) -> None:
        """
        Delete a role from the repository.

        Args:
            role (Role): The role to be deleted.

        Returns:
            None
        """
        repository.delete(role)

    def all(self) -> List[Role]:
        """
        Get all roles from the repository.

        Returns:
            List[Role]: A list of all roles.
        """
        return repository.all()

    def find(self, id: int) -> Role:
        """
        Find a role by ID in the repository.

        Args:
            id (int): The ID of the role to find.

        Returns:
            Role: The found role.
        """
        return repository.find(id)

    def find_by_name(self, name: str) -> Role:
        """
        Find a role by name in the repository.

        Args:
            name (str): The name of the role to find.

        Returns:
            Role: The found role.
        """
        return repository.find_by_name(name=name)
