import os
import json

from NeutrinoAI.NeutrinoGPT.generate import NeutrinoGPT
from NeutrinoAI.BuildfileCompiler.buildfile_compiler import BuildfileCompiler
from NeutrinoAI.logger import FileLogger

logger = FileLogger()


class AIBuildfileGenerator:
    def __init__(self, app_description: str):
        self.app_description = app_description
        self.neutrino_gpt = NeutrinoGPT(self.app_description)

        models, relations, schema, controllers, routes, routes_logic = self.neutrino_gpt.generate_database_architecture()
        self.buildfile_compiler = BuildfileCompiler(
            models_list=models,
            models_schema=schema,
            model_relations=relations,
            controllers=controllers,
            routes=routes,
            routes_logic=routes_logic,
        )

    def get_buildfile(self):
        return self.buildfile_compiler.get_buildfile()

    def get_buildfile_json(self) -> str:
        buildfile_data = self.buildfile_compiler.get_buildfile()
        json_out = json.dumps(buildfile_data, indent=4)

        return json_out


def write_to_outfile(content, output_name):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    output_file_path = os.path.join(os.path.join(__location__, f"./{output_name}"))

    with open(output_file_path, "w") as output_file:
        output_file.write(content)


if __name__ == "__main__":
    app_description = \
"""
Waitlist system to keep track of Applications. Applications should contain an applicant's name (first and last), company, and a description of 
what they plan to use the product for. Applications should have a boolean "accepted" status.
I should also be able to create access codes, which consist of a random string of 6 characters. They should have a status indicating whether or not
they have been used.
"""
    logger.clear_logs()

    neutrino_ai = AIBuildfileGenerator(app_description=app_description)
    write_to_outfile(str(neutrino_ai.get_buildfile()), "output.txt")
    json_data = neutrino_ai.get_buildfile_json()
    write_to_outfile(json_data, "output.json")
