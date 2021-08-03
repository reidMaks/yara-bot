from unittest import TestCase
import bot


class Test(TestCase):
    def test_eat_time_switcher(self):

        good_suite = {
            '00:00:00': '🙂',
            '00:59:59': '🙂',
            '01:00:00': '🤔',
            '01:29:59': '🤔',
            '01:30:00': '😕',
            '01:59:59': '😕',
            '02:00:00': '😡',
            '02:59:59': '😡',
            '03:00:00': '🤬',
            '58:59:59': '🤬',
        }

        bad_suite = ['-58:59:59', 'some string', None, False, '::', 6588]

        for param, result in good_suite.items():
            self.assertEqual(bot.eat_time_switcher(param), result)
        for param in bad_suite:
            with self.assertRaises(AssertionError) as cm:
                bot.eat_time_switcher(param)
            expt = cm.exception
            self.assertTrue(type(expt) == AssertionError)
