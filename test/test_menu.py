import unittest
import sys
import os

from app.menu import Menu, CycleMenus
from app.menu_data import menu_list, header, message, footer
import app.menu


# TODO: examine all tests ?

# TODO: write more tests if necessary
class MenuTest(unittest.TestCase):

    def setUp(self):
        self.my_cycle_menus = CycleMenus()
        self.my_menu = Menu(menu_list[0], [], header, message, footer, self.my_cycle_menus.send_choice)
        self.old_stdout = sys.stdout
        f = open(os.devnull, 'w')
        sys.stdout = f

    def tearDown(self):
        sys.stdout = self.old_stdout

    def test_enter_blank_line_is_valid_selection(self):
        self.my_menu.read()
        self. my_menu.selection = ''
        t_1 = self.my_menu.validate_selection()
        t_2 = self.my_menu.good_combination()
        self.assertTrue(t_1 and t_2)

    def test_enter_blank_line_selects_default_value(self):
        self.my_menu.read()
        self.my_menu.selection = ''
        cur_dflt = self.my_menu.get_current_default()
        self.assertEqual(cur_dflt, 7)

    def test_enter_default_values_number_selects_default_value(self):
        self.my_menu.read()
        self.my_menu.reformat_selection('7')
        self.my_menu.send_choice(self.my_menu.reformatted_selection)
        self.assertEqual(self.my_cycle_menus.chosen[0][1], self.my_menu.default[0])

    def test_enter_nondefault_values_number_selects_nondefault_value(self):
        self.my_menu.read()
        self.my_menu.reformat_selection('15')
        self.my_menu.send_choice(self.my_menu.reformatted_selection)
        self.assertEqual(self.my_cycle_menus.chosen[0][1], '15')

    def test_menu_does_not_accept_out_of_range_value(self):
        self.my_menu.read()
        self.my_menu.selection = '16\n'
        is_valid = self.my_menu.validate_selection()
        self.assertFalse(is_valid)

    def test_out_of_range_value_gives_correct_error_message(self):
        self.my_menu.read()
        self.my_menu.selection = '16\n'
        self.my_menu.validate_selection()
        self.assertEqual(self.my_menu.err_msg, '\n\nSorry. Value entered is out of range.')

    def test_menu_does_not_accept_non_integer_value(self):
        self.my_menu.read()
        self.my_menu.selection = 'y\n'
        is_valid = self.my_menu.validate_selection()
        self.assertFalse(is_valid)

    def test_non_integer_value_gives_correct_error_message(self):
        self.my_menu.read()
        self.my_menu.selection = 'y\n'
        self.my_menu.validate_selection()
        self.assertEqual(self.my_menu.err_msg, '\n\nPlease input an integer value')


# TODO: write more tests if necessary
class CycleMenusTest(unittest.TestCase):

    def setUp(self):
        self.old_stdout = sys.stdout
        f = open(os.devnull, 'w')
        sys.stdout = f
        self.my_cycle_menus = CycleMenus()
        app.menu.raw_input = lambda _: '5'
        self.my_cycle_menus.this_menu = Menu(menu_list[0], self.my_cycle_menus.chosen,
                                             header, message, footer, self.my_cycle_menus.send_choice)
        self.my_cycle_menus.this_menu.run()

    def tearDown(self):
        sys.stdout = self.old_stdout

    def test_invalid_selection_combination_is_caught(self):
        app.menu.raw_input = lambda _: '4'
        self.my_cycle_menus.this_menu = Menu(menu_list[1], self.my_cycle_menus.chosen,
                                             header, message, footer, self.my_cycle_menus.send_choice)
        self.my_cycle_menus.this_menu.read()
        self.my_cycle_menus.this_menu.get_selection()
        self.my_cycle_menus.this_menu.validate_selection()
        self.assertFalse(self.my_cycle_menus.this_menu.good_combination())
