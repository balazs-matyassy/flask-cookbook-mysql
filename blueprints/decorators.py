import functools
import io

from flask import abort, request, render_template, Response, send_file
from werkzeug.http import HTTP_STATUS_CODES

from blueprints.forms import EntityForm


def get_params(*names):
    def get_params_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            items = {
                name: request.args.get(name)
                for name in names
                if request.args.get(name)
            }

            return view(*args, **{**kwargs, **items})

        return wrapped_view

    return get_params_decorator


def post_params(*names):
    def post_params_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            items = {
                name: request.form.get(name)
                for name in names
                if request.form.get(name)
            }

            return view(*args, **{**kwargs, **items})

        return wrapped_view

    return post_params_decorator


def variable(name, factory, *param_names, dict_params=False, update=False, ignore_not_found=False):
    def variable_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            if name in kwargs and not update:
                return view(*args, **kwargs)

            if dict_params:
                param_items = {
                    param_name: kwargs[param_name]
                    for param_name in param_names
                    if param_name in kwargs
                }

                if len(param_items) == len(param_names):
                    value = factory(**param_items)
                else:
                    return view(*args, **kwargs)
            else:
                param_values = [kwargs[param_name] for param_name in param_names if param_name in kwargs]

                if len(param_values) == len(param_names):
                    value = factory(*param_values)
                else:
                    return view(*args, **kwargs)

            if value is None and not ignore_not_found:
                abort(404)
            elif value is None:
                return view(*args, **kwargs)

            return view(*args, **{**kwargs, name: value})

        return wrapped_view

    return variable_decorator


def entity_form(name, entity_name, fields=None,
                csrf_validation=False, json=False, submit=False, repository=None, update=False):
    def entity_form_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            if name in kwargs and not update:
                return view(*args, **kwargs)

            form = EntityForm(kwargs[entity_name], fields=fields, csrf_validation=csrf_validation, json=json)

            if submit:
                if form.validate_on_submit() and repository:
                    try:
                        repository.save(form.entity)
                    except Exception as err:
                        form.errors.append(str(err))

            return view(*args, **{**kwargs, name: form})

        return wrapped_view

    return entity_form_decorator


def csrf_form(name, json=False, submit=False, update=False):
    def csrf_form_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            if name in kwargs and not update:
                return view(*args, **kwargs)

            form = EntityForm(csrf_validation=True, json=json)

            if submit:
                form.validate_on_submit()

            return view(*args, **{**kwargs, name: form})

        return wrapped_view

    return csrf_form_decorator


def http_response(*param_names):
    def http_response_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            param_items = {
                param_name: kwargs[param_name]
                for param_name in param_names
                if param_name in kwargs
            }

            return view(*args, **param_items)

        return wrapped_view

    return http_response_decorator


def html_response(template_name, result_name, *param_names, **context):
    def html_response_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            param_items = {}

            if result_name in kwargs:
                param_items[result_name] = kwargs[result_name]

            param_items.update({
                param_name: kwargs[param_name]
                for param_name in param_names
                if param_name in kwargs
            })

            result = view(*args, **param_items)

            if isinstance(result, Response):
                return result

            return render_template(template_name, **{**context, result_name: result})

        return wrapped_view

    return html_response_decorator


def json_response(schema=None, *param_names, collection=False):
    def json_response_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            param_items = {
                param_name: kwargs[param_name]
                for param_name in param_names
                if param_name in kwargs
            }

            result = view(*args, **param_items)
            status_code = None
            location = None

            if isinstance(result, tuple):
                if len(result) >= 2:
                    status_code = result[1]

                if len(result) >= 3:
                    location = result[2]

                result = result[0]

            if isinstance(result, Response):
                return __response(result, status_code, location)
            elif isinstance(result, EntityForm):
                if result.errors:
                    payload = {
                        'error': HTTP_STATUS_CODES.get(400),
                        'messages': result.errors
                    }

                    return payload, 400

                result = result.entity

            if schema:
                if collection:
                    items = [schema(item) for item in result]

                    result = {
                        'items': items,
                        '_meta': {
                            'count': len(items)
                        },
                        '_links': {
                            'self': request.path
                        }
                    }
                else:
                    result = schema(result)

            return __response(result, status_code, location)

        return wrapped_view

    return json_response_decorator


def file_response(inline=False, *param_names):
    def file_response_decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            param_items = {
                param_name: kwargs[param_name]
                for param_name in param_names
                if param_name in kwargs
            }

            file = view(*args, **param_items)

            return send_file(
                io.BytesIO(file.content),
                mimetype=file.mimetype,
                as_attachment=not inline,
                download_name=file.filename
            )

        return wrapped_view

    return file_response_decorator


def __response(response, status_code=None, location=None):
    if status_code and location:
        return response, status_code, {'Location': location}
    elif status_code:
        return response, status_code
    elif location:
        return response, 200, {'Location': location}

    return response
