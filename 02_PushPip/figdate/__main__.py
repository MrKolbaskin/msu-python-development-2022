import time
import locale
import pyfiglet
import sys

locale.setlocale(locale.LC_ALL, 'ru_RU')

def date(format="%Y %d %b, %A", font="graceful"):
    return pyfiglet.figlet_format(time.strftime(format), font=font)

if __name__ == "__main__":
    print(date(*sys.argv[1:]))

