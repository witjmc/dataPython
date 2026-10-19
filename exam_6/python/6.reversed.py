#6.문자열에서 숫자만 추출 (영문자가 뒤/앞에 있을 때 -거꾸로:reversed)

# 문자열에서 숫자만 추출 
#  다음 문자열에서 숫자만 추출한 후 더해라. 단 영문자가 뒤에 나오면 제외.
# " 1이 3개면 111이됩니다. 그런데 88K을 두번 더하면 11,11이 되어서 22가 됩니다."
#   결과 : 1+3+111+11+11+22 +11 =170
# 거꾸로 : 1+3+111+88+11+11+22+11 = 258 (단 영문자가 앞에 나오면 제외.)

# 영문자가 뒤에 있을 때
myStr = " 1이 3개면 111이됩니다. 그런데 88k을 두번 더하면 11,11이 되어서 22가 됩니다.11"
numStr = ""
hap = 0
for i in range(len(myStr)) :
    ch = myStr[i]  # [0]공백 [1]1 [2]이 [3]공백 ...으로 myStr길이만큼 ch변수에 들어감
    print('[', i, '번째문자]', myStr[i])
    if ch.isnumeric() : # isnumeric 숫자인지 아닌지 판별, 숫자이면 참이므로 아래실행,
        numStr += ch    #  거짓이면 else문으로
        print(i,'번째', numStr)
    else :
        if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z' :
            numStr = ""  #영문자를 만나면,공백처리
        else :
            if len(numStr) > 0 : #numStr변수에 무엇이라도 들어가 있으면 아래 실행,
                print(myStr[i], '!! 여기서 이전 숫자가 저장되는부분')
                # 하나도 없으면 다음 for문으로
                hap += int(numStr) #numStr변수에 담겨진 것은 숫자같아보이지만,
                numStr = ""        # 문자!,그래서 숫자로 자료형변형 후,
                            # hap변수에 넣고, numStr변수는 초기화, 빈것으로 만들기~!
if len(numStr) > 0:  #마지막 문장 '~22가 됩니다.11'에서 11은 그 다음 문자가 없다.
    hap += int(numStr)  #for문 마지막 if문을 보면, 문자가 ch변수에 들어올 때,
    numStr = ""         # 이전에 담긴 numStr변수 숫자처럼 보이는 문자를
                        # hap변수에 넣었다.
                        # 그런데, 마지막 11은 그렇게 해주는 기능이 없기에
                        # for문 끝나고 만들어 준다.
print(hap)
Colored by Color Scripter
cs

#영문자가 앞에 있을 때
myStr = " 1이 3개면 111이됩니다. 그런데 88k8을 두번 더하면 11,11이 되어서 22가 됩니다.11"
numStr = ""
hap = 0
for i in reversed(range(len(myStr))) : #영문자가 앞에 있을 때 문장을 거꾸로 세어간다. 
    ch = myStr[i]  
    print('[', i, '번째문자]', myStr[i])
    if ch.isnumeric() : 
        numStr += ch    
        print(i,'번째', numStr)
    else :
        if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z' :
            numStr = ""  
        else :
            if len(numStr) > 0 : 
                print(myStr[i], '!! 여기서 이전 숫자가 저장되는부분')
                hap += int(numStr) 
                numStr = ""                                   
if len(numStr) > 0:  
    hap += int(numStr)  
    numStr = ""                                                 
print(hap)

# 작성일 : 2022.08.03
# 깃작성 : 2026.10.19
