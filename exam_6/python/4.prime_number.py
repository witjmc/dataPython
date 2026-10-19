#4. 소수 구하기 (1~100까지) / 소수합계 구하기 (리스트 500개 저장)/ 2부터 소수 아닌 수 500개

#1.1~100까지 소수 구하기 (소수란 1과 자신을 제외하고 나누어 떨어지는 수가 없는 수 : 2,3,5,7,11,13,17....) 
sosuList=[2]
for num in range (3,101,2) :
    isSosu = True
    for u in range(2, num//2+1, 1) :
        if num % u == 0 :
            isSosu = False
            break
    if isSosu :
        sosuList.append(num)
print(sosuList)
cs


#2.1~500개 리스트 저장 후, 소수 리스트 합계 구하기
sosuList=[2]
num = 3
while True :
    isSosu = True
    for u in range(2, num//2+1, 1) :
        if num % u == 0 :
            isSosu = False
            break
        if isSosu :
            sosuList.append(num)
    if len(sosuList) >= 500 :
        break
    num += 2
 
print(sum(sosuList))


#3. 2부터 소수가 아닌 수를 500개 구하고, 그 합계를 내라.
sosuList = [2]
num = 3
nuSosuList = []
while True :
    isSosu = True
    for u in range (2, num//2+1, 1) :
        if num % u == 0:
            isSosu = False
            nuSosuList.append(num)
            break
        if isSosu :
            sosuList.append(num)
    if len(nuSosuList)>= 500:
        break
    num += 1
print(sum(nuSosuList))

# 작성일 : 2022.08.02
# 깃작성 : 2026.10.19


