from NeutrinoAI.NeutrinoGPT.generate import NeutrinoGPT


# def generate_database_architecture(self):
#         models = self.generate_db_tables()
#         relations = self.generate_relations(models)
#         schema = self.generate_schema(models, relations)
#         controllers = self.generate_controllers(models, relations)
#         routes = self.generate_routes(models, schema, relations, controllers)

#         print("==========")
#         print("Models:\n", models)
#         print("Relations:\n", relations)
#         print("Schema:\n", schema)
#         print("Controllers:\n", controllers)
#         print("Routes:\n", routes)
#         print("==========")

#         return models, relations, schema, controllers, routes


APP_DESCRIPTION = """
simple twitter-like blog app
"""

if __name__ == "__main__":
    generator = NeutrinoGPT(app_description=APP_DESCRIPTION)

    models = generator.generate_db_tables()
    print(models)
    