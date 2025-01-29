from Logic.conditional_block import ConditionalBlock
from Logic.custom_block import CustomBlock
from Logic.mailer_block import MailerBlock
from Logic.next_block import NextBlock
from Logic.query_block import QueryBlock
from Logic.error_block import ErrorBlock
from Logic.return_block import ReturnBlock
from Logic.delete_block import DeleteBlock
from Logic.update_block import UpdateBlock
from Logic.create_block import CreateBlock
from generator.Logic.bcrypt_block import BcryptBlock
from Logic.jwt_block import JWTBlock


def recurse_block(block):
    if 'success' in block or 'error' in block:
        success_list = []
        error_list = []
        for sub_block in block['success']:
            success_list.append(recurse_block(sub_block))

        for sub_block in block['error']:
            error_list.append(recurse_block(sub_block))

        parsed = parse_block(block, success=success_list, error=error_list)
        return parsed
    else:
        return parse_block(block)


def parse_block(block, success=[], error=[]):
    block_type = block['blockVariant']
    model = block['model'] if 'model' in block else None
    params = block['params'] if 'params' in block else None
    var_name = block['varName'] if 'varName' in block else None
    bcrypt_variant = block['bcryptVariant'] if 'bcryptVariant' in block else None
    plain_text = block['plainText'] if 'plainText' in block else None
    hash = block['hash'] if 'hash' in block else None
    salt_rounds = block['saltRounds'] if 'saltRounds' in block else None
    variant = block['variant'] if 'variant' in block else None
    condition = block['condition'] if 'condition' in block else None
    status = block['status'] if 'status' in block else None
    message = block['message'] if 'message' in block else None
    data = block['data'] if 'data' in block else None
    create_fields = block['fields'] if 'fields' in block else None
    update_fields = block['updateParams'] if 'updateParams' in block else None
    multiple = block["multiple"] if 'multiple' in block else None
    return_content = block['returnContent'] if 'returnContent' in block else None
    code = block['code'] if 'code' in block else None
    jwt_variant = block['jwtVariant'] if 'jwtVariant' in block else None
    payload = block['payload'] if 'payload' in block else None
    secret = block['secret'] if 'secret' in block else None
    token = block['token'] if 'token' in block else None
    expiration = block['expiration'] if 'expiration' in block else None
    # Mailers
    mailer = block['mailer'] if 'mailer' in block else None
    data_context = block['dataContext'] if 'dataContext' in block else None
    recipient = block['recipient'] if 'recipient' in block else None
    subject = block['subject'] if 'subject' in block else None
    template = block['template'] if 'template' in block else None

    if block_type == 'query':
        if (multiple):
            variant = "many"
        else:
            variant = "one"

        return QueryBlock(model=model, params=params, var_name=var_name, variant=variant)

    elif block_type == 'custom':
        return CustomBlock(code=code)

    elif block_type == 'error':
        return ErrorBlock(status=status, message=return_content)

    elif block_type == 'return':
        return ReturnBlock(status=status, data=data, return_content=return_content)

    elif block_type == 'conditional':
        return ConditionalBlock(condition=condition, success=success, error=error)

    elif block_type == 'if':
        return ConditionalBlock(condition=condition, success=success, error=[])

    elif block_type == 'ifelse':
        return ConditionalBlock(condition=condition, success=success, error=error)

    elif block_type == 'create':
        return CreateBlock(
            model=model,
            create_fields=create_fields,
            var_name=var_name,
            success=success,
            error=error
        )

    elif block_type == 'update':
        if (multiple):
            variant = "many"
        else:
            variant = "one"

        return UpdateBlock(
            model=model,
            params=params,
            update_fields=update_fields,
            var_name=var_name,
            variant=variant,
            success=success,
            error=error
        )

    elif block_type == 'delete':
        if (multiple):
            variant = "many"
        else:
            variant = "one"

        return DeleteBlock(
            model=model,
            params=params,
            var_name=var_name,
            variant=variant,
            success=success,
            error=error
        )
    elif block_type == "BCrypt":

        return BcryptBlock(model, var_name, bcrypt_variant, plain_text, hash, salt_rounds)

    elif block_type == "JWT":

        return JWTBlock(model, jwt_variant, payload, secret, token, expiration, success, error)

    elif block_type == "next":
        return NextBlock()

    elif block_type == "mailer":

        return MailerBlock(mailer, recipient, subject, data_context, template)
