from flask import request, send_from_directory, jsonify
import generator
import os
import glob
from Logic.interact import json_to_formatted_code
from page_builder import build_controller_page, build_db_page, build_middlewares_page, build_model_page, \
    build_routes_page, build_server_page, build_transporter_page, build_mailer_page, build_base_mailer_page, \
    build_default_layout_page, build_mailer_template_page


def compile_page_preview():
    if request.get_json():
        # here we want to get the page and model from query string (i.e. ?page=server_index)
        page = request.args.get('page')

        data = request.get_json()
        project, error = generator.project_from_builder_data(data)
        if error:
            res = jsonify({"message": f"Error building project: {str(error)}"})
            res.headers.add('Access-Control-Allow-Origin', '*')
            return res, 400

        if not page or page == "":
            res = jsonify({"message": "No page passed"})
            return res, 400

        page_output = ""
        if page == "server_index":
            page_output = build_server_page(project)
        elif page == "database":
            page_output = build_db_page(project)
        elif page == "routes":
            page_output = build_routes_page(project)
        elif page == "middlewares":
            page_output = build_middlewares_page(project)
        elif page == "mailer_transporter":
            page_output = build_transporter_page(project)
        elif page == "base_mailer":
            page_output = build_base_mailer_page(project)
        elif page == "default_email_layout":
            page_output = build_default_layout_page(project)
        elif "_" in page:
            temp = page.split("_")
            model_name = temp[0]
            model = project.model_from_name(model_name)

            if "mailer" in page:
                mailer = project.mailer_from_name(model_name)
                page_output = build_mailer_page(project, mailer)

            elif "template" in page:
                template = project.template_from_name(model_name)
                page_output = build_mailer_template_page(project, template)

            # SERVER
            elif "controller" in page:
                temp_controller = None
                check_string = page.replace("_controller", "")
                for controller in project.controllers:
                    if check_string == controller.name:
                        temp_controller = controller
                page_output = build_controller_page(project, temp_controller)

            elif "model" in page:
                page_output = build_model_page(project, model)

            else:
                res = jsonify({"message": "Invalid page"})
                return res, 400

        res = jsonify({"content": page_output})
        return res, 200

    res = jsonify({"message": "Please pass a valid input"})
    return res, 400


def compile_project_warnings():
    """
    Gets a list of warnings and errors that may or may not cause build to fail
    """
    if request.get_json():
        data = request.get_json()
        project, error = generator.project_from_builder_data(data)
        if error:
            res = jsonify({"message": f"Fatal error. Project build failed: {str(error)}"})
            return res, 500

        res = jsonify({"warnings": project.warnings})
        return res, 200

    res = jsonify({"message": "Please pass a valid input"})
    return res, 400


def compile_logic_code_preview():
    """
    Given Buildfile logic structure in JSON body, returns compiled function code
    """
    if request.get_json():
        data = request.get_json()
        code_generated = json_to_formatted_code(data["logic"], True)

        res = jsonify({"code": code_generated})
        return res, 200

    res = jsonify({"message": "Please pass a valid input"})
    return res, 400


def build_project_directory():
    """
    Returns a json representation of the project directory structure
    """
    if request.get_json():
        data = request.get_json()
        project, error = generator.project_from_builder_data(data)
        if error:
            res = jsonify({"message": f"Build failed, compile project to view warnings: {str(error)}"})
            return res, 500

        res = jsonify(project.build_directory())
        return res, 200

    res = jsonify({"message": "Please pass a valid input"})
    return res, 400


def export_project(app):
    """
    Main Generator function, creates project and returns zip file
    """

    # Clean up previous project zip files
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        del_paths = glob.glob(os.path.join(path, 'neutrino_project*'))
        for del_path in del_paths:
            os.remove(del_path)
    except Exception as error:
        print("Error removing or closing downloaded file handle")
        app.logger.error("Error removing or closing downloaded file handle", error)

    # Attempt project build
    if request.get_json():
        data = request.get_json()
        project, error = generator.project_from_builder_data(data)

        # Project Build Error
        if error:
            app.logger.error("Error while attempting to build Project object in project_from_builder_data()", error)
            res = jsonify({"message": f"Fatal error. Project build failed: {str(error)}"})
            status = 500

            return res, status

        # Contains Fatal Errors
        elif project.contains_fatal_errors():
            res = jsonify({
                "message": "Project contains errors, build will fail",
                "errors": project.contains_fatal_errors()
            })
            status = 401

            return res, status

        project_name, error = generator.generator(data)

        # Project Export Error
        if error:
            app.logger.error("Error while attempting to export project in generator()", error)
            res = jsonify({"message": f"Fatal error. Project export failed: {str(error)}"})
            status = 500

            return res, status

        # Successful Export
        dir_path = os.path.dirname(os.path.realpath(__file__))
        attachment = send_from_directory(
            dir_path,
            "neutrino_project_" + data["project_name"] + ".zip",
            as_attachment=True
        )

        res = attachment
        status = 200

        return res, status

    res = jsonify({"message": "Please pass a valid input"})
    status = 400

    return res, status
