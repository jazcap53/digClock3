import unittest

from app.menu import Menu
from app.menu_data import menu_list, header, message, footer


class TestMenu(unittest.TestCase):

    def setUp(self):
        self.my_menu = Menu(menu_list[0], [], header, message, footer)

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
        self.my_menu.update_chosen('7')
        self.assertEqual(self.my_menu.chosen[0][1], self.my_menu.default[0])

    def test_enter_nondefault_values_number_selects_nondefault_value(self):
        self.my_menu.read()
        self.my_menu.update_chosen('15')
        self.assertEqual(self.my_menu.chosen[0][1], '15')

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

    def test_bad_combination_of_choices_is_rejected(self):
        self.my_menu.read()
        self.my_menu.update_chosen('14')
        self.my_menu = Menu(menu_list[1], [], header, message, footer)
        self.my_menu.read()
        self.my_menu.update_chosen('8')
        print self.my_menu.chosen
        self.assertFalse(self.my_menu.good_combination())
