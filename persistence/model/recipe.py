from persistence.mixins import OwnershipMixin, AuthoringMixin
from persistence.model import AbstractEntity
from persistence.utils import try_parse_int


class Recipe(AbstractEntity, OwnershipMixin, AuthoringMixin):
    def __init__(self, recipe_id=None, **kwargs):
        super().__init__(**kwargs)

        self.id = recipe_id
        self.name = ''
        self.description = ''
        self.difficulty = 1
        self.__category_id = None
        self.__category = None

        if kwargs:
            self.update(kwargs)

    @property
    def category_id(self):
        return self.__category_id

    @category_id.setter
    def category_id(self, value):
        self.__category_id = value
        self.__category = None

    @property
    def category(self):
        if self.__category:
            return self.__category

        return CategoryRepository.find_by_id(self.__category_id)

    @category.setter
    def category(self, value):
        self.__category_id = value.id if value else None
        self.__category = value

    @property
    def difficulty_description(self):
        if self.difficulty == 1:
            return 'Very easy'
        elif self.difficulty == 2:
            return 'Easy'
        elif self.difficulty == 3:
            return 'Medium'
        elif self.difficulty == 4:
            return 'Difficult'
        elif self.difficulty == 5:
            return 'Very difficult'

        return 'Unknown'

    @property
    def ingredients(self):
        return IngredientRepository.find_all_by_recipe_id(self.id)

    @property
    def images(self):
        return ImageRepository.find_all_by_recipe_id(self.id)

    @property
    def form(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'difficulty': self.difficulty,
            **self._ownership_form,
            **self._authoring_form
        }

    @form.setter
    def form(self, data):
        if 'category_id' in data:
            self.category_id = try_parse_int(data['category_id'])

        if 'name' in data:
            self.name = data['name'].strip().capitalize()

        if 'description' in data:
            self.description = data['description'].strip()

        if 'difficulty' in data:
            self.difficulty = try_parse_int(data['difficulty'], 1, 1, 5)

    def update(self, data):
        self._update_ownership_data(data)
        self._update_authoring_data(data)

        if 'category' in data:
            self.category = data['category']

        self.form = data

    def validate(self):
        errors = []

        if not self.category_id:
            errors.append('Category missing.')
        elif not self.category:
            errors.append('Invalid category.')

        if not self.name:
            errors.append('Name missing.')

        return errors

    @staticmethod
    def create(data):
        if data is None:
            return None

        recipe = Recipe(recipe_id=data.get('id'))
        recipe.update(data)

        return recipe

    def __repr__(self):
        return f'<Recipe {self.name}>'


from persistence.repository.category import CategoryRepository
from persistence.repository.image import ImageRepository
from persistence.repository.ingredient import IngredientRepository
