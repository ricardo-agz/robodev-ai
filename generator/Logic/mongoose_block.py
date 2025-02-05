from Logic.error_block import ErrorBlock
from Logic.logic_block import LogicBlock


class MongooseBlock(LogicBlock):
    """
    Wrapper class for Mongoose Action Logic Blocks
    (primarily useful for create, update and delete)
    """

    def __init__(
            self,
            block_type,
            model,
            params="",
            update_fields=[],
            create_fields=[],
            var_name=None,
            variant="one",
            success=[],
            error=None,
            tabs=1,
            recursive=False
    ) -> None:
        self.block_type = block_type
        self.model = model
        self.variant = variant
        self.params = params
        self.update_fields = update_fields
        self.create_fields = create_fields
        self.var_name = var_name
        self.tabs = tabs
        self.recursive = recursive
        self.adverb = self.block_type[:-1] + "ing"

        if not error:
            self.error = [
                ErrorBlock(message=f"Error {self.adverb} {model.lower()}")
            ]
        else:
            self.error = error
        self.success = success

        super().__init__(
            block_type=self.block_type,
            recursive=self.recursive
        )

    def get_create_block(self, tabs, callback_str):
        callback_func_str = self.get_callback_str(tabs)
        out_str = f"{self.TAB_CHAR * tabs}const {self.var_name} = await new {self.model}({{\n"
        # out_str += f"{self.TAB_CHAR*tabs}{{\n"

        # get rid of leading and trailing "{", "}" if any and split by ","
        split_fields = self.create_fields.strip()
        if split_fields[0] == "{":
            split_fields = split_fields[1:]
        if split_fields[-1] == "}":
            split_fields = split_fields[:-1]
        split_fields = split_fields.split(",")

        if split_fields == ['']:
            split_fields = []
        else:
            split_fields = [f"{self.TAB_CHAR * (tabs + 1)}" + x.strip() + "," for x in split_fields]
        new_fields = "\n".join(split_fields)

        out_str += new_fields + "\n"
        out_str += f"{self.TAB_CHAR * tabs}}})"
        out_str += f".save({callback_str.strip()});\n"

        return out_str

    def print_block(self, tabs=None):
        tabs = self.tabs if not tabs else tabs
        callback_func_str = self.get_callback_str(tabs)

        if self.block_type == "create":
            return self.get_create_block(tabs, callback_func_str)

        query = f"{self.block_type}Many" if self.variant == "many" else f"{self.block_type}One"
        if "_id" in self.params:
            query = f"findByIdAnd{self.block_type.capitalize()}"
            self.params = "id"

        if self.block_type == 'update':
            # get rid of leading and trailing "{", "}" if any and split by ","
            split_fields = self.create_fields.strip()
            if split_fields[0] == "{":
                split_fields = split_fields[1:]
            if split_fields[-1] == "}":
                split_fields = split_fields[:-1]
            split_fields = split_fields.split(",")

            if split_fields == ['']:
                split_fields = []
            else:
                split_fields = [f"{self.TAB_CHAR * (tabs + 1)}" + x.strip() + "," for x in split_fields]
            new_fields = "\n".join(split_fields)

            update_fields_str = f"{self.TAB_CHAR * tabs}{{\n" + new_fields + f"\n{self.TAB_CHAR * tabs}}},\n"
        else:
            update_fields_str = ''

        var_str = f"const {self.var_name} = await " if self.var_name else ''

        out = f"{self.TAB_CHAR * tabs}{var_str}{self.model}.{query}({self.params},\n" + \
              update_fields_str + \
              callback_func_str + \
              ");\n"

        return out
