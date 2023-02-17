import os
import json

from NeutrinoAI.BuildfileCompiler.route_generator import build_crud_routes, build_single_crud_route, build_non_crud_route
from NeutrinoAI.BuildfileCompiler.gpt_pseudocode_compiler import pseudocode_compiler
from NeutrinoAI.BuildfileCompiler.util import generate_unique_id
from NeutrinoAI.logger import FileLogger

logger = FileLogger()


def find_controller_from_name(controllers_list, controller_name):
    controller_name = controller_name.lower().strip()
    for controller in controllers_list:
        if controller_name == controller["name"].lower():
            return controller
    return None


class BuildfileCompiler:

    def __init__(
            self,
            models_list: list[str],
            models_schema: list[tuple[str, list[tuple[str, str]]]],
            model_relations: list[tuple[str, str, str, str, str, str, str]],
            controllers: list[str],
            routes: list[(str, list[str])],
            routes_logic: list[(str, str, str)] # (method, url, pseudocode_str)
    ):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        buildfile_path = os.path.join(os.path.join(__location__, "buildfile_template.json"))
        with open(buildfile_path, 'r') as file:
            data = json.load(file)

        self.buildfile = data
        self.models_list = models_list
        self.models_schema = models_schema
        self.model_relations = model_relations
        self.controllers = controllers
        self.routes = routes
        self.routes_logic = routes_logic
        self.model_id_map = {}
        self.controller_id_map = {}

        self.compile_buildfile()

    def get_model_from_id(self, model_id):
        if not model_id:
            return None

        for key, value in self.model_id_map.items():
            if model_id == value:
                return key

        return None

    def get_model_schema(self, model_name):
        if not model_name:
            return None

        for model, fields in self.models_schema:
            if model_name.lower() == model.lower():
                return fields
        return None

    def compile_buildfile(self) -> None:
        logger.log("compiling...")

        db_params = []
        relations = []
        controllers = []
        routes = []

        for i, (model, params) in enumerate(self.models_schema):
            model_id = f"mdl-{model}-{generate_unique_id()}"
            model_schema = {
                "model_name": model,
                "id": model_id,
                "schema": []
            }

            # save the id for the model
            self.model_id_map[model.lower()] = model_id

            for field, datatype in params:
                model_schema["schema"].append({
                    "name": field,
                    "required": True,
                    "type": datatype[0].upper() + datatype[1:]
                })

            db_params.append(model_schema)

        for i, (relation_name, model_a, model_b, relation_type, field_name_a, field_name_b, joint_table) \
                in enumerate(self.model_relations):

            if model_a.lower() in self.model_id_map and model_b.lower() in self.model_id_map:
                relation = {
                    "id": f"rel-{generate_unique_id()}",
                    "relation_name": relation_name,
                    "relation_type": relation_type,
                    "model_a": self.model_id_map[model_a.lower()],
                    "model_b": self.model_id_map[model_b.lower()],
                    "field_a": field_name_a,
                    "field_b": field_name_b,
                    "joint_table": joint_table
                }

                relations.append(relation)

        for controller in self.controllers:
            model = self.model_id_map[controller.lower()] if controller.lower() in self.model_id_map else None
            controller = {
                "name": controller,
                "affiliation": model,
                "id": f"crl-{controller}-{generate_unique_id()}"
            }

            controllers.append(controller)

        for controller_name, route_data in self.routes:
            controller_data = find_controller_from_name(controllers, controller_name)

            if not controller_data:
                logger.log(f"ERROR: controller not found: {controller_name}")
                logger.log(controllers)
                logger.log("\n")
                continue

            # standard CRUD route
            if len(route_data) == 1:
                route = route_data[0]
                model = None
                if controller_data["affiliation"]:
                    model = self.get_model_from_id(controller_data["affiliation"])

                schema = self.get_model_schema(model)
                if model and schema:
                    crud_route = build_single_crud_route(route, controller_data["id"], model, schema)
                    routes.append(crud_route)

            # other non-CRUD route
            else:
                method, url, handler, description = route_data
                non_crud_route = build_non_crud_route(
                    controller_id=controller_data["id"],
                    handler=handler,
                    http_method=method,
                    url=url,
                    description=description
                )
                routes.append(non_crud_route)

        # compile the gpt pseudocode and insert into the appropriate route
        for verb, url, pseudocode in self.routes_logic:
            try:
                logic = pseudocode_compiler(pseudocode)
            except Exception as e:
                logic = [{
                    "blockVariant": "custom",
                    "code": "// TODO: sorry Neutrino AI could not complete this function..."
                }]
                logger.log(f"ERROR COMPILING ROUTE: {e}")
            for route in routes:
                if route["verb"] == verb and route["url"] == url:
                    route["logic"] = logic

        self.buildfile["db_params"] = db_params
        self.buildfile["relations"] = relations
        self.buildfile["controllers"] = controllers
        self.buildfile["routes"] = routes

    def get_buildfile(self):
        return self.buildfile


if __name__ == "__main__":
    schema = [
        ('User', [('username', 'string'), ('email', 'string'), ('password', 'string')]),
        ('Product', [('name', 'string'), ('description', 'string'), ('price', 'number')]),
        ('Order', [('total_price', 'number'), ('payment_method', 'string')]),
        ('OrderItem', [('quantity', 'number')]), ('Category', [('name', 'string')]),
        ('ProductCategory', []),
        ('Review', [('rating', 'number'), ('content', 'string')]),
        ('Cart', [('total_price', 'number')]),
        ('Seller', [('name', 'string')]), ('Listing', [('title', 'string')])
    ]

    relations = [
        ('User', 'Product', 'many-to-many', 'products', 'purchased_by', 'OrderItem'),
        ('Product', 'OrderItem', 'one-to-many', 'order_items', 'product', None),
        ('Order', 'OrderItem', 'one-to-many', 'order_items', 'order', None),
        ('Category', 'ProductCategory', 'many-to-many', 'products', 'categories', 'ProductCategory'),
        ('User', 'Review', 'one-to-many', 'reviews', 'author', None),
        ('User', 'Cart', 'one-to-many', 'carts', 'owner', None),
        ('Seller', 'Listing', 'one-to-many', 'listings', 'seller', None),
        ('Listing', 'Product', 'one-to-many', 'products', 'listing', None)
    ]

    compiler = BuildfileCompiler(models_schema=schema, model_relations=relations)

    compiler.compile_buildfile()
    json_out = json.dumps(compiler.buildfile, indent=4)
    # print(json_out)

    # print(compiler.buildfile)



