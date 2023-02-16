from BuildfileCompiler.util import generate_unique_id


def build_crud_routes(controller_id, model, schema):
    crud_routes = []

    for i, route in enumerate(["index", "show", "create", "update", "delete"]):
        url, verb = get_route_url_and_verb(route, model)
        crud_routes.append(
            {
                "controller": controller_id,
                "id": f"rt-{controller_id}-{generate_unique_id()}",
                "middleware": [],
                "logic": get_route_logic(route, model, schema),
                "url": url,
                "handler": route,
                "verb": verb
            }
        )

    return crud_routes


def build_single_crud_route(route, controller_id, model, schema):
    url, verb = get_route_url_and_verb(route, model)

    route_data = {
        "controller": controller_id,
        "id": f"rt-{controller_id}-{generate_unique_id()}",
        "middleware": [],
        "logic": get_route_logic(route, model, schema),
        "url": url,
        "handler": route,
        "verb": verb
    }

    return route_data


def build_non_crud_route(controller_id, handler, http_method, url, description):

    route_data = {
        "controller": controller_id,
        "id": f"rt-{controller_id}-{generate_unique_id()}",
        "middleware": [],
        "logic": [],
        "url": url,
        "handler": handler,
        "verb": http_method,
        "description": description
    }

    return route_data


def pluralize(noun):
    if noun.endswith('s') or noun.endswith('x') or noun.endswith('z') or noun.endswith('ch') or noun.endswith('sh'):
        return noun + 'es'
    elif noun.endswith('y'):
        return noun[:-1] + 'ies'
    else:
        return noun + 's'


def pascal_to_dash(pascal_string):
    if not pascal_string:
        return None

    dash_string = ""
    for char in pascal_string:
        if char.isupper():
            dash_string += "-" + char.lower()
        else:
            dash_string += char
    return dash_string


def get_route_url_and_verb(route, model):
    model = pluralize(model)
    model_name = pascal_to_dash(model)

    if route == "index":
        return f"/api/{model_name}", "get"
    elif route == "show":
        return f"/api/{model_name}/:id", "get"
    elif route == "create":
        return f"/api/{model_name}", "post"
    elif route == "update":
        return f"/api/{model_name}/:id", "put"
    elif route == "delete":
        return f"/api/{model_name}/:id", "delete"

    return None, None


def get_route_logic(route, model, schema):
    if route == "index":
        return build_crud_index_logic(model, schema)
    elif route == "show":
        return build_crud_show_logic(model, schema)
    elif route == "create":
        return build_crud_create_logic(model, schema)
    elif route == "update":
        return build_crud_update_logic(model, schema)
    elif route == "delete":
        return build_crud_delete_logic(model, schema)
    return []


def build_crud_index_logic(model, schema):
    logic = [
        {
          "id": f"lgc-{model}-{generate_unique_id()}",
          "blockVariant": "query",
          "varName": "data",
          "params": "{}",
          "model": model,
          "multiple": True
        },
        {
          "id": f"lg-{model}-{generate_unique_id()}",
          "blockVariant": "return",
          "status": 200,
          "data": True,
          "returnContent": "data"
        }
      ]

    return logic


def build_crud_show_logic(model, schema):
    logic = [
        {
          "id": f"lgc-{model}-{generate_unique_id()}",
          "blockVariant": "query",
          "varName": "data",
          "params": "{ _id: id }",
          "model": model,
          "multiple": False
        },
        {
          "id": f"lg-{model}-{generate_unique_id()}",
          "blockVariant": "return",
          "status": 200,
          "data": True,
          "returnContent": "data"
        }
      ]

    return logic


def build_crud_create_logic(model, schema):
    fields_str = get_fields_str(schema)

    logic = [
        {
          "id": f"lgc-{model}-{generate_unique_id()}",
          "blockVariant": "create",
          "varName": "newData",
          "model": model,
          "fields": fields_str,
          "success": [
            {
              "id": f"lgc-{model}-{generate_unique_id()}",
              "blockVariant": "return",
              "status": 200,
              "data": False,
              "returnContent": f"New {model} was successfully created!"
            }
          ],
          "error": [
            {
              "id": f"lgc-{model}-{generate_unique_id()}",
              "blockVariant": "error",
              "status": 500,
              "returnContent": f"Error creating new {model}"
            }
          ]
        }
      ]

    return logic


def build_crud_update_logic(model, schema):
    fields_str = get_fields_str(schema)

    logic = [
        {
          "id": f"lgc-{model}-{generate_unique_id()}",
          "blockVariant": "update",
          "varName": "newData",
          "params": "{ _id: id }",
          "updateParams": fields_str,
          "model": model,
          "multiple": False,
          "success": [
            {
              "id": f"lgc-{model}-{generate_unique_id()}",
              "blockVariant": "return",
              "status": 200,
              "data": False,
              "returnContent": f"{model} was successfully updated!"
            }
          ],
          "error": [
            {
              "id": f"lgc-{model}-{generate_unique_id()}",
              "blockVariant": "error",
              "status": 500,
              "returnContent": f"Error updating {model}"
            }
          ]
        }
      ]

    return logic


def build_crud_delete_logic(model, schema):
    logic = [
        {
          "id": f"lgc-{model}-{generate_unique_id()}",
          "blockVariant": "delete",
          "varName": "data",
          "params": "{ _id: id }",
          "model": model,
          "multiple": False,
          "success": [
            {
              "id": f"lgc-{model}-{generate_unique_id()}",
              "blockVariant": "return",
              "status": 200,
              "data": False,
              "returnContent": f"{model} was successfully deleted"
            }
          ],
          "error": [
            {
              "id": f"lgc-{model}-{generate_unique_id()}",
              "blockVariant": "error",
              "status": 500,
              "returnContent": f"Error deleting {model}"
            }
          ]
        }
      ]

    return logic


def get_fields_str(schema):
    fields_str = "{ "
    for i, (field_name, data_type) in enumerate(schema):
        fields_str += f"{field_name}"
        if i < len(schema) - 1:
            fields_str += ", "
    fields_str += " }"

    return fields_str
