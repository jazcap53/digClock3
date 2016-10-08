from __future__ import print_function

""" See unicode.org 2300-23ff 2500-25ff """

# The eleven unicode characters used to draw the clock face:
emdash = u'\u2501'
vert = u'\u2503'  # vertical line
topL = u'\u250f'  # upper left corner of a rectangle
topR = u'\u2513'
botL = u'\u2517'
botR = u'\u251b'
teeL = u'\u252b'  # 'T' shape with the stem pointing leftward
teeR = u'\u2523'
dot = u'\u2981'
topTip = u'\u257b'  # tip: end of a vertical line
botTip = u'\u2579'

# Each row of each numeral of the clock face is a string of length 9.

# The possible top rows:
topTermR = ' ' * 7 + topTip + ' '  # term: terminating
topTermBoth = ' ' + topTip + ' ' * 5 + topTip + ' '
concDn = ' ' + topL + emdash * 5 + topR + ' '  # conc: concave
horizLDn = ' ' + topL + emdash * 5 + '  '
horizRDn = '  ' + emdash * 5 + topR + ' '

# The possible center rows:
mid2 = ' ' + topL + emdash * 5 + botR + ' '
mid3 = '  ' + emdash * 5 + teeL + ' '
mid4 = ' ' + botL + emdash * 5 + teeL + ' '
mid5 = ' ' + botL + emdash * 5 + topR + ' '
mid6 = ' ' + teeR + emdash * 5 + topR + ' '
mid8 = ' ' + teeR + emdash * 5 + teeL + ' '
mid9 = ' ' + botL + emdash * 5 + teeL + ' '

# The possible bottom rows:
botTermR = ' ' * 7 + botTip + ' '
concUp = ' ' + botL + emdash * 5 + botR + ' '  # conc: concave
horizLUp = ' ' + botL + emdash * 5 + '  '  # horizontal, upward at left end
horizRUp = '  ' + emdash * 5 + botR + ' '

# Other useful rows:
left = ' ' + vert + ' ' * 7  # vertical line on left
right = ' ' * 7 + vert + ' '
both = ' ' + vert + ' ' * 5 + vert + ' '
blank = ' ' * 9
blank5 = ' ' * 5
dot5 = '  ' + dot + '  '

# The eight unicode characters used to draw AM and PM:
dblTeeL = u'\u2560'
dblTeeR = u'\u2563'
dblTeeCtr = u'\u2566'  # stem of 'T' pointing downward
dblTopL = u'\u2554'
dblTopR = u'\u2557'
dblCross = u'\u2550'
dblVert = u'\u2551'
dblBotR = u'\u255d'

# Each row of each character in AM or PM is a string of length 3.
# The characters are made up double lines.

# Possible top rows of letters A, P, M:
dblConcDn = dblTopL + dblCross + dblTopR
dblTeeDn = dblTopL + dblTeeCtr + dblTopR

# Possible center rows of letters A, P, M:
dblHoriz = dblTeeL + dblCross + dblTeeR
dblHorizRUp = dblTeeL + dblCross + dblBotR
dbl3Vert = dblVert + dblVert + dblVert

# Possible bottom rows of letters A, P, M:
dbl2Vert = dblVert + ' ' + dblVert
dblLVert = dblVert + '  '


# The complete digits:
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


# Test code
if __name__ == '__main__':
    digits_arr = [Space, Nine, Eight, Seven, Six, Five, Four, Three, Two, One,
                  Zero, Colon]
    time_arr = [One, Two, Colon, Four, Seven, Colon, Five, Two]
    print()
    # Print all the digits
    for i in range(9):
        for dig in digits_arr:
            print(dig.lines[i], sep='', end='')
        print()
    print()
    print()
    # Print 12:46:52
    for i in range(9):
        for dig in time_arr:
            print(dig.lines[i], sep='', end='')
        print()
    print()
    # Print AM
    print(' ' * 25 + dblConcDn + ' ' + dblTeeDn)
    print(' ' * 25 + dblHoriz + ' ' + dbl3Vert)
    print(' ' * 25 + dbl2Vert + ' ' + dbl2Vert)
    # Print PM
    print(' ' * 25 + dblConcDn + ' ' + dblTeeDn)
    print(' ' * 25 + dblHorizRUp + ' ' + dbl3Vert)
    print(' ' * 25 + dblLVert + ' ' + dbl2Vert)
