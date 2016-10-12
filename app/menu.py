from __future__ import print_function
import os
import time
# TODO: import entire menu_data package
from menu_data import menu_list
from menu_data import header, message, footer
from menu_data import bad_combinations

# TODO: make err_msg into an @property
# TODO: simplify flow
class Menu:
    """
    Class provided: an interactive menu presented to user
    Instantiated by global function cycle_menus()
    """
    def __init__(self, source, chosen, headr, msg, footr):
        self.source = source
        self.header = headr
        self.message = msg
        self.footer = footr
        self.description = None
        self.entries = [('', '', '')]  # make self.entries 1-indexed
        self.default = None
        self.selection = None
        self.bad_combinations = bad_combinations
        self.chosen = chosen[:]  # TODO: comment on why [:] is necessary
        self.err_msg = None

    def run(self):
        """
        Calls subroutines that:
            read and display the current menu
            get and validate the user response
        Called by: global function cycle_menus()
        """
        self.read()
        self.display()
        while True:  # loop until user makes a valid selection
            self.get_selection()
            test_1 = self.validate_selection()
            test_2 = self.good_combination()
            if not test_2:
                self.print_err_msg()
                continue
            if test_1 and test_2:  # both tests passed
                break
            else:
                self.err_msg = '\n\nINPUT ERROR'
                self.print_err_msg()
        self.update_chosen(self.selection)

    def read(self):
        """
        Reads the menu data
        Called by: self.run()
        """
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
        Present current menu to the user.
        Called by: self.run()
        """
        os.system('clear')
        print(self.header + '\n')
        print(self.message + self.description + ':\n')
        for item in self.entries[1:]:
            print('{:2}) {:10}'.format(item[0], item[1]))
        print()
        for item in self.chosen:  # self.chosen is empty for first menu
            print('Your {}: {}'.format(item[0], item[2]))

    def get_selection(self):
        """
        Get the user selection.
        Called by: self.run()
        """
        self.selection = raw_input('\n\n' + self.footer + ' ')

    def validate_selection(self):
        """
        Checks that user input represents an integer in the correct
        range, or is a null string.
        :return: True on good input
                 False otherwise
        Called by: self.run()
        """
        menu_len = len(self.entries)
        ret = False
        self.selection = self.selection.strip()
        if self.selection:
            try:
                sel_as_int = int(self.selection)
                if 0 < sel_as_int < menu_len:
                    ret = True
            except ValueError:  # input is not an integer
                pass  # ret is already False
        else:
            ret = True  # empty string is a valid input
        return ret

    def good_combination(self):
        """

        :return:
        """
        if not self.selection:  # self.selection has already been strip()ped
            new_value = self.get_current_default()
        else:
            selection_int = int(self.selection)
            new_value = int(self.entries[selection_int][0])
        choices_so_far = [int(item[1]) for item in self.chosen]
        choices_so_far.append(new_value)
        choices_tuple = tuple(choices_so_far)
        if choices_tuple in self.bad_combinations:
            # get error message corresponding to this bad combination
            self.err_msg = self.bad_combinations[choices_tuple]
            return False
        return True

    def get_current_default(self):
        return int(self.default[0])

    def print_err_msg(self):
        """
        Called by: self.run()
        """
        print('\033[41m')  # red background
        print(self.err_msg)
        time.sleep(2)
        print('\033[40m')  # black background

    def update_chosen(self, sel):
        """
        Stores option selected by user
        :param sel: user choice as a string (may be null)
        Called by: self.run()
        """
        # description is a *string* describing the current menu
        # e.g, 'text color'
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
        else:
            list_to_append = description_as_list + self.default
        self.chosen.append(list_to_append)


def cycle_menus():
    """
    Calls run() for each menu
    :return: the collected user choices for each menu run
    Called by: client get_time.run_clock()
    """
    global_chosen = []  # holds selections from all menus
    for m in menu_list:
        this_menu = Menu(m, global_chosen, header, message, footer)
        # read and display menu, get and validate selection,
        # update saved choices
        this_menu.run()
        global_chosen.append(this_menu.chosen[-1])
    os.system('clear')
    for item in global_chosen:  # self.chosen is empty for first menu
        print('Your {}: {}'.format(item[0], item[2]))
    _ = raw_input('\n\nPress \'Enter\' to start clock...')
    return global_chosen

if __name__ == '__main__':
    cycle_menus()
