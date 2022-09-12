from Logic.logic_parser import recurse_block

def json_to_formatted_code(data, islogicpreview=False):
    code = "";
    for block in data:
        try:
            parsed_block = recurse_block(block)
            if (parsed_block):
                # print(parsed_block)
                # print(parsed_block.print_block())
                if islogicpreview:
                  parsed_block.set_tabs(1)
                  
                code += parsed_block.print_block()
        except Exception as e:
            print(e);

    return code




