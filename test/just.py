results = [["19", 0.913, (830.6, 72.8, 22.2, 49.7)], ["19", 0.8, (990.3, 64.4, 24.0, 37.8)],["19", 0.85, (685.5, 82.4, 24.5, 52.2)]]
# print(list(a))
newResults = []
for i in range(len(results)):
    newResult = []
    newResult.append(results[i][0])
    newResult.append(results[i][1])
    newResult.append(list(results[i][2]))
    newResults.append(newResult)

print(results)
print( newResults)
