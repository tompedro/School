c = str(input("Inserire i coefficenti dei primi termini delle equazioni separati da spazi -> ")).split(" ")
n = str(input("Inserire ora i termini noti separati da spazi -> ")).split(" ")
matrix = []
results = []
isSystem2x2 = len(c) == 4

if isSystem2x2 != 4 and isSystem2x2 != 9:
	quit()

try :
    for i in c:
        matrix.append(int(i))
    for i in n:
        results.append(int(i))
except:
    print()
    print("Guarda che devi inserire dei numeri!!")
    exit()

def calculateMatrix2x2(matrix):
    return matrix[0]*matrix[3] - matrix[1]*matrix[2]

def calculateMatrix3x3(matrix):
    a = matrix[0] * matrix[4] * matrix[8] + matrix[1] * matrix[5] * matrix[6] + matrix[2] * matrix[7] * matrix[3]
    b = matrix[2] * matrix[4] * matrix[6] + matrix[1] * matrix[8] * matrix[3] + matrix[5] * matrix[0] * matrix[7]
    return a - b
def sostituteColoumn(matrix,other,integer,length):
    res = []
    for i in range(len(matrix)):
        if (i - integer) % length == 0:
            res.append(other[int((i - integer) / length)])
        else:
            res.append(matrix[i])
    return res
    
d,dx,dy = 0,0,0
if isSystem2x2:
    d = calculateMatrix2x2(matrix)
    dx = calculateMatrix2x2(sostituteColoumn(matrix,results,0,2))
    dy = calculateMatrix2x2(sostituteColoumn(matrix,results,1,2))
else:
    d = calculateMatrix3x3(matrix)
    dx = calculateMatrix3x3(sostituteColoumn(matrix,results,0,3))
    dy = calculateMatrix3x3(sostituteColoumn(matrix,results,1,3))
    dz = calculateMatrix3x3(sostituteColoumn(matrix,results,2,3))
    print("La variabile z vale : ", dz/d)
print("La variabile x vale : " , dx/d)
print("La variabile y vale : " , dy/d)