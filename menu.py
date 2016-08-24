import os

FGColors = {
    'FGBLACK':      ('01', '\033[30m'),
    'FGBLUE':       ('02', '\033[34m'),
    'FGCYAN':       ('03', '\033[36m'),
    'FGDARKGREY':   ('04', '\033[90m'),
    'FGGREEN':      ('05', '\033[32m'),
    'FGLIGHTBLUE':  ('06', '\033[94m'),
    'FGLIGHTCYAN':  ('07', '\033[96m'),
    'FGLIGHTGRAY':  ('08', '\033[37m'),
    'FGLIGHTGREEN': ('09', '\033[92m'),
    'FGLIGHTRED':   ('10', '\033[91m'),
    'FGORANGE':     ('11', '\033[33m'),
    'FGPINK':       ('12', '\033[95m'),
    'FGPURPLE':     ('13', '\033[35m'),
    'FGRED':        ('14', '\033[31m'),
    'FGYELLOW':     ('15', '\033[93m')
}

BGColors = {
    'BGBLACK':     ('16', '\033[40m'),
    'BGBLUE':      ('17', '\033[44m'),
    'BGCYAN':      ('18', '\033[46m'),
    'BGGREEN':     ('19', '\033[42m'),
    'BGLIGHTGRAY': ('20', '\033[47m'),
    'BGORANGE':    ('21', '\033[43m'),
    'BGPURPLE':    ('22', '\033[45m'),
    'BGRED':       ('23', '\033[41m')
}


def display_menu():
    os.system('clear')
    print('\nForeground choices:\n')
    for fg in sorted(FGColors):
        print('{:10} {:2}'.format(fg[2:], FGColors[fg][0]))
    print('\nBackground choices:\n')
    for bg in sorted(BGColors):
        print('{:10} {:2}'.format(bg[2:], BGColors[bg][0]))
    print('\nModes:\n')
    print('{:10} {:2}'.format('24-hour', '24'))
    print('{:10} {:2}'.format('12-hour', '25'))
    s = raw_input('\nPlease enter a foreground choice, a background choice, and a mode, separated by spaces:\n')
