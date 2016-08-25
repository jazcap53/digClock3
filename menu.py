import os


class Menu:
    FGColors = [
        (' 0', 'text color',    None),
        (' 1', 'BLACK',         '\033[30m'),
        (' 2', 'BLUE',          '\033[34m'),
        (' 3', 'CYAN',          '\033[36m'),
        (' 4', 'DARKGREY',      '\033[90m'),
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
    ]

    BGColors = [
        (' 0', 'background color', None),
        (' 1', 'BLACK (*)',        '\033[40m'),
        (' 2', 'BLUE',             '\033[44m'),
        (' 3', 'CYAN',             '\033[46m'),
        (' 4', 'GREEN',            '\033[42m'),
        (' 5', 'LIGHTGRAY',        '\033[47m'),
        (' 6', 'ORANGE',           '\033[43m'),
        (' 7', 'PURPLE',           '\033[45m'),
        (' 8', 'RED',              '\033[41m')
    ]

    DisplayModes = [
        (' 0', 'display mode'),
        (' 1', '24-HOUR'),
        (' 2', '12-HOUR (*)'),
    ]

    ChimeModes = [
        (' 0', 'chime mode'),
        (' 1', 'CHIME (*)'),
        (' 2', 'SILENT')
    ]

    defaults = [7, 1, 2, 1]

    def __init__(self):
        self.header = 'Welcome to DigClock'
        self.question = 'Please select a '
        self.footer = 'Your choice, or \'Enter\' for default (*):'

    def cycle_menus(self):
        """ Call display_menu() for each menu """
        menus = [Menu.FGColors,     Menu.BGColors,
                 Menu.DisplayModes, Menu.ChimeModes]
        chosen = [['text color', None],   ['background color', None],
                  ['display mode', None], ['chime mode', None]]
        for i in range(len(menus)):
            while True:
                self.display_menu(menus[i], chosen)
                sel = self.get_selection()
                valid = self.validate_selection(sel, len(menus[i]))
                if valid:
                    break
            if not sel.strip():
                chosen[i][1] = Menu.defaults[i]
            else:
                chosen[i][1] = int(sel)

    def display_menu(self, this_menu, chosen):
        """
        Present a menu to the user.
        :param this_menu: the menu to be displayed
               Item 0 in this_menu holds the name of the menu
        :param chosen: list of 2-element lists
               Inner list holds menu name, and the selection
               (if any) chosen for that menu
        :return: None
        """
        os.system('clear')
        print(self.header + '\n')
        print(self.question + this_menu[0][1] + ':\n')
        for item in this_menu[1:]:
            print('{:2}) {:10}'.format(item[0], item[1]))
        for item in chosen:
            if item[1]:
                print('Your {}: {}'.format(item[0], item[1]))  # TODO: get menu item name instead of number

    def get_selection(self):
        sel = raw_input('\n' + self.footer + ' ')
        return sel

    @staticmethod
    def validate_selection(sel, menu_len):
        """
        :param sel: the raw user input
        :param menu_len: a two-item menu will have entries 0, 1, 2
               where entry 0 holds the name of the menu
        :return: True on good input
                 False otherwise
        """
        ret = False
        sel = sel.strip()
        if sel:
            try:
                sel_as_int = int(sel)
                if 0 < sel_as_int < menu_len:
                    ret = True
            except ValueError:
                pass  # ret == False
        else:  # empty string is a valid input
            ret = True
        return ret

    def save_selection(self, s):
        pass  # TODO: N.Y.I
