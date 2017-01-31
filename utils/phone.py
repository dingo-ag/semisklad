import csv
import re
import os
from semisklad.settings.base import BASE_DIR

csv_path = os.path.join(BASE_DIR, 'utils/phone_codes.csv')


class PhoneNormalize:
    def __init__(self, number=None):
        if number is None:
            number = ''
        if not isinstance(number, str):
            raise TypeError('Class takes only string')
        self.number = number
        self.district = None

    @staticmethod
    def district_define(code):
        with open(csv_path) as codes:
            reader = csv.DictReader(codes)
            for row in reader:
                if row['code'] == code:
                    return row['operator_region']

    def normalize_phone_number(self):
        district_code = ''

        def num_format(n):
            nonlocal district_code
            district_code = n[3:5]
            return '+{}({}){}-{}-{}'.format(n[:2], n[2:5], n[5:8], n[8:10], n[10:])

        try:
            number = str(self.number)
        except (ValueError, TypeError, UnicodeError, OverflowError):
            return None
        p = r'\D'
        rn = re.sub(p, '', number)
        if len(rn) == 12 and rn.startswith('3'):
            raw_number = num_format(rn)
        elif len(rn) == 11 and rn.startswith('8'):
            rn = '3' + rn
            raw_number = num_format(rn)
        elif len(rn) == 10 and rn.startswith('0'):
            rn = '38' + rn
            raw_number = num_format(rn)
        else:
            raw_number = rn
        if district_code:
            self.district = self.district_define(district_code)
        return raw_number


if __name__ == '__main__':
    c = PhoneNormalize('80442565454')
    d = c.normalize_phone_number()
    print(c.district)
    assert (PhoneNormalize('80442565454').normalize_phone_number()) == '+38(044)256-54-54'
    assert (PhoneNormalize('+38(096)972-62-58').normalize_phone_number()) == '+38(096)972-62-58'
