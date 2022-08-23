from Logic.logic_parser import recurse_block

def json_to_formatted_code(data):
    code = "";
    for block in data:
        try:
            parsed_block = recurse_block(block)
            if (parsed_block):
                code += parsed_block.print_block()
        except Exception as e:
            print(e);

    return code




