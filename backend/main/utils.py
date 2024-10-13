from datetime import datetime
from .models import *

def to_int(str_value, def_value):
    if str_value.isdigit():
        return int(str_value)
    else:
        return def_value
    
def is_datetimes_intersect(datetime_a_1, datetime_a_2, datetime_b_1, datetime_b_2):
    if datetime_a_1 >= datetime_a_2:
        raise Exception("Cannot be datetime_a_1 >= datetime_a_2!")
    if datetime_b_1 >= datetime_b_2:
        raise Exception("Cannot be datetime_b_1 >= datetime_b_2!")    
    
    return (datetime_a_2 > datetime_b_1 and datetime_a_1 <= datetime_b_1) or (datetime_b_2 > datetime_a_1 and datetime_b_1 <= datetime_a_1)

def get_user_type_caption(user):
    if user.groups.filter(name="clients").exists():
        return "Client"
    elif user.groups.filter(name="specialists").exists():
        return "Specialist"
    elif user.groups.filter(name="admins").exists():
        return "Admin"
    else:
        return ""

def str_to_datetime(str, tz_str=""):
    if tz_str:
        return datetime.strptime(f"{str} {tz_str}", "%Y-%m-%d %H:%M:%S %z")
    else:
        return datetime.strptime(f"{str}", "%Y-%m-%d %H:%M:%S %z")