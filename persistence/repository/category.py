from persistence.decorators import (query, fetchone, fetchall, insert_statement, update_statement, statement,
                                    update_authoring)
from persistence.repository import AbstractRepository


class CategoryRepository(AbstractRepository):
    @staticmethod
    def get_entity_factory():
        return Category.create

    @classmethod
    @query('''
        SELECT `id`, `name`, `description`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `category`
        ORDER BY `name`;
    ''')
    @fetchall
    def find_all(cls):
        pass

    @classmethod
    @query('''
        SELECT `id`, `name`, `description`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `category`
        WHERE `id` = %s;
    ''')
    @fetchone
    def find_by_id(cls, category_id):
        pass

    @classmethod
    @query('''
        SELECT `id`, `name`, `description`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `category`
        WHERE `name` LIKE CONCAT('%%', %s, '%%')
        ORDER BY `name`;
    ''')
    @fetchall
    def find_all_by_name_like(cls, name):
        pass

    @staticmethod
    @update_authoring
    @insert_statement('''
        INSERT INTO `category` ( `name`, `description`
                    , `created_at`, `created_by`, `modified_at`, `modified_by`)
        VALUES (%(name)s, %(description)s
                    , %(created_at)s, %(created_by)s, %(modified_at)s, %(modified_by)s);
    ''')
    @update_statement('''
        UPDATE `category`
        SET `name` = %(name)s, `description` = %(description)s
            , `created_at` = %(created_at)s, `created_by` = %(created_by)s
            , `modified_at` = %(modified_at)s, `modified_by` = %(modified_by)s
        WHERE `id` = %(id)s
    ''')
    def save(category):
        pass

    @staticmethod
    @statement('''
        DELETE FROM `category`
        WHERE `id` = %s;
    ''')
    def delete_by_id(category_id):
        pass


from persistence.model.category import Category
