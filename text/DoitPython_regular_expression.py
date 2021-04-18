import re

data = """ 
CHO 999999-1234567
KIM 888888-2345678
"""

result = []

for line in data.split('\n'): 
    stuff = re.findall('^[a-zA-Z]', line)
    if len(stuff) != 1: continue
    word_result = []
    for word in line.split(" "):
        if len(word) == 14 and word[:6].isdigit() and word[7:].isdigit():
            word = word[:6] + '-' + '*******'
        word_result.append(word)
    result.append(" ".join(word_result))
print("\n".join(result))

# 훨씬 간단
pat = re.compile("(\d{6}[-]\d{7})")
print(pat.sub("\g<1>-*******", data))

"""
기본 구조

메타 문자  
^ $ * + ? { } [ ] \ | ( )

문자클래스 
    * [], 괄호 안의 모든 문자들과 매치
    * 주의 사항 : 문자 클래스 안에서 ^를 사용하면 not의 의미가 된다. 
    * [0-9] 모든 숫자, [^0-9] 문자하고만 매치, [a-zA-Z] 모든 알파벳 문자

자주 사용하는 문자 클래스
    * \d : 모든 숫자와 매치 [0-9]
    * \D : 숫자가 아닌 것과 매치 [^0-9]
    * \s : whitespace문자와 매치 [ \t\n\r\f\v] 와 동일한 표현, 맨 앞의 빈칸은 공백 의미
    * \S : whitespace가 아닌 것과 매치 [^ \t\n\r\f\v]
    * \w : 문자 + 숫자와 매치 [a-zA-Z0-9_]와 동일한 의미
    * \W : 문자 + 숫자가 아닌 것과 매치 [^a-zA-Z0-9_]와 동일한 의미

DOT(.)
    * .은 \n을 제외한 모든 문자와 매치됨 re.dotall -> \n도 포함할 수 있음
    * a.b a와 b사이에 어떤 문자라도 있어야 함

반복(*)


"""