import os 
file_to_open = os.path.expanduser('data.txt.txt')
f = open(file_to_open)
for line in f:
  t=([int(x) for x in line.split()])
#w = [int(x) for x in w.split()]
#print(w)
Max=t[0]
amount=t[1]
w=t[2:int(amount)+2]
c=t[int(amount)+2:]

a=[0 for i in range(amount)]
for i in range (amount):
    a[i]=[0 for i in range(Max+1)]
for j in range (Max):
    for i in range (amount):
        #print(i,j+1)
        if(w[i]<=(j+1)):
            if(i>0):
              plus=c[i]+a[i-1][(j+1)-w[i]]
            #print(c[i])
            #print(i-1,j+1-w[i])
            #print(a[i-1][(j+1)-w[i]])
            else:
                plus=c[i]
        else:
            plus=0
        a[i][j+1]=max(a[i-1][j+1],plus)
print("Max cost = "+ str(a[amount-1][Max]))
