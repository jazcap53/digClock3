from __future__ import print_function
import time
import menu_data


# TODO: update docstrings throughout this file
def clear_screen():
    """
    Using this function because calling os.system('clear') inserts
    multiple blank lines into the output of unit tests.
    :return: None
    """
    print('\n' * 45)


class CycleMenus(object):

    def __init__(self):
        self.chosen = []  # holds selections from all menus
        self.this_menu = None

    def cycle(self):
        """
        Calls run() for each menu in turn.
        :return: the collected user choices for the menus run
        Called by: DigClock.run_clock()
        """
        for m in menu_data.menu_list:
            self.this_menu = Menu(m, self.chosen, menu_data.header,
                                  menu_data.message, menu_data.footer, self.send_choice)
            # read and display menu, get and validate selection
            self.this_menu.run()
        clear_screen()
        for item in self.chosen:  # self.chosen is empty for first menu
            print('Your {}: {}'.format(item[0], item[2]))
        _ = raw_input('\n\nPress \'Enter\' to start clock...')
        # TODO: replace with callback in DigClock?
        return self.chosen  # to DigClock.set_menu_option()

    def send_choice(self, choice):
        """
        Callback handed to Menu object.
        Retrieves the user's menu selection, formatted appropriately
        for the CycleMenus class.
        :param choice: will hold the user's menu selection
        :return: None
        """
        self.chosen.append(choice)


# TODO: prepend '_' to 'private' data member names ?
class Menu(object):
    """
    Class provided: an interactive menu presented to the user.
    The menu shows options (with the default option marked by an
    asterisk) and gets the user's choice.
    Instantiated by CycleMenus().
    """
    def __init__(self, source, chosen, headr, msg, footr, send_choice):
        self.source = source            # a list of options from menu_data.menu_list
        self.chosen = chosen[:]         # the user's selections so far
        self.header = headr             # displayed at the top of the menu
        self.message = msg              # displayed below the header
        self.footer = footr             # displayed by raw_input()
        self.send_choice = send_choice  # callback to CycleMenus()
        self.description = None
        self.entries = [('', '', '')]   # make self.entries 1-indexed
        self.default = None
        self.selection = None
        self.reformatted_selection = None
        self.bad_combinations = menu_data.bad_combinations
        self.err_msg = None

    def run(self):
        """
        Calls subroutines that:
            read and display the current menu
            get and validate the user response
            reformat that response
            send response back to CycleMenus object
        :return: None
        Called by: CycleMenus.cycle()
        """
        self.read()
        self.display()
        self.get_valid_selection()
        self.reformat_selection(self.selection)
        # callback sends reformatted selection back to CycleMenus object
        self.send_choice(self.reformatted_selection)

    def read(self):
        """
        Read the options for the current menu.
        :return: None
        Called by: self.run()
        """
        for ix, item in enumerate(self.source):
            if ix == 0:  # self.source[0] is menu description, e.g., 'text color'
                self.description = item[:]
            else:
                self.entries.append(item[:])
                # item example: ('2', 'BLUE', '\x1b[34m')
                if item[1] and item[1].endswith(' (*)'):
                    # default item example: ('3', 'LIGHT CYAN (*)', '\x1b[96m')
                    self.default = list(item)
                    self.default[1] = self.default[1].rstrip(' ()*')

    def display(self):
        """
        Present the current menu to the user.
        :return: None
        Called by: self.run()
        """
        clear_screen()
        print(self.header + '\n')
        print(self.message + self.description + ':\n')
        for item in self.entries[1:]:
            print('{:2}) {:10}'.format(item[0], item[1]))
        print()
        for item in self.chosen:  # self.chosen is empty for first menu
            print('Your {}: {}'.format(item[0], item[2]))

    def get_valid_selection(self):
        """
        Call subroutines to get and validate a selection from the user
        :return: None
        Called by: self.run()
        """
        while True:  # loop until user makes a valid selection
            self.selection = None
            self.get_selection()
            test_1 = self.validate_selection()
            if not test_1:
                self.print_err_msg()
                continue
            test_2 = self.good_combination()
            if not test_2:
                self.print_err_msg()
                continue
            if test_1 and test_2:  # both tests passed
                break
            else:
                self.err_msg = '\n\nINPUT ERROR'
                self.print_err_msg()

    def get_selection(self):
        """
        Get the user selection.
        :return: None
        Called by: self.run()
        """
        self.selection = raw_input('\n\n' + self.footer + ' ')

    def validate_selection(self):
        """
        Checks that the input string represents an integer in the
        correct range, or is empty.
        :return: True on good input
                 False otherwise
        Called by: self.run()
        """
        menu_len = len(self.entries)
        ret = False
        self.selection = self.selection.strip()
        if self.selection:
            try:
                if 0 < int(self.selection) < menu_len:
                    ret = True
                else:
                    self.err_msg = '\n\nSorry. Value entered is out of range.'
            except ValueError:  # input is not an integer
                self.err_msg = '\n\nPlease input an integer value'
        else:
            ret = True  # empty string is a valid input
        return ret

    def good_combination(self):
        """
        Checks for validity of *combinations* of selections.
        E.g., a blue text color on a blue background will be rejected.
        :return: True if combination of inputs so far is valid
                 False otherwise
        Called by: self.get_valid_selection()
        """
        if not self.selection:  # user simply pressed <Enter>
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
        """
        Get the default option for the current menu.
        :return: The default option as an integer
        Called by: self.good_combination()
        """
        return int(self.default[0])

    def print_err_msg(self):
        """
        Display the current error message and sleep for 2 seconds.
        :return: None
        Called by: self.get_valid_selection()
        """
        print('\033[41m')  # red background
        print(self.err_msg)
        print('\033[40m')  # black background
        print('\033[0m')
        time.sleep(2)

    def reformat_selection(self, selected):
        """
        Reformat selected option as e.g., [text color, CYAN]
        :param selected: a string holding the user's choice, e.g., '3'
                         may be '' to represent the default option
        :return: the reformatted selection
        Called by: self.run()
        """
        if selected:
            # self.description: e.g., 'text color'
            self.reformatted_selection = [self.description]
            for ix, item in enumerate(self.entries[int(selected)]):
                if ix == 1 and item.endswith(' (*)'):
                    # the default item has been selected by its number
                    self.reformatted_selection += [item.rstrip(' ()*')]
                else:
                    # a non-default item has been selected
                    self.reformatted_selection.append(item)
        else:
            # the default item has been selected by pressing <Enter>
            self.reformatted_selection = [self.description] + self.default


if __name__ == '__main__':
    c = CycleMenus()
    c.cycle()
