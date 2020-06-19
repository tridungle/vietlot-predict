# -*- coding: utf-8 -*-
import json
import csv
import datetime
file = open('dataset645.json')
data = json.load(file)
file.close()

with open('dataset645.csv','w') as dataset:
    csvFile = csv.writer(dataset)
    count = 0
    rows = []
    for item in data:
        columns = []
        columns.append(count)
        columns.append(count+1)
        columns.append(item['period'])
        columns.append(item['date'])
        date = datetime.datetime.strptime(item['date'], "%d/%m/%Y")
        columns.append(date.day)
        columns.append(date.month)
        columns.append(date.year)
        numbers = item['numbers']
        for number in numbers:
            columns.append(number)
        # print(columns)
        rows.append(tuple(columns))
        #
    data2Write = zip(*rows)
    for data in data2Write:
        csvFile.writerow(data)
