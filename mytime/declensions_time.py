def declension(n, form_0, form_1, form_2):
    units = n % 10
    tens = (n // 10) % 10
    if tens == 1:
        return form_0
    if units in [0, 5, 6, 7, 8, 9]:
        return form_0
    if units == 1:
        return form_1
    if units in [2, 3, 4]:
        return form_2


def russian_time(hour, minute):
    """склоняет часы и минуты.
        принимает:
            часы
            минуты
        возвращает:
            строку просклоненную"""
    h = declension(hour, 'часов', 'час', 'часа')
    m = declension(minute, 'минут', 'минуту', 'минуты')

    return f'{hour} {h} {minute} {m} '
