from persistence.mixins import AuthoringMixin
from persistence.model import AbstractEntity
from persistence.utils import try_parse_int


class Ingredient(AbstractEntity, AuthoringMixin):
    def __init__(self, ingredient_id=None, **kwargs):
        super().__init__(**kwargs)

        self.id = ingredient_id
        self.name = ''
        self.quantity = 0
        self.unit = ''
        self.__recipe_id = None
        self.__recipe = None

        if kwargs:
            self.update(kwargs)

    @property
    def recipe_id(self):
        return self.__recipe_id

    @recipe_id.setter
    def recipe_id(self, value):
        self.__recipe_id = value
        self.__recipe = None

    @property
    def recipe(self):
        if self.__recipe:
            return self.__recipe

        return RecipeRepository.find_by_id(self.__recipe_id)

    @recipe.setter
    def recipe(self, value):
        self.__recipe_id = value.id if value else None
        self.__recipe = value

    @property
    def form(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            **self._authoring_form
        }

    @form.setter
    def form(self, data):
        if 'name' in data:
            self.name = data['name'].strip().lower()

        if 'quantity' in data:
            self.quantity = try_parse_int(data['quantity'], 0)

        if 'unit' in data:
            self.unit = data['unit'].strip().lower()

    def update(self, data):
        self._update_authoring_data(data)

        if 'recipe_id' in data:
            self.recipe_id = data['recipe_id']

        if 'recipe' in data:
            self.recipe = data['recipe']

        self.form = data

    def validate(self):
        errors = []

        if not self.name:
            errors.append('Name missing.')

        if self.quantity < 0:
            errors.append('Invalid quantity.')

        return errors

    @staticmethod
    def create(data):
        if data is None:
            return None

        ingredient = Ingredient(ingredient_id=data.get('id'))
        ingredient.update(data)

        return ingredient

    def __repr__(self):
        return f'<Ingredient {self.recipe.name} - {self.name}>'


from persistence.repository.recipe import RecipeRepository
