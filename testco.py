x = [0,4,4,4,2,1,4,6,0,0,2,3,3,0,1,6,0,5,6,1,4,1,0,3]
i=0
x0 = 0
x1 = 0
x2 = 0
x3 = 0
x4 = 0
x5 = 0
x6 = 0
x7 = 0

j=1
while(j < 25) :
    if(x[i] == 0) :
        x0 += 1
    if(x[i] == 1) :
        x1 += 1
    if(x[i] == 2) :
        x2 += 1
    if(x[i] == 3) :
        x3 += 1
    if(x[i] == 4) :
        x4 += 1
    if(x[i] == 5) :
        x5 += 1
    if(x[i] == 6) :
        x6 += 1
    if(x[i] == 7) :
        x7 += 1
    j+=1
    i+=1

print(x0)
print(x1)
print(x2)
print(x3)
print(x4)
print(x5)
print(x6)
print(x7)