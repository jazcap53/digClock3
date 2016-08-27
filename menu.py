import os
import time
import menu_data


class Menu:

    header = 'Welcome to DigClock'
    message = 'Please select a '
    footer = 'Your choice, or \'Enter\' for default (*):'

    def __init__(self, source, chosen):
        self.source = source
        self.description = None
        self.entries = [('', '', '')]  # make self.entries 1-indexed
        self.default = None
        self.chosen = chosen[:]

    def run(self):
        self.read()
        self.display()
        selection = None  # present to make PyCharm happy
        while True:
            selection = self.get_selection()
            test_1 = self.validate_selection(selection, len(self.entries))
            test_2 = True  # may be set to False
            if self.description == 'background color' and test_1:
                test_2 = self.check_bkgnd_ne_fgnd(selection)
                if not test_2:  # bkgrnd and text colors are the same
                    self.print_err_msg('BACKGROUND COLOR MUST NOT MATCH TEXT COLOR')
                    continue
            if test_1 and test_2:  # both tests passed
                break
            else:
                self.print_err_msg('\n\nINPUT ERROR')
        self.update_chosen(selection)

    def read(self):
        enum_menu_data = enumerate(self.source)
        for ix, item in enum_menu_data:
            if ix == 0:
                self.description = item[:]
            else:
                self.entries.append(item[:])
                # remove trailing ' (*)' from default selection
                if item[1] and item[1].endswith(' (*)'):
                    self.default = list(item)
                    self.default[1] = self.default[1].rstrip(' ()*')
        self.source = None  # gc self.source

    def display(self):
        """
        Present a menu to the user.
        :return: None
        """
        os.system('clear')
        print(Menu.header + '\n')
        print(Menu.message + self.description + ':\n')
        for item in self.entries[1:]:
            print('{:2}) {:10}'.format(item[0], item[1]))
        # print('')
        for item in self.chosen:  # self.chosen is empty for first menu
            print('Your {}: {}'.format(item[0], item[2]))

    def get_selection(self):
        sel = raw_input('\n\n' + self.footer + ' ')
        return sel

    @staticmethod
    def validate_selection(sel, menu_len):
        """
        :param sel: the raw user input
        :param menu_len: a two-item menu will have entries 0, 1, 2
               where entry 0 holds None
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
                pass  # ret is already False
        else:
            ret = True  # empty string is a valid input
        return ret

    def check_bkgnd_ne_fgnd(self, sel):
        if not sel:
            bkgnd_val = self.default[1]
        else:
            sel_as_int = int(sel)  # sel has already been strip()ped
            bkgnd_val = self.entries[sel_as_int][1].rstrip(' ()*')
        fgnd_val = self.chosen[0][2]
        if fgnd_val == bkgnd_val:
            return False
        return True

    @staticmethod
    def print_err_msg(err_msg):
        print('\033[41m')
        print(err_msg)
        time.sleep(2)
        print('\033[40m')

    def update_chosen(self, sel):
        description_as_list = [self.description]
        if sel:
            list_to_append = description_as_list
            entry_enum = enumerate(self.entries[int(sel)])
            for ix, entry in entry_enum:
                if ix == 1:
                    short_entry = entry.rstrip(' ()*')
                    list_to_append += [short_entry]
                else:
                    list_to_append += [entry]
            self.chosen.append(list_to_append)
        else:
            list_to_append = description_as_list + self.default
            self.chosen.append(list_to_append)


def cycle_menus():
    """ Call run() for each menu """
    global_chosen = []  # holds selections from all menus
    for m in [menu_data.first, menu_data.second, menu_data.third,
              menu_data.fourth]:
        this_menu = Menu(m, global_chosen)
        # display menu, get and validate selection, update saved choices
        this_menu.run()
        global_chosen.append(this_menu.chosen[-1])
    os.system('clear')
    for item in global_chosen:  # self.chosen is empty for first menu
        print('Your {}: {}'.format(item[0], item[2]))
    _ = raw_input('\n\nPress \'Enter\' to start clock...')
    return global_chosen

if __name__ == '__main__':
    cycle_menus()
