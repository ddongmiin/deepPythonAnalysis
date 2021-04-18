import re

hand = open('mbox-short.txt')
for line in hand :
    line = line.rstrip()
    if line.startswith("From: "):
        print(line)

hand = open('mbox-short.txt')
for line in hand :
    line = line.rstrip()
    if re.search('From: ', line):
        print(line)
