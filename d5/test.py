from collections import defaultdict

with open('puzzle_input.txt') as f:
    manual = f.read().split("\n\n")
    
rules = manual[0].split()
updates = manual[1].split()

updates_formated = [[int(w) for w in v.split(',')] for v in updates]
rules_formated = defaultdict(list)
for rule in rules:
    r1,r2 = rule.split('|')
    rules_formated[int(r1)].append(int(r2))

result1 = 0
result2 = 0
bad = []
fixed = []

#1
for update in updates_formated:
    for i, u in enumerate(update):
        intersection_set = set(update[:i]).intersection(set(rules_formated[u]))
        if len(intersection_set) > 0:
            bad.append(update)
            break
    else:
        result1 += update[len(update)//2]

print(result1)

#2
for b in bad:
    while True: 
        for i, u in enumerate(b):
            p1 = b[:i]
            p1_copy = p1[:]
            p2 = [u]
            p3 = b[i+1:]
            intersection_set = set(p1).intersection(set(rules_formated[u]))
            if 0 < len(intersection_set):
                for p in p1_copy:
                    if p in intersection_set:
                        p1.remove(p)
                        p2.append(p)
                b = p1+p2+p3
                break     
        else:
            fixed.append(b)
            break  
for fix in fixed:
    result2 += fix[len(fix)//2]
    
print(result2)