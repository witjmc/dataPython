#5. 2차원 배열 /리스트 (0~255 랜덤, 평균, 최d대/최소, 중위수)

#2차열 함수 선언 
from random import randint, randrange
def printBox() :
    global Box,ROW, COL
    for i in range(ROW) :
        for k in range(COL) :
            print("%3d" % Box[i][k], end = ' ')
        print( )



# 열과 행의 수(크기) 입력받기
ROW = int(input("열 :")); COL = int(input("행 : "));



#2차열 배열 만들기
Box = None; ROW, COL = 0, 0
Box = []
for i in range(ROW) :
    tmp = []
    for k in range(COL) :
        tmp.append(0)
    Box.append(tmp)



#행/열 입력받고, 해당 크기 0~255 채우기
for i in range(ROW) :
    for k in range(COL) :
        Box[i][k] = randint(0,255)
printBox()



#평균값 구하고 출력
sum = 0
for i in range(ROW) :
    for k in range(COL) :
        sum += Box[i][k]
print('평균값:', sum/(ROW*COL))



#최대값과 최소값 그 위치(행,열)을 출력
max =0
min =999
for i in range(ROW) :
    for k in range(COL) :
       if(Box[i][k]> max) :
           max = Box[i][k]
           max_i = i
           max_k = k
       elif(Box[i][k]<min) :
           min = Box[i][k]
           min_i = i
           min_k = k
 
print('최대값:', max,'(', max_i,',', max_k ,')' ,  '최소값:', min,'(' , min_i,',', min_k, ')')



#평균값을 기준으로 흑백으로 분리 후 출력
for i in range(ROW) :
    for k in range(COL) :
        if Box[i][k] > sum/(ROW*COL) :
            Box[i][k] = 255
        else :
            Box[i][k] = 0
print(Box)




######다른 방식######
#2차열 리스트 만들기 
import random
height = int(input('행-->')); width = int(input('열-->'));
image = [ [random.randint(0, 255) for _ in range(width)] for _ in range(height)]
 
for lst in image :
        print(lst)



#평균값 구하기
hap = 0
for lst in image :
    hap += sum(lst)
print('평균-->',  hap/(height * width))



#최소값 최대값 구하기
maxValue = minValue = image[0][0]
maxX = maxY = minX = minY = 0
for i in range(height) :
    for k in range(width) :
        if maxValue < image[i][k] :
            maxValue = image[i][k]; maxX=i ; maxY=k
        if minValue > image[i][k] :
            minValue = image[i][k] ; minX =i; minY =k
print('최대->',maxX, maxY, maxValue,',최소->',minX, minY, minValue)



#중위수 구하기
image1 = []
for lst in image :
    image += lst
image1.sort()
midValue = image1[len(image1)//2]
print('중위수 -->', midValue)





