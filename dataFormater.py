import pandas
import numpy as np
data = pandas.read_csv('Lekagul Sensor Data.csv')
unique = {}
for index, row in data.iterrows():
	if row['car-id'] not in unique:
		unique[row['car-id']] = {'path': [(row['Timestamp'], row['gate-name'])], 'type': row['car-type']}
	unique[row['car-id']]['path'].append((row['Timestamp'], row['gate-name']))
np.save('cardict.npy', unique) 
unique = np.load('cardict.npy').item()
print(set([unique[i]['type'] for i in unique]))
locations = set()
for i in unique:
	for j in unique[i]['path']:
		locations.add(j[1])
print(locations)
print(len(locations))
print(list(unique.keys())[0])
print(unique['20154301124328-262'])