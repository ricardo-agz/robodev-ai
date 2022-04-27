from re import sub
import inflect

inflectEngine = inflect.engine()

def pascal_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  fst = s[0].upper()

  return fst + ''.join([s[0].lower(), s[1:]])[1:]

def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])

def camel_to_snake(name):
  name = sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
  return sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def append_at_index(arr, subarr, index):
  return arr[:index] + subarr + arr[index+1:]

def camel_to_dash(s):
  return sub(r'(?<!^)(?=[A-Z])', '-', s).lower()

def pluralize(s):
  if inflectEngine.plural_noun(s):
    return inflectEngine.plural_noun(s)
  return inflectEngine.plural_noun(s)

def singularize(s):
  if inflectEngine.singular_noun(s):
    return inflectEngine.singular_noun(s)
  return s