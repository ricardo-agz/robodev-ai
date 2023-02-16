import json


def parse_block(lines):
    line = lines[0]
    var_name = None
    operation = line
    if "->" in line:
        var_split = line.split("->")
        var_name = var_split[1].strip() if len(var_split) > 1 else None
        operation = var_split[0]

    if operation.startswith("RETURN"):
        args = [x.strip() for x in operation[6:].split(";")]
        status = args[0] if len(args) > 0 else 200
        message = args[1] if len(args) > 1 else "returned"
        data = args[2] if len(args) > 2 else None
        return {
            "blockVariant": "return",
            "status": status,
            "message": message,
            "returnContent": data,
        }

    elif operation.startswith("ERROR"):
        args = [x.strip() for x in operation[5:].split(";")]
        status = args[0] if len(args) > 0 else 200
        message = args[1] if len(args) > 1 else "error"
        return {
            "blockVariant": "error",
            "status": status,
            "returnContent": message,
        }

    elif operation.startswith("HASH_TEXT"):
        args = [x.strip() for x in operation[9:].split(";")]
        plaintext = args[0] if len(args) > 0 else ""
        return {
          "blockVariant": "BCrypt",
          "bcryptVariant": "hash",
          "plainText": plaintext,
          "hash": "",
          "saltRounds": 10,
          "varName": var_name
        }

    elif operation.startswith("COMPARE_TO_HASH"):
        args = [x.strip() for x in operation[15:].split(";")]
        plaintext = args[0] if len(args) > 0 else ""
        hash = args[1] if len(args) > 1 else ""
        return {
          "blockVariant": "BCrypt",
          "bcryptVariant": "compare",
          "plainText": plaintext,
          "hash": hash,
          "saltRounds": 10,
          "varName": var_name
        }

    elif operation.startswith("SIGN_JWT_TOKEN"):
        args = [x.strip() for x in operation[14:].split(";")]
        payload = args[0] if len(args) > 0 else ""
        return {
          "blockVariant": "JWT",
          "success": [],
          "error": [],
          "jwtVariant": "sign",
          "payload": payload,
          "secret": "'pleasechange'",
          "token": "",
          "expiration": 86400
        }

    elif operation.startswith("VERIFY_JWT_TOKEN"):
        args = [x.strip() for x in operation[16:].split(";")]
        token = args[0] if len(args) > 0 else ""
        return {
          "blockVariant": "JWT",
          "success": [],
          "error": [],
          "jwtVariant": "sign",
          "payload": "",
          "secret": "'pleasechange'",
          "token": token,
          "expiration": 86400
        }

    elif operation.startswith("QUERY"):
        args = [x.strip() for x in operation[5:].split(";")]
        if len(args) == 0:
            raise ValueError("Invalid syntax, QUERY required a model")
        model = args[0]
        search_fields = args[1] if len(args) > 1 else "{ }"
        multiple = args[2] if len(args) > 2 else True
        return {
            "blockVariant": "query",
            "model": model,
            "params": search_fields,
            "multiple": multiple,
            "varName": var_name
        }
    elif operation.startswith("CREATE"):
        args = [x.strip() for x in operation[6:].split(";")]
        if len(args) < 2:
            raise ValueError("Invalid syntax, CREATE requires a model and create fields")
        model = args[0]
        create_fields = args[1]
        return {
            "blockVariant": "create",
            "model": model,
            "fields": create_fields,
            "varName": var_name,
            "success": [],
            "error": []
        }
    elif operation.startswith("UPDATE"):
        args = [x.strip() for x in operation[6:].split(";")]
        if len(args) == 0:
            raise ValueError("Invalid syntax, UPDATE requires a model")
        model = args[0]
        search_fields = args[1] if len(args) > 1 else "{ }"
        update_fields = args[2] if len(args) > 2 else "{ }"
        multiple = args[3] if len(args) > 3 else False
        return {
            "blockVariant": "update",
            "model": model,
            "params": search_fields,
            "updateParams": update_fields,
            "multiple": multiple,
            "varName": var_name,
            "success": [],
            "error": []
        }
    elif operation.startswith("DELETE"):
        args = [x.strip() for x in operation[6:].split(";")]
        if len(args) == 0:
            raise ValueError("Invalid syntax, DELETE requires a model")
        model = args[0].strip
        search_fields = args[1] if len(args) > 1 else "{ }"
        multiple = args[2] if len(args) > 2 else False
        return {
            "blockVariant": "delete",
            "model": model,
            "params": search_fields,
            "multiple": multiple,
            "varName": var_name,
            "success": [],
            "error": []
        }
    else:
        return {"blockVariant": operation}


def pseudocode_compiler(code_str):
    lines = code_str.split("\n")
    lines = [x.strip() for x in lines if x.strip()]

    return rec_pseudocode_compiler(lines, 0, 0)[0]


def rec_custom_code(lines, i):
    if not lines:
        return [], i

    i += 1
    
    if lines[0].startswith("PASS"):
        return [], i

    rec_lines, rec_count = rec_custom_code(lines[1:], i)

    return ([lines[0]] + rec_lines, i + rec_count)


