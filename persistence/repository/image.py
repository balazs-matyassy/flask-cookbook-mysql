from persistence.decorators import (query, fetchone, fetchall, update_authoring,
                                    insert_statement, update_statement, statement)
from persistence.repository import AbstractRepository


class ImageRepository(AbstractRepository):
    @staticmethod
    def get_entity_factory():
        return Image.create

    @classmethod
    @query('''
        SELECT `id`, `recipe_id`, `filename`, `mimetype`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `image`
        WHERE `id` = %s;
    ''')
    @fetchone
    def find_by_id(cls, image_id):
        pass

    @classmethod
    @query('''
            SELECT `id`, `recipe_id`, `filename`, `mimetype`, `content`
                , `created_at`, `created_by`, `modified_at`, `modified_by`
            FROM `image`
            WHERE `id` = %s;
        ''')
    @fetchone
    def find_with_content_by_id(cls, image_id):
        pass

    @classmethod
    @query('''
        SELECT `id`, `recipe_id`, `filename`, `mimetype`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `image`
        ORDER BY `id`;
    ''')
    @fetchall
    def find_all(cls, recipe_id):
        pass

    @classmethod
    @query('''
        SELECT `id`, `recipe_id`, `filename`, `mimetype`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `image`
        WHERE `id` = %s AND `recipe_id` = %s;
    ''')
    @fetchone
    def find_by_id_and_recipe_id(cls, image_id, recipe_id):
        pass

    @classmethod
    @query('''
        SELECT `id`, `recipe_id`, `filename`, `mimetype`
            , `created_at`, `created_by`, `modified_at`, `modified_by`
        FROM `image`
        WHERE `recipe_id` = %s
        ORDER BY `id`;
    ''')
    @fetchall
    def find_all_by_recipe_id(cls, recipe_id):
        pass

    @staticmethod
    @update_authoring
    @insert_statement('''
        INSERT INTO `image` (`recipe_id`, `filename`, `mimetype`, `content`
                    , `created_at`, `created_by`, `modified_at`, `modified_by`)
        VALUES (%(recipe_id)s, %(filename)s, %(mimetype)s, %(content)s
                    , %(created_at)s, %(created_by)s, %(modified_at)s, %(modified_by)s);
    ''')
    @update_statement('''
        UPDATE `image`
        SET `recipe_id` = %(recipe_id)s, `filename` = %(filename)s, `mimetype` = %(mimetype)s, `content` = %(content)s
            , `created_at` = %(created_at)s, `created_by` = %(created_by)s
            , `modified_at` = %(modified_at)s, `modified_by` = %(modified_by)s
        WHERE `id` = %(id)s;
    ''')
    def save(ingredient):
        pass

    @staticmethod
    @statement('''
        DELETE FROM `image`
        WHERE `id` = %s;
    ''')
    def delete_by_id(image_id):
        pass


from persistence.model.image import Image
