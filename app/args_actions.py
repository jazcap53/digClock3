import sys
import argparse
import time


class ParseTime(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        # print 'local time is', time.localtime()
        # print 'local time hour is', time.strftime('%H', time.localtime())
        # print 'gm time is', time.gmtime()
        # print 'gm time hour is', time.strftime('%H', time.gmtime())
        # print 'the time zone is', time.timezone
        # print 'daylight is', time.daylight
        # if time.daylight:
        #     print 'the local altzone value is', time.altzone
        # print type(values)
        # print values
        # print 'len(values) is', len(values)
        if len(values) != 8:
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
            except TypeError:
                print('TypeError in ParseTime.__call()')
                sys.exit(1)
        # print '%s %s %s' % (hrs, mins, secs)
        time_zone_secs = time.timezone
        a_day_in_secs = 86400
        if not bad_length and 0 <= hrs <= 23 and 0 <= mins <= 59 and\
                0 <= secs <= 59:
            time_secs = (3600 * hrs + 60 * mins + secs + time_zone_secs)\
                        % a_day_in_secs
        else:
            raise ValueError
        # print time_secs
        setattr(namespace, self.dest, time_secs)  # set namespace.t to time_secs
        # print namespace
