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

# for AM, PM
dblTeeL = u'\u2560'
dblTeeR = u'\u2563'
dblTeeCtr = u'\u2566'
dblTopL = u'\u2554'
dblTopR = u'\u2557'
dblCross = u'\u2550'
dblVert = u'\u2551'

# top rows of A, P, M
dblConcDn =dblTopL + dblCross + dblTopR
dblTeeDn = dblTopL + dblTeeCtr + dblTopR

# mid rows of A, P, M
dblHoriz = dblTeeL + dblCross + dblTeeR
dbl3Vert = dblVert + dblVert + dblVert
dbl2Vert = dblVert + ' ' + dblVert

# bot rows of A, P, M










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


class Space(object):
    lines = [blank, blank, blank, blank, blank, blank, blank, blank, blank]


class Colon(object):
    lines = [blank5, blank5, dot5, blank5, blank5, dot5, blank5, blank5,
             blank5]


class One(object):
    lines = [topTermR, right, right, right, right, right,
             right, right, botTermR]


class Two(object):
    lines = [horizRDn, right, right, right, mid2, left, left,
             left, horizLUp]


class Three(object):
    lines = [horizRDn, right, right, right, mid3, right,
             right, right, horizRUp]


class Four(object):
    lines = [topTermBoth, both, both, both, mid4, right, right,
             right, botTermR]


class Five(object):
    lines = [horizLDn, left, left, left, mid5, right, right,
             right, horizRUp]


class Six(object):
    lines = [horizLDn, left, left, left, mid6, both, both,
             both, concUp]


class Seven(object):
    lines = [horizRDn, right, right, right, right, right,
             right, right, botTermR]


class Eight(object):
    lines = [concDn, both, both, both, mid8, both, both,
             both, concUp]


class Nine(object):
    lines = [concDn, both, both, both, mid9, right, right,
             right, botTermR]


class Zero(object):
    lines = [concDn, both, both, both, both, both, both,
             both, concUp]


if __name__ == '__main__':  # test code -- print all the digits, then 12:46:52
    digits_arr = [Space, Nine, Eight, Seven, Six, Five, Four, Three, Two, One,
                  Zero, Colon]
    time_arr = [One, Two, Colon, Four, Seven, Colon, Five, Two]
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
    print(' ' * 25 + dblConcDn + ' ' + dblTeeDn)
    print(' ' * 25 + dblHoriz + ' ' + dbl3Vert)
    print(' ' * 25 + dbl2Vert + ' ' + dbl2Vert)