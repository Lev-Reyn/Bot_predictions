import json

file = open('testpredictions.txt')
lst = []
for i in range(20):
    lst.append(file.readline().strip())
print(lst)

with open('data_predictions/predictions.json', 'w') as file:
    json.dump(lst, file, indent=4, ensure_ascii=False)


