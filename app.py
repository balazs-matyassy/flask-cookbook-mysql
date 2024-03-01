from flask import Flask

import blueprints.api.categories
import blueprints.api.recipes
import blueprints.api.security
import blueprints.categories
import blueprints.pages
import blueprints.recipes
import blueprints.security
import blueprints.users
import persistence
import security
from config import Config
from persistence.repository.category import CategoryRepository
from persistence.repository.role import RoleRepository


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    persistence.init_app(app)
    security.init_app(app)

    app.register_blueprint(blueprints.api.categories.bp, url_prefix='/api/categories')
    app.register_blueprint(blueprints.api.recipes.bp, url_prefix='/api/recipes')
    app.register_blueprint(blueprints.api.security.bp, url_prefix='/api/security')

    app.register_blueprint(blueprints.categories.bp, url_prefix='/categories')
    app.register_blueprint(blueprints.pages.bp, url_prefix='/')
    app.register_blueprint(blueprints.recipes.bp, url_prefix='/recipes')
    app.register_blueprint(blueprints.security.bp, url_prefix='/')
    app.register_blueprint(blueprints.users.bp, url_prefix='/users')

    app.jinja_env.globals['find_all_categories'] = CategoryRepository.find_all
    app.jinja_env.globals['find_all_roles'] = RoleRepository.find_all

    return app


if __name__ == '__main__':
    create_app().run()
