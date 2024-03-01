from persistence.mixins import AuthoringMixin, FileMixin
from persistence.model import AbstractEntity


class Image(AbstractEntity, FileMixin, AuthoringMixin):
    def __init__(self, image_id=None, **kwargs):
        super().__init__(**kwargs)

        self.id = image_id
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
            **self._file_form,
            **self._authoring_form
        }

    @form.setter
    def form(self, data):
        self._update_file_data(data)

    def _load_content(self):
        return ImageRepository.find_with_content_by_id(self.id).content

    def update(self, data):
        self._update_file_data(data)
        self._update_authoring_data(data)

        if 'recipe_id' in data:
            self.recipe_id = data['recipe_id']

        if 'recipe' in data:
            self.recipe = data['recipe']

    def validate(self):
        return self._validate_file_data({'png', 'jpg', 'jpeg', 'gif'})

    @staticmethod
    def create(data):
        if data is None:
            return None

        image = Image(image_id=data.get('id'))
        image.update(data)

        return image

    def __repr__(self):
        return f'<Image {self.recipe.name} - {self.filename}>'


from persistence.repository.image import ImageRepository
from persistence.repository.recipe import RecipeRepository
