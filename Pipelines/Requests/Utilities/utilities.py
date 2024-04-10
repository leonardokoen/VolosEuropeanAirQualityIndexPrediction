def calculate_eaqi(value : float) -> int:
    if value <= 10:
        return 0
    elif value <= 20:
        return 1
    elif value <= 25:
        return 2
    elif value <= 50:
        return 3
    elif value <= 75:
        return 4
    else:
        return 5
    