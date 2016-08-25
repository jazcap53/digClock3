import os

FGColors = [
    (' 1', 'BLACK',       '\033[30m'),
    (' 2', 'BLUE',        '\033[34m'),
    (' 3', 'CYAN',        '\033[36m'),
    (' 4', 'DARKGREY',    '\033[90m'),
    (' 5', 'GREEN',       '\033[32m'),
    (' 6', 'LIGHTBLUE',   '\033[94m'),
    (' 7', 'LIGHTCYAN (*)', '\033[96m'),
    (' 8', 'LIGHTGRAY',   '\033[37m'),
    (' 9', 'LIGHTGREEN',  '\033[92m'),
    ('10', 'LIGHTRED',    '\033[91m'),
    ('11', 'ORANGE',      '\033[33m'),
    ('12', 'PINK',        '\033[95m'),
    ('13', 'PURPLE',      '\033[35m'),
    ('14', 'RED',         '\033[31m'),
    ('15', 'YELLOW',      '\033[93m')
]

BGColors = [
    (' 1', 'BLACK (*)',     '\033[40m'),
    (' 2', 'BLUE',      '\033[44m'),
    (' 3', 'CYAN',      '\033[46m'),
    (' 4', 'GREEN',     '\033[42m'),
    (' 5', 'LIGHTGRAY', '\033[47m'),
    (' 6', 'ORANGE',    '\033[43m'),
    (' 7', 'PURPLE',    '\033[45m'),
    (' 8', 'RED',       '\033[41m')
]

DisplayModes = [
    (' 1', '24-HOUR'),
    (' 2', '12-HOUR (*)'),
]

ChimeModes = [
    (' 1', 'CHIME (*)'),
    (' 2', 'SILENT')
]


def cycle_menus():
    headers = ['Welcome to DigClock']
    messages = ['Please select a text color']
    choices = [FGColors]
    chosen = [(None, None)]
    footer = 'Your choice, or \'Enter\' for default (*):'
    for i in range(1):
        display_menu(headers[i], messages[i], choices[i], chosen[i], footer)


def display_menu(header, message, choices, chosen, footer):
    os.system('clear')
    if header:
        print(header + '\n')
    print(message + '\n')
    for item in choices:
        print('{:2} {:10}'.format(item[0], item[1]))
    if chosen[0]:
        print(chosen[0], ' ', chosen[1])
    s = raw_input('\n' + footer + ' ')
