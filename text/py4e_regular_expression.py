"""
edwith의 py4e 정규표현식 강좌를 참조했습니다.
"""

import re

hand = open('mbox-short.txt')
for line in hand :
    line = line.rstrip()
    if line.startswith("From: "):
        print(line)


# From: 인 문자열 전체
hand = open('mbox-short.txt')
for line in hand :
    line = line.rstrip()
    if re.search('From: ', line):
        print(line)


# 첫 시작이 From: 인 경우만
hand = open("mbox-short.txt")
for line in hand :
    line = line.rstrip()
    if re.search("^From: ", line):
        print(line)

"""
re.search returns a True/False depending on whether the string matches the regular expression __
if we actually want the matching strings to be extracted, we use re.findall() __
"""

x = 'My 2 favorite numbers are 19 and 42'
y = re.findall('[0-9]+', x) #+를 제외하면 단일 숫자를 하나씩 추출
print(y)

x = 'My 2 favorite numbers are 19 and 42'
y = re.findall('[AEIOU]+', x)
print(y)

"""
Warning : Greedy Matching
The repeat characters (* and +) push outward in both directions (greedy) to match the largest possible string

From : 과 From : Using the : 중 후자가 더 길기 때문에 후자를 출력한다.
"""

x = "From : Using the : character"
y = re.findall("^F.+:", x)
print(y)

# 하지만, ?를 붙이면 탐욕적이지 않기 때문에 짧은 부분을 출력
x = "From : Using the : character"
y = re.findall("^F.+?:", x)
print(y)

"""
Fine-Tuning String Extraction 
you can refine the match for re.findall() and seperately determine which portion of the match is to be
extracted by using parentheses
"""

# 탐욕적으로 설정했기 때문에 공백을 만나기 전까지 문자열이 길어짐 (원리를 이해) 6:20초부터, 영상2 
x = "From tjdrud1323@naver.com sat jan 5"
y = re.findall("\S+@\S+", x)
print(y)

"""
Fine-Truning Strin Extraction
Parentheses are not part of the match - but they tell where to start and stop what string to extract
"""

# 괄호는 추출 시작범위와 끝 부분을 정해준다. 즉, 괄호안의 부분만 추출해라 
x = "From tjdrud1323@naver.com sat jan 5"
y = re.findall("From (\S+@\S+", x)
print(y)

#using find
data = "From stephen.maruard@uct.ac.za Sat Jan  5 09:14:16 2008"
atpos = data.find('@')
print(atpos)
sppos = data.find(' ', atpos) #find의 두 번째 파라미터는 파라미터의 시작 위치
print(sppos)
host = data[atpos+1 : sppos]
print(host)

"""
The double split pattern
Sometimes we split a line one way, and then grab one of the pieces of the line and split that piece again
"""

#using split, split의 디폴트 인자는 공백
words = data.split()
email = words[1].split('@')
print(email[1])

"""
The Reg Version
__ ^공백 -> 공백 말고 다 찾아라
"""

lin = 'From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008'
y = re.findall('@([^ ]*)', lin)
print(y)

#1. @를 찾아라
#2. 괄호안의 것들을 찾을 건데
#3. 우선, ^ 공백이 아냐
#4. 걔네들을 무한히 반복해

"""
Even cooler Regex Version
데이터 클리닝까지 동시에
"""

lin = 'From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008'
y = re.findall('^From .*@([^ ]*)', lin)
print(y)

#1. 라인의 첫 번째 줄을 살펴봐
#2. From이 있는지 살펴봐
#3. 공백 한칸 띄우고 모든 문자/숫자 반복
#4. @를 찾아봐
#5. 괄호안의 것을 찾아봐

"""
Spam Confidence
"""

hand = open('mbox-short.txt')
numlist = list()
for line in hand :
    line = line.rstrip()
    stuff = re.findall('^X-DSPAM-Confidence: ([0-9.]+)', line)
    if len(stuff) != 1 : continue
    num = float(stuff[0])
    numlist.append(num)
print('Maximum: ', max(numlist))

#1. 조건에 안 맞는 애들 X-DSPAM으로 시작하지 않는 애들은 Skip 
#2. 그리고 동시에 continue를 통해 조건에 맞지 않는 애들은 아래 코드를 실행하지 않음

"""
Escape character
If you want a special regular expression character to just behave normally 
(most of the time) you prefix it with \
"""

x = 'We just received $10.00 for cookies.'
y = re.findall('\$[0-9.]+', x)
print(y)

#1. 역슬래쉬 후 $를 찾아라
#2. 0~9 숫자 그리고, .을 찾아라
#3. 걔네만 무한 반복