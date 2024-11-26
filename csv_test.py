import csv

data = [
    {"name": "David", "age": 26},
    {"name": "JJ", "age": 26},
    {"name": "Amy", "age": 30},
    {"name": "Daniel", "age": 19}
]

with open('users.csv', mode='w', newline='') as csvfile:
    fields = ['name', 'age']
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)