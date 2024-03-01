from persistence.mixins import AuthoringMixin
from persistence.model import AbstractEntity


class Category(AbstractEntity, AuthoringMixin):
    def __init__(self, category_id=None, **kwargs):
        super().__init__(**kwargs)

        self.id = category_id
        self.name = ''
        self.description = ''

        if kwargs:
            self.update(kwargs)

    @property
    def recipes(self):
        return RecipeRepository.find_all_by_category_id(self.id)

    @property
    def form(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            **self._authoring_form
        }

    @form.setter
    def form(self, data):
        if 'name' in data:
            self.name = data['name'].strip().capitalize()

        if 'description' in data:
            self.description = data['description'].strip()

    def update(self, data):
        self._update_authoring_data(data)
        self.form = data

    def validate(self):
        errors = []

        if self.name == '':
            errors.append('Name missing.')

        return errors

    @staticmethod
    def create(data):
        if data is None:
            return None

        category = Category(category_id=data.get('id'))
        category.update(data)

        return category

    def __repr__(self):
        return f'<Category {self.name}>'


from persistence.repository.recipe import RecipeRepository
