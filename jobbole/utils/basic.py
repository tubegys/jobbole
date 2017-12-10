import re
import datetime


def get_num(value):
    return value


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


def strdate_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return str(create_date)


if __name__ == '__main__':
    print(date_convert('\r\n\r\n            2017/10/28 ·  '))