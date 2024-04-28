# regex.py

import re

def role_id_from_string(role_str):
    if re.match(r'/adm(in)?', role_str, re.I):
        return 2  # id for 'admin'
    elif re.match(r'/m(gr|ngr|anager)?', role_str, re.I):
        return 3  # id for 'manager'
    else:
        return 5  # id for 'user'

