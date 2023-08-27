
with open("tmp.txt", "r") as f:
    data = f.readlines()

tps = []
for i in range(0, len(data), 2):
    time = eval(data[i].strip().split(" ")[-1])
    count = eval(data[i+1].strip().split(" ")[-1])
    tps.append(time/count)

print(tps)
print(sum(tps)/len(tps))
    