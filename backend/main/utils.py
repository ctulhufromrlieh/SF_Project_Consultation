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