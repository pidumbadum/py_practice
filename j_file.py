import json

data = {
    'Vasya266':{'age':17, 'last_visit':'18.04.2006', 'all_time':'20 hours'}
}

#балуюсь
ans =input('Do you want to add more user? Y/N ')
while ans =='Y' or ans=='н' or ans=='y':
    users_id, age, last_visit, all_time = map(str, input('Enter information like "users_id, age, last_visit, all_time"\n').split(','))
    age = int(age)
    data[users_id] = {'age':age, 'last_visit':last_visit, 'all_time':all_time}
    ans = input('Do you want to add more user? Y/N ')

with open('user_data.json', 'w') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

#а теперь почитаем, что вышло
with open('user_data.json', 'r') as f:
    data2 = json.load(f)

print(f'JSON file: ')
for key, val in data2.items():
    print(key)
    for k, v in data2[key].items():
        a = " " * 4
        print(f'{a}{k}: {v}')