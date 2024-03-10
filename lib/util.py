def cast_args(args):
    return_dict = {}
    for key in args:
        value = args[key]
        try:
            casted_value = int(value)
        except:
            try:
                casted_value = float(value)
            except:
                if value.lower() == "true":
                    casted_value = True
                elif value.lower() == "false":
                    casted_value = False
                else:
                    casted_value = value

        return_dict[key] = casted_value

    return return_dict
