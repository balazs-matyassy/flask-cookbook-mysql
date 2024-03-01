from persistence.decorators import (query, fetchone, fetchall,
                                    update_authoring, insert_statement, update_statement, statement)
from persistence.repository import AbstractRepository


class IngredientRepository(AbstractRepository):
    @staticmethod
    def get_entity_factory():
        return Ingredient.create

    @classmethod
    @query('''
        SELECT `id`, `recipe_id`, `name`, `quantity`, `unit`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `ingredient`
        WHERE `id` = %s;
    ''')
    @fetchone
    def find_by_id(cls, ingredient_id):
        pass

    @classmethod
    @query('''
            SELECT `id`, `recipe_id`, `name`, `quantity`, `unit`
                , `created_at`, `created_by`, `modified_at`, `modified_by`
            FROM `ingredient`
            ORDER BY `id`;
    ''')
    @fetchall
    def find_all(cls, recipe_id):
        pass

    @classmethod
    @query('''
        SELECT `id`, `recipe_id`, `name`, `quantity`, `unit`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `ingredient`
        WHERE `id` = %s AND `recipe_id` = %s;
    ''')
    @fetchone
    def find_by_id_and_recipe_id(cls, ingredient_id, recipe_id):
        pass

    @classmethod
    @query('''
        SELECT `id`, `recipe_id`, `name`, `quantity`, `unit`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `ingredient`
        WHERE `recipe_id` = %s
        ORDER BY `id`;
    ''')
    @fetchall
    def find_all_by_recipe_id(cls, recipe_id):
        pass

    @staticmethod
    @update_authoring
    @insert_statement('''
        INSERT INTO `ingredient` (`recipe_id`, `name`, `quantity`, `unit`
                    , `created_at`, `created_by`, `modified_at`, `modified_by`)
        VALUES (%(recipe_id)s, %(name)s, %(quantity)s, %(unit)s
                    , %(created_at)s, %(created_by)s, %(modified_at)s, %(modified_by)s);
    ''')
    @update_statement('''
        UPDATE `ingredient`
        SET `recipe_id` = %(recipe_id)s, `name` = %(name)s, `quantity` = %(quantity)s, `unit` = %(unit)s
            , `created_at` = %(created_at)s, `created_by` = %(created_by)s
            , `modified_at` = %(modified_at)s, `modified_by` = %(modified_by)s
        WHERE `id` = %(id)s;
    ''')
    def save(ingredient):
        pass

    @staticmethod
    @statement('''
        DELETE FROM `ingredient`
        WHERE `id` = %s;
    ''')
    def delete_by_id(ingredient_id):
        pass


from persistence.model.ingredient import Ingredient
