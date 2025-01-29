from Logic.logic_parser import recurse_block


def json_to_formatted_code(data, is_logic_preview=False):
    code = ""
    for block in data:
        try:
            parsed_block = recurse_block(block)
            if parsed_block:
                if is_logic_preview:
                    parsed_block.set_tabs(1)

                code += parsed_block.print_block()
        except Exception as e:
            print(e)

    return code
