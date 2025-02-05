from Logic.interact import json_to_formatted_code


class Route:
    #  controller_id = route["controller"],
    #       id = route["id"],
    #       url = route["url"],
    #       handler = route["handler"],
    #       verb = route["verb"],
    #       logic = route["logic"],
    #       middleware=route["middleware"]
    def __init__(
            self,
            controller_id=None,
            controller_name=None,
            id=None,
            url=None,
            handler=None,
            verb=None,
            logic=[],
            middleware=None,
            disabled=False,
            protected=False,
            pagination=False,
            alias=None
    ) -> None:
        self.controller_id = controller_id
        self.controller_name = controller_name
        self.id = id
        self.url = url
        self.handler = handler
        self.verb = verb
        self.middleware = middleware
        self.disabled = disabled
        self.protected = protected
        self.logic = logic
        self.pagination = pagination
        self.alias = alias
        self.TAB_CHAR = "  "

        if self.logic != "":
            pass

    def get_logic(self):
        return self.logic

    def get_route_call(self):
        """
        router.get('/users/:id', verifyJWT, UserController.find)
        """
        middleware = f", " + ",".join(self.middleware) if len(self.middleware) != 0 else ""
        return f"router.{self.verb.lower()}('{self.url}'{middleware}, {self.controller_name}Controller.{self.handler});\n"

    def get_params_from_url(self):
        temp = self.url.split('/')
        out = [x.replace(":", "") for x in temp if ":" in x]
        return out

    def get_param_declaration(self):
        params = self.get_params_from_url()
        param_str = ""

        for i, p in enumerate(params):
            param_str += p
            param_str += ", " if i != len(params) - 1 else ""
        out = f"const {{ {param_str} }} = req.params;"

        if len(params) > 0:
            return out
        return ""

    def get_handler_function(self):
        # header comment
        url_params = self.get_params_from_url()
        params_comment = f" * params: {url_params}\n\t" if len(url_params) > 0 else ""
        func = f'{self.TAB_CHAR}/*\n{self.TAB_CHAR} * {self.handler}\n{self.TAB_CHAR} * url: {self.url}\n{self.TAB_CHAR}{params_comment} */\n'
        # declaration
        func += f'{self.TAB_CHAR}{self.handler}: async (req, res)' + " => {\n"
        func += f"{2 * self.TAB_CHAR}try {{\n"
        func += f"{self.TAB_CHAR * 3}{self.get_param_declaration()}\n" if len(url_params) > 0 else ""
        logic = json_to_formatted_code(self.logic)
        for line in logic.split("\n"):
            if line != "":
                func += f"{self.TAB_CHAR}" + line + "\n"
        func += f"{self.TAB_CHAR * 2}}} catch(e) {{\n"
        func += f"{self.TAB_CHAR * 3}console.error(`server error in {self.controller_name}Controller {self.handler}() : ${{e}}`);\n"
        func += f"{self.TAB_CHAR * 2}}};\n"
        func += f"{self.TAB_CHAR}}},\n"
        return func
