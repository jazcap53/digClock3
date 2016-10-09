header = 'Welcome to DigClock' or None
message = 'Please select a ' or None
footer = 'Your choice, or \'Enter\' for default (*):' or None

"""
Each inner list will instantiate a Menu object.
(*) indicates the default choice for each Menu.
"""
menu_list = [[
        'text color',
        (' 1', 'BLACK',         '\033[30m'),
        (' 2', 'BLUE',          '\033[34m'),
        (' 3', 'CYAN',          '\033[36m'),
        (' 4', 'DARKGRAY',      '\033[90m'),
        (' 5', 'GREEN',         '\033[32m'),
        (' 6', 'LIGHTBLUE',     '\033[94m'),
        (' 7', 'LIGHTCYAN (*)', '\033[96m'),
        (' 8', 'LIGHTGRAY',     '\033[37m'),
        (' 9', 'LIGHTGREEN',    '\033[92m'),
        ('10', 'LIGHTRED',      '\033[91m'),
        ('11', 'ORANGE',        '\033[33m'),
        ('12', 'PINK',          '\033[95m'),
        ('13', 'PURPLE',        '\033[35m'),
        ('14', 'RED',           '\033[31m'),
        ('15', 'YELLOW',        '\033[93m')
    ],
    [
        'background color',
        (' 1', 'BLACK (*)', '\033[40m'),
        (' 2', 'BLUE',      '\033[44m'),
        (' 3', 'CYAN',      '\033[46m'),
        (' 4', 'GREEN',     '\033[42m'),
        (' 5', 'LIGHTGRAY', '\033[47m'),
        (' 6', 'ORANGE',    '\033[43m'),
        (' 7', 'PURPLE',    '\033[45m'),
        (' 8', 'RED',       '\033[41m')
    ],
    [
        'display mode',
        (' 1', '24-HOUR'),
        (' 2', '12-HOUR (*)'),
    ],
    [
        'chime mode',
        (' 1', 'CHIME (*)'),
        (' 2', 'SILENT')
    ]]
