from persistence.decorators import (query, fetchall, fetchone, update_ownership, update_authoring,
                                    insert_statement, update_statement, statement)
from persistence.repository import AbstractRepository


class RecipeRepository(AbstractRepository):
    @staticmethod
    def get_entity_factory():
        return Recipe.create

    @staticmethod
    def get_join_factory(join_key):
        return Category.create if join_key == 'category' else None

    @classmethod
    @query('''
        SELECT `recipe`.`id`, recipe.`category_id`
            , `recipe`.`name`, `recipe`.`description`, `recipe`.`difficulty`
            , `recipe`.`owned_by`
            , `recipe`.`created_at`, `recipe`.`created_by`, `recipe`.`modified_at`, `recipe`.`modified_by`
            , `category`.`name` AS 'category_name', `category`.`description` AS 'category_description'
            , `category`.`created_at` AS 'category_created_at', `category`.`created_by` AS 'category_created_by'
            , `category`.`modified_at` AS 'category_modified_at', `category`.`modified_by` AS 'category_modified_by'
        FROM `recipe`
        INNER JOIN `category` ON `category`.`id` = `recipe`.`category_id`
        ORDER BY `category`.`name`, `recipe`.`name`;
    ''')
    @fetchall('category')
    def find_all(cls):
        pass

    @classmethod
    @query('''
        SELECT `id`, `category_id`, `name`, `description`, `difficulty`
            , `owned_by`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `recipe`
        WHERE `id` = %s;
    ''')
    @fetchone
    def find_by_id(cls, recipe_id):
        pass

    @classmethod
    @query('''
        SELECT `id`, `category_id`, `name`, `description`, `difficulty`
            , `owned_by`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `recipe`
        WHERE `category_id` = %s
        ORDER BY `name`;
    ''')
    @fetchall
    def find_all_by_category_id(cls, category_id):
        pass

    @classmethod
    @query('''
        SELECT `recipe`.`id`, recipe.`category_id`
            , `recipe`.`name`, `recipe`.`description`, `recipe`.`difficulty`
            , `recipe`.`owned_by`
            , `recipe`.`created_at`, `recipe`.`created_by`, `recipe`.`modified_at`, `recipe`.`modified_by`
            , `category`.`name` AS 'category_name', `category`.`description` AS 'category_description'
            , `category`.`created_at` AS 'category_created_at', `category`.`created_by` AS 'category_created_by'
            , `category`.`modified_at` AS 'category_modified_at', `category`.`modified_by` AS 'category_modified_by'
        FROM `recipe`
        INNER JOIN `category` ON `category`.`id` = `recipe`.`category_id`
        WHERE `recipe`.`name` LIKE CONCAT('%%', %s, '%%')
        ORDER BY `category`.`name`, `recipe`.`name`;
    ''')
    @fetchall('category')
    def find_all_by_name_like(cls, name):
        pass

    @staticmethod
    @update_ownership
    @update_authoring
    @insert_statement('''
        INSERT INTO `recipe` (`category_id`, `name`, `description`, `difficulty`
                    , `owned_by`
                    , `created_at`, `created_by`, `modified_at`, `modified_by`)
        VALUES (%(category_id)s, %(name)s, %(description)s, %(difficulty)s
                    , %(owned_by)s
                    , %(created_at)s, %(created_by)s, %(modified_at)s, %(modified_by)s);
    ''')
    @update_statement('''
        UPDATE `recipe`
        SET `category_id` = %(category_id)s, `name` = %(name)s
            , `description` = %(description)s, `difficulty` = %(difficulty)s
            , `owned_by` = %(owned_by)s
            , `created_at` = %(created_at)s, `created_by` = %(created_by)s,
            `modified_at` = %(modified_at)s, `modified_by` = %(modified_by)s
        WHERE `id` = %(id)s;
    ''')
    def save(recipe):
        pass

    @staticmethod
    @statement('''
        DELETE FROM `recipe`
        WHERE `id` = %s;
    ''')
    def delete_by_id(recipe_id):
        pass


from persistence.model.category import Category
from persistence.model.recipe import Recipe
