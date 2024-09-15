def convert_to_int(value_str):
    try:
        value_str = value_str.replace(',', '.')
        float_value = float(value_str)
        return int(float_value)
    except ValueError:
        return None
    except AttributeError:
        return None