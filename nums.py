from __future__ import print_function

# the eleven unicode characters used to draw the clock face
emdash = u'\u2501'
vert = u'\u2503'
topL = u'\u250f'
topR = u'\u2513'
botL = u'\u2517'
botR = u'\u251b'
teeL = u'\u252b'
teeR = u'\u2523'
dot = u'\u2981'
topTip = u'\u257b'
botTip = u'\u2579'

# each row of each numeral of the clock face is a string of length 9

# possible (useful) top rows
topTermR = ' ' * 7 + topTip + ' '  # term: terminating
topTermBoth = ' ' + topTip + ' ' * 5 + topTip + ' '
concDn = ' ' + topL + emdash * 5 + topR + ' '
horizLDn = ' ' + topL + emdash * 5 + '  '
horizRDn = '  ' + emdash * 5 + topR + ' '

# possible (useful) bottom rows
botTermR = ' ' * 7 + botTip + ' '
concUp = ' ' + botL + emdash * 5 + botR + ' '  # conc: concave
horizLUp = ' ' + botL + emdash * 5 + '  '
horizRUp = '  ' + emdash * 5 + botR + ' '

# possible (useful) center rows
mid2 = ' ' + topL + emdash * 5 + botR + ' '
mid3 = '  ' + emdash * 5 + teeL + ' '
mid4 = ' ' + botL + emdash * 5 + teeL + ' '
mid5 = ' ' + botL + emdash * 5 + topR + ' '
mid6 = ' ' + teeR + emdash * 5 + topR + ' '
mid8 = ' ' + teeR + emdash * 5 + teeL + ' '
mid9 = ' ' + botL + emdash * 5 + teeL + ' '

# other useful rows
left = ' ' + vert + ' ' * 7
right = ' ' * 7 + vert + ' '
both = ' ' + vert + ' ' * 5 + vert + ' '
blank = ' ' * 9
blank5 = ' ' * 5
dot5 = '  ' + dot + '  '

# see unicode.org 2300-23ff 2500-25ff

class space(object):
    lines = [blank, blank, blank, blank, blank, blank, blank, blank, blank]

class colon(object):
    lines = [blank5, blank5, dot5, blank5, blank5, dot5, blank5, blank5,\
            blank5]

class one(object):
    lines = [topTermR, right, right, right, right, right,\
            right, right, botTermR]

class two(object):
    lines = [horizRDn, right, right, right, mid2, left, left,\
            left, horizLUp]

class three(object):
    lines = [horizRDn, right, right, right, mid3, right,\
            right, right, horizRUp]

class four(object):
    lines = [topTermBoth, both, both, both, mid4, right, right,\
            right, botTermR]

class five(object):
    lines = [horizLDn, left, left, left, mid5, right, right,\
            right, horizRUp]

class six(object):
    lines = [horizLDn, left, left, left, mid6, both, both,\
            both, concUp]

class seven(object):
    lines = [horizRDn, right, right, right, right, right,\
            right, right, botTermR]

class eight(object):
    lines = [concDn, both, both, both, mid8, both, both,\
            both, concUp]

class nine(object):
    lines = [concDn, both, both, both, mid9, right, right,\
            right, botTermR]

class zero(object):
    lines = [concDn, both, both, both, both, both, both,\
            both, concUp]

if __name__ == '__main__':  # test code -- print all the digits, then 12:46:52
    digits_arr = [space, nine, eight, seven, six, five, four, three, two, one,\
            zero, colon]
    time_arr = [one, two, colon, four, seven, colon, five, two]
    print()
    for i in range(9):
        for dig in digits_arr:
            print(dig.lines[i], sep='', end='')
        print()
    print()
    print()
    for i in range(9):
        for dig in time_arr:
            print(dig.lines[i], sep='', end='')
        print()
    print()