def rec_pseudocode_compiler(lines, i, depth):
    # base case, end of code
    if not lines:
        return [], i

    i += 1

    if lines[0].startswith("IF"):
        # recurse under IF bracket
        sub_true = lines[1:]
        true_logic, true_count = rec_pseudocode_compiler(sub_true, 0, depth + 1)

        # recurse under ELSE case
        sub_false = lines[true_count + 1:]
        false_logic, false_count = rec_pseudocode_compiler(sub_false, 0, depth + 1)

        # recurse after conditional
        sub_rest = lines[true_count + false_count + 1:]
        rest_logic, rest_count = rec_pseudocode_compiler(sub_rest, 0, depth)

        block = [{
            "blockVariant": "ifelse",
            "condition": lines[0][3:].strip(),
            "success": true_logic,
            "error": false_logic
        }]

        return (
            block + rest_logic,
            i + true_count + false_count + rest_count
        )

    if lines[0].startswith("CUSTOM"):
        # recurse under the custom code lines
        sub_custom = lines[1:]
        custom_logic, custom_count = rec_custom_code(sub_custom, 0)

        # recurse after custom
        sub_rest = lines[custom_count + 1:]
        rest_logic, rest_count = rec_pseudocode_compiler(sub_rest, 0, depth)

        logic_str = "\n".join(custom_logic)

        block = [{
            "blockVariant": "custom",
            "code": logic_str,
        }]

        return (
            block + rest_logic,
            i + custom_count
        )

    elif lines[0].startswith("ELSE"):
        return [], i

    elif lines[0].startswith("PASS"):
        return [], i

    elif lines[0].startswith("<="):
        return [], i

    elif lines[0].startswith("x="):
        return [], i

    else:
        if lines[0].startswith("CREATE") or \
                lines[0].startswith("UPDATE") or \
                lines[0].startswith("DELETE") or \
                lines[0].startswith("SIGN_JWT_TOKEN") or \
                lines[0].startswith("VERIFY_JWT_TOKEN"):

            success_logic = []
            error_logic = []
            success_count = 0
            error_count = 0
            callbacks = 0

            # recurse through callback
            if len(lines) > 2:
                if lines[1].startswith("=>"):
                    # recurse under success case
                    sub_success = lines[2:]
                    success_logic, success_count = rec_pseudocode_compiler(sub_success, 0, depth + 1)
                    callbacks += 1
                elif lines[1].startswith("=x"):
                    # recurse under error case
                    sub_error = lines[2:]
                    error_logic, error_count = rec_pseudocode_compiler(sub_error, 0, depth + 1)
                    callbacks += 1

            # recurse through second callback (if any)
            sub_rest = lines[success_count + error_count + 2:]
            if len(sub_rest) > 1:
                if sub_rest[0].startswith("=>"):
                    # recurse under success case
                    sub_success = sub_rest[1:]
                    success_logic, success_count = rec_pseudocode_compiler(sub_success, 0, depth + 1)
                    callbacks += 1
                elif sub_rest[0].startswith("=x"):
                    # recurse under error case
                    sub_error = sub_rest[1:]
                    error_logic, error_count = rec_pseudocode_compiler(sub_error, 0, depth + 1)
                    callbacks += 1

            # recurse after callbacks (if any) TODO: offset is wrong doesn't work for nested callbacks
            callback_offset = callbacks + 1
            sub_after = lines[success_count + error_count + callback_offset:]
            after_logic, after_count = rec_pseudocode_compiler(sub_after, 0, depth)

            block = parse_block(lines)
            block["success"] = success_logic
            block["error"] = error_logic

            return (
                [block] + after_logic,
                i + success_count + error_count + after_count
            )

        else:
            block = parse_block(lines)
            rec_res, rec_count = rec_pseudocode_compiler(lines[1:], 0, depth)
            return [block] + rec_res, i + rec_count


"""
Pseudocode Syntax:

PASS defines the end of an ELSE statement
=>
defines a callback function on the success of a database operation
<=
=x
defines a callback function when catching an error on a database operation
x=

variable names can be assigned by ->

Functions defined by 
OPERATION arg1; arg2; arg3, ...

ex:
QUERY User; { id: req.body.id }; false -> user
"""

if __name__ == "__main__":
    code = """
    QUERY User; { _id: req.params.follower_id }; false -> follower
    IF follower 
        QUERY User; { _id: req.params.followed_id }; false -> followed
        IF followed 
            UPDATE User; { _id: follower._id }; { $push: { following: followed._id } }
                =>
                <=
                =x
                ERROR 500; "error following"
                x=
            UPDATE User; { _id: followed._id }; { $push: { followers: follower._id } }
                =>
                <=
                =x
                ERROR 500; "error following"
                x=
            RETURN 200; "followed successfully"
        ELSE
            ERROR 404; "followed user not found"
    ELSE 
        ERROR 404; "follower user not found"
        PASS
    """


    custom_code = """
    console.log("hello");
    console.log("world");
    PASS
    """

    # print(rec_custom_code(custom_code.splitlines(), 0))

    # print(json.dumps(pseudocode_compiler(code), indent=2))

