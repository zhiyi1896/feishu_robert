
from app.repositories.user_repository import UserRepository



class EmployeeService:

    def __init__(self, mysql_repository: UserRepository):

        self.mysql_repository = mysql_repository

    async def get_employee_id_by_name(self, assignee_name):

        employee_id = await self.mysql_repository.get_employee_id_by_name(assignee_name)

        return employee_id

    async def get_current_user_id(self,open_id: str):

        user_id = await self.mysql_repository.get_current_user_id(open_id)

        return user_id

    async def get_employee_by_id(self, creator_id: int):

        name = await self.mysql_repository.get_employee_by_creator_id(creator_id)

        return name


    async def get_subordinate_ids(self,manager_id: int):

        subordinate_ids = await self.mysql_repository.get_subordinate_ids(manager_id)

        return subordinate_ids

    async def get_all_subordinate_ids(self,manager_id: int):

        all_ids = []

        queue = [manager_id]

        while queue:
            current_id = queue.pop(0)
            subordinate_ids = await self.mysql_repository.get_subordinate_ids(current_id)

            for subordinate_id in subordinate_ids:
                if subordinate_id not in all_ids:
                    all_ids.append(subordinate_id)
                    queue.append(subordinate_id)

        return all_ids

    async def get_open_id_by_employee_id(self, employee_id):

        open_id = await self.user_repository.get_open_id_by_employee_id(employee_id)

        return open_id

