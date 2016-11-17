import sys
import argparse
import time


class ParseTime(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) != 8:  # pragma: no cover
            hrs = 0
            mins = 0
            secs = 0
            bad_length = True
        else:
            try:
                hrs = int(values[0:2])
                mins = int(values[3:5])
                secs = int(values[6:])
                bad_length = False
            except TypeError:  # pragma: no cover
                print('TypeError in ParseTime.__call()')
                raise
        time_zone_secs = time.timezone
        a_day_in_secs = 86400
        if not bad_length and 0 <= hrs <= 23 and 0 <= mins <= 59 and\
                0 <= secs <= 59:
            time_secs = (3600 * hrs + 60 * mins + secs + time_zone_secs)\
                        % a_day_in_secs
        else:  # pragma: no cover
            raise ValueError
        setattr(namespace, self.dest, time_secs)  # set namespace.t to time_secs
