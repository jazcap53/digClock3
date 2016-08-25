import os

FGColors = [
    (' 1', 'FGBLACK',      '\033[30m'),
    (' 2', 'FGBLUE',       '\033[34m'),
    (' 3', 'FGCYAN',       '\033[36m'),
    (' 4', 'FGDARKGREY',   '\033[90m'),
    (' 5', 'FGGREEN',      '\033[32m'),
    (' 6', 'FGLIGHTBLUE',  '\033[94m'),
    (' 7', 'FGLIGHTCYAN',  '\033[96m'),
    (' 8', 'FGLIGHTGRAY',  '\033[37m'),
    (' 9', 'FGLIGHTGREEN', '\033[92m'),
    ('10', 'FGLIGHTRED',   '\033[91m'),
    ('11', 'FGORANGE',     '\033[33m'),
    ('12', 'FGPINK',       '\033[95m'),
    ('13', 'FGPURPLE',     '\033[35m'),
    ('14', 'FGRED',        '\033[31m'),
    ('15', 'FGYELLOW',     '\033[93m')
]

BGColors = [
    ('01', 'BGBLACK',     '\033[40m'),
    ('02', 'BGBLUE',      '\033[44m'),
    ('03', 'BGCYAN',      '\033[46m'),
    ('04', 'BGGREEN',     '\033[42m'),
    ('05', 'BGLIGHTGRAY', '\033[47m'),
    ('06', 'BGORANGE',    '\033[43m'),
    ('07', 'BGPURPLE',    '\033[45m'),
    ('08', 'BGRED',       '\033[41m')
]

DisplayModes = [
    ('01', '24-HOUR'),
    ('02', '12-HOUR'),
]

ChimeModes = [
    ('01', 'CHIME'),
    ('02', 'SILENT')
]

def display_menu():
    os.system('clear')
    print('\n Foreground colors:' + ' ' * 20 + 'Background colors:' + ' ' * 10 +
          'Display modes:' + ' ' * 10 + 'Alarm modes' + '\n')
    for fg in range(0, 7):
        fmt_str = '{:2} {:10}' + ' ' * 5 + '{:2} {:10}' + ' ' * 6 + '| ' + '{:2} {:10}'
        print(fmt_str.format(FGColors[fg][0],
                             FGColors[fg][1][2:],
                             FGColors[fg + 8][0],
                             FGColors[fg + 8][1][2:],
                             BGColors[fg][0],
                             BGColors[fg][1][2:]
                             )
              )
    fmt_str_3 = '{:2} {:10}' + ' ' * 24 + '| ' + '{:2} {:10}'
    print(fmt_str_3.format(FGColors[7][0], FGColors[7][1][2:],
                           BGColors[7][0], BGColors[7][1][2:]
                           )
          )
    '''
    print('\nBackground colors:\n')
    for bg in sorted(BGColors):
        print('{:10} {:2}'.format(bg[2:], BGColors[bg][0]))
    print('\nModes:\n')
    print('{:10} {:2}'.format('24-hour', '24'))
    print('{:10} {:2}'.format('12-hour', '25'))
    '''
    s = raw_input('\nPlease enter a foreground color, a background color, a display mode,'
                  'and an alarm mode, separated by spaces:\n')
