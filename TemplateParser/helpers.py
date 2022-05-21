from re import sub
import inflect

inflectEngine = inflect.engine()

def pascal_case(s):
  if type(s) != str: return ""
  s = s.strip().replace(" ", "_")
  if s == "": return ""
  if "_" in s:
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    fst = s[0].upper()
    return fst + ''.join([s[0].lower(), s[1:]])[1:]
  else:
    return s[0].upper() + s[1:]

def camel_case(s):
  if type(s) != str: return ""
  s = s.strip().replace(" ", "_")
  if s == "": return ""
  if "_" in s:
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    fst = s[0].upper()
    return fst + ''.join([s[0].lower(), s[1:]])[1:]
  else:
    return s[0].lower() + s[1:]

def title_space_case(s):
  if type(s) != str: return ""
  s = s.strip().replace(" ", "_")
  if s == "": return ""
  if "_" in s:
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    s = sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', s)
    fst = s[0].upper()
    return fst + ''.join([s[0].lower(), s[1:]])[1:]
  else:
    s = sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', s)
    return s[0].upper() + s[1:]

def camel_to_snake(s):
  if type(s) != str: return ""
  s = s.strip().replace(" ", "_")
  name = sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
  return sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()

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