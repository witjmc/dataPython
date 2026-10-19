#두 자연수 사이의 총합 (범위 숫자 합)

#두 자연수 입력받기
num1, num2, hap = [0]*3
num1 = int(input("숫자1입력:"))
num2 = int(input("숫자2입력:"))

#두 자연수 입력받았을 때, 큰 수와 작은 수 구분하기
#(정렬하기 -> 위치바꾸기)
if num1>num2 :
    num1, num2 = num2, num1

#두 자연수 사이의 총 합계
for i in range( num1, num2+1, 1) :
    hap += i
    print(hap)
    

# 작성일: 2022.08.02 
# 깃작성: 2026.10.19
