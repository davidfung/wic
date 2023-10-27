with open("p0103.txt", "r") as file:
    data = file.read().split()

for x in list(filter(lambda x: not x.isnumeric(), data)): print(x)
for x in list(filter(lambda x: x.isnumeric(), data)): print(x)
