import random

n = 20
m = 20

for i in range(n):
    aux = ""
    for j in range(m):
        
        r = random.randint(0,1)
        if(r == 0): aux = aux + "*"
        else: aux = aux + "-"
    print(aux)