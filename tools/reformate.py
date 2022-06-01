with open('data/ev_all_votes.csv', 'r', encoding='utf-8') as f:
    data = f.readlines()

new_data = []

for row in data:
    if row.split(',')[2] >= '1990':
        new_data.append(row)

with open('ev_all_votes.csv', 'w', encoding='utf-8') as f:
    for row in new_data:
        f.write(row)

