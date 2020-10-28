import csv

al = []
with open(r'C:\Users\Jason\Desktop\T1XB.csv', 'r') as f:
    reader = csv.reader(f)
    for i in reader:
        al.append(i[1])

print(al)


