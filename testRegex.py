import re
fileName = "techSupport_0F5954_3-19.wri"


str1 = "#System : Status_START"
str2 = "#System : Status_END"
str3 = "#Users : Guest Services_START"

fileName = "catsample.txt"


if __name__ == '__main__':

    fd = open(fileName, 'r')

    pattern = '#([\w\s\S]*) : ([\w\s\S]*)_(START|END)'
    pattern = '^#([\w\s\S]*) : ([\w\s\S]*)_(START|END)'

    pattern = '^#([\w\s\S]*)_(START|END)'

    p = re.compile(pattern)

    while True:

        line = fd.readline()

        if line == "":
            break

        m = p.match(line)

        if m:
            g = m.groups()
            print line.strip(), g
        else:
            print line.strip(), "#########################"







