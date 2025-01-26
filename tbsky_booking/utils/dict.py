def get_value_from_dict[T](d: dict, key: str, default_value: T, sep=".") -> T:
    split_key = key.split(sep)
    if d.get(split_key[0]) and len(split_key) == 1:
        return d[split_key[0]] or default_value
    elif d.get(split_key[0]) and len(split_key) > 1:
        return get_value_from_dict(
            d[split_key[0]], sep.join(split_key[1:]), default_value, sep
        )
    return default_value
