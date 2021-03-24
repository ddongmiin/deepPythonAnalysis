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