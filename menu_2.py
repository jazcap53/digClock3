import os
import time
import sys
import menu_data


class Menu:

    header = 'Welcome to DigClock'
    question = 'Please select a '
    footer = 'Your choice, or \'Enter\' for default (*):'

    def __init__(self, source):
        self.source = source
        self.name = None
        self.description = None
        self.data = [None]  # make self.data 1-indexed
        self.default = None
        self.chosen = []

    def read(self):
        enum_menu_data = enumerate(self.source)
        for ix, item in enum_menu_data:
            if ix == 0:
                self.name = item[:]
            elif ix == 1:
                self.description = item[:]
            else:
                self.data.append(item[:])
                if item[1].ends_with(' (*)'):
                    self.default = list(item)
                    self.default[1] = self.default[1][:-4]
        self.source = None  # gc self.source









    defaults = [(' 7', 'LIGHTCYAN', '\033[96m'), (' 1', 'BLACK', '\033[40m'),
                (' 2', '12-HOUR'), (' 1', 'CHIME')]

    menus = [FGColors, BGColors, DisplayModes, ChimeModes]

    chosen = [['text color', None, None], ['background color', None, None],
              ['display mode', None, None], ['chime mode', None, None]]

    def __init__(self):
        self.header =   'Welcome to DigClock'
        self.question = 'Please select a '
        self.footer =   'Your choice, or \'Enter\' for default (*):'

    def cycle_menus(self):  # TODO: cleanup
        """ Call display_menu() for each menu """
        for i in range(len(Menu.menus)):
            while True:
                self.display_menu(Menu.menus[i], Menu.chosen)
                sel = self.get_selection()
                if not sel:
                    sel = Menu.defaults[i][0]
                select_val_ok = self.validate_selection(sel, len(Menu.menus[i]))
                bkgnd_ok = True
                if select_val_ok and i == 1:
                    bkgnd_ok = self.check_bkgnd_ne_fgnd(sel)
                    if not bkgnd_ok:
                        print('\033[41m')
                        print('BACKGROUND COLOR MUST NOT MATCH FOREGROUND COLOR')
                        time.sleep(2)
                        print('\033[40m')
                if select_val_ok and bkgnd_ok:
                    break
            if not sel.strip():
                Menu.chosen[i][1] = int(Menu.defaults[i][0])
                Menu.chosen[i][2] = Menu.defaults[i][1]
            else:
                sel_as_int = int(sel)
                Menu.chosen[i][1] = sel_as_int
                Menu.chosen[i][2] = self.clean_default_str(Menu.menus[i][sel_as_int][1])

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
        print('\n')
        for item in chosen:
            if item[1]:
                print('Your {}: {}'.format(item[0], item[2]))

    def get_selection(self):
        sel = raw_input('\n\n' + self.footer + ' ')
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

    def check_bkgnd_ne_fgnd(self, sel):
        bkgnd_val = self.clean_default_str(Menu.menus[1][int(sel)][1])
        fgnd_val = Menu.chosen[0][2]
        if fgnd_val == bkgnd_val:
            return False
        return True

    @staticmethod
    def clean_default_str(d_str):
        if d_str.endswith(' (*)'):
            return d_str[: -4]
        return d_str
