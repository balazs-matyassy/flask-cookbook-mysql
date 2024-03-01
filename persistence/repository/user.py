from persistence.decorators import (query, fetchall, fetchone, update_authoring,
                                    insert_statement, update_statement, statement)
from persistence.repository import AbstractRepository


class UserRepository(AbstractRepository):
    @staticmethod
    def get_entity_factory():
        return User.create

    @staticmethod
    def get_join_factory(join_key):
        return Role.create if join_key == 'role' else None

    @classmethod
    @query('''
        SELECT `user`.`id`, `user`.`username`, `user`.`password` AS 'digest', `user`.`role_id`
            , `user`.`created_at`, `user`.`created_by`, `user`.`modified_at`, `user`.`modified_by`
            , `role`.name AS 'role_name'
        FROM `user`
        INNER JOIN `role` ON `role`.`id` = `user`.`role_id`
        ORDER BY `role`.`name`, `user`.`username`;
    ''')
    @fetchall('role')
    def find_all(cls):
        pass

    @classmethod
    @query('''
        SELECT `user`.`id`, `user`.`username`, `user`.`password` AS 'digest', `user`.`role_id`
            , `user`.`created_at`, `user`.`created_by`, `user`.`modified_at`, `user`.`modified_by`
            , `role`.name AS 'role_name'
        FROM `user`
        INNER JOIN `role` ON `role`.`id` = `user`.`role_id`
        WHERE `user`.`id` = %s;
    ''')
    @fetchone('role')
    def find_by_id(cls, user_id):
        pass

    @classmethod
    @query('''
        SELECT `id`, `username`, `password` AS 'digest', `role_id`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `user`
        WHERE `role_id` = %s
        ORDER BY `username`;
    ''')
    @fetchall
    def find_all_by_role_id(cls, role_id):
        pass

    @classmethod
    @query('''
        SELECT `user`.`id`, `user`.`username`, `user`.`password` AS 'digest', `user`.`role_id`
            , `user`.`created_at`, `user`.`created_by`, `user`.`modified_at`, `user`.`modified_by`
            , `role`.name AS 'role_name'
        FROM `user`
        INNER JOIN `role` ON `role`.`id` = `user`.`role_id`
        WHERE `user`.`username` = %s;
    ''')
    @fetchone('role')
    def find_by_username(cls, username):
        pass

    @classmethod
    @query('''
        SELECT `user`.`id`, `user`.`username`, `user`.`password` AS 'digest', `user`.`role_id`
            , `user`.`created_at`, `user`.`created_by`, `user`.`modified_at`, `user`.`modified_by`
            , `role`.name AS 'role_name'
        FROM `user`
        INNER JOIN `role` ON `role`.`id` = `user`.`role_id`
        WHERE `user`.`username` LIKE CONCAT('%%', %s, '%%')
        ORDER BY `role`.`name`, `user`.`username`;
    ''')
    @fetchall('role')
    def find_all_by_username_like(cls, username):
        pass

    @staticmethod
    @update_authoring
    @insert_statement('''
        INSERT INTO `user` (`username`, `password`, `role_id`
                    , `created_at`, `created_by`, `modified_at`, `modified_by`)
        VALUES (%(username)s, %(digest)s, %(role_id)s
                    , %(created_at)s, %(created_by)s, %(modified_at)s, %(modified_by)s);
    ''')
    @update_statement('''
        UPDATE `user`
        SET `username` = %(username)s, `password` = %(digest)s, `role_id` = %(role_id)s
            , `created_at` = %(created_at)s, `created_by` = %(created_by)s
            , `modified_at` = %(modified_at)s, `modified_by` = %(modified_by)s
        WHERE `id` = %(id)s;
    ''')
    def save(user):
        pass

    @staticmethod
    @statement('''
        DELETE FROM `user`
        WHERE `id` = %s;
    ''')
    def delete_by_id(user_id):
        pass


from persistence.model.role import Role
from persistence.model.user import User
