# import json
#
# file = open('testpredictions.txt')
# lst = []
# for i in range():
#     lst.append(file.readline().strip())
# print(lst)
#
# with open('data_predictions/predictions.json', 'w') as file:
#     json.dump(lst, file, indent=4, ensure_ascii=False)
#
#


from datetime import datetime as dt

# число, "0 друзей", "1 друг", "2 друга"
# def declension(n, form_0, form_1, form_2):
#     units = n % 10
#     tens = (n // 10) % 10
#     if tens == 1:
#         return form_0
#     if units in [0, 5, 6, 7, 8, 9]:
#         return form_0
#     if units == 1:
#         return form_1
#     if units in [2, 3, 4]:
#         return form_2
#
#
# def russian_time(hour, minute):
#     h = declension(hour, 'часов', 'час', 'часа')
#     m = declension(minute, 'минут', 'минуту', 'минуты')
#
#     return f'{hour} {h} {minute} {m} '
#
#
# print(russian_time(hour=10, minute=1))


# import zipfile
#
# archive = zipfile.ZipFile('Archive.zip', mode='w')
# try:
#     archive.write('data_users/664295561user.json')
#     archive.write('data_users/5352265596user.json')
#     print('Files added.')
# finally:
#     print('Reading files now.')
#     archive.close()


# d1 = {
#     'name': 'lol'
# }
# d2 = {
#     'name': 'blin',
#     'surname': 'aaaa'
# }
# print(d1 | d2)
# zip_archive = zipfile.ZipFile("Archive.zip", "r") # list file information for file_info in zip_archive.infolist(): print(file_info.filename, file_info.date_time, file_info.file_size)
