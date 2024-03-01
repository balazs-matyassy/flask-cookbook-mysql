from persistence.decorators import query, fetchall, fetchone
from persistence.repository import AbstractRepository


class RoleRepository(AbstractRepository):
    @staticmethod
    def get_entity_factory():
        return Role.create

    @classmethod
    @query('''
        SELECT `id`, `name`
        FROM `role`
        ORDER BY `name`;
    ''')
    @fetchall
    def find_all(cls):
        pass

    @classmethod
    @query('''
        SELECT `id`, `name`
        FROM `role`
        WHERE `id` = %s;
    ''')
    @fetchone
    def find_by_id(cls, role_id):
        pass

    @classmethod
    @query('''
        SELECT `id`, `name`
        FROM `role`
        WHERE `name` = %s;
    ''')
    @fetchone
    def find_by_name(cls, name):
        pass

    def save(self, role):
        raise NotImplementedError()

    def delete_by_id(self, role_id):
        raise NotImplementedError()


from persistence.model.role import Role
