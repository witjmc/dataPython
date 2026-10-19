#2.정렬하기 ( csv(엑셀)를 2차원 리스트에 저장하고 정렬하기) -중복제거 없음


#엑셀파일 읽어드리기
csvFname = 'data1.csv'
image = []
 
with open(csvFname, 'r') as reader :
    while True :
        inStr = reader.readline()
        if not inStr :
            break
        numList = inStr.split(',')
        numList = list(map(int, numList))
        image.append(numList)
#print(image)



#2차원 리스트에 저장하기
image1 = []
for lst in image :
    image1 += lst
#print(image1)



#정렬하기(오름차순)
for i in range(len(image1)-1) :
    for k in range(0, len(image1)-(i+1)) :
        if image1[k] > image1[k+1]:
            image1[k], image1[k+1] = image1[k+1], image1[k]
print(image1)



#중위값 구하기
print(image1[len(image1)//2])



#정렬하기(내림차순)
for i in range(len(image1)-1) :
    for k in range(0, len(image1)-(i+1)) :
        if image1[k] < image1[k+1]:
            image1[k], image1[k+1] = image1[k+1], image1[k]
print(image1)

작성일: 2022.08.01 깃작성:2026.10.19


