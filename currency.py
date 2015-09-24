'''
Get the Exchange Rates on your terminal!

It  uses some code from the Python Cookbook
'''

import sys
import json
import argparse

from urllib import urlopen


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

myArr = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]

#following from Python cookbook, #475186

def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False

has_colours = has_colours(sys.stdout)

def printout(text, colour=WHITE):
    if has_colours:
        seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
        sys.stdout.write(seq)
    else:
        sys.stdout.write(text)

#END python cookbook

def print_info_amount(currency_from, currency_to, num_from, num_to):
    sys.stdout.write('%.2f in ' % round(num_from,2))
    printout('%s' % currency_from, RED)
    sys.stdout.write(' is exquivalent to %.2f in ' % round(num_to,2))
    printout('%s\n' % currency_to, GREEN)

def print_info_no_amount(currency_from, currency_to, rate):
    sys.stdout.write('The rate from ')
    printout(currency_from, RED)
    sys.stdout.write(' to ')
    printout(currency_to, GREEN)
    sys.stdout.write(' is ')
    printout('%f\n' % rate,YELLOW)

def get_info(currency_from, currency_to, amount):
    url = 'https://currency-api.appspot.com/api/%s/%s.json' % (currency_from, currency_to)
    content = json.loads(urlopen(url).read())
    if content['message']:
        print 'API returned error: %s' % content['message']
    else:
        curTo = content['source']
        curFrom = content['target']
        rate = content['rate']
        if not amount:
            print_info_no_amount(currency_from, currency_to, rate)
        else:
            print_info_amount(currency_from, currency_to, amount, amount * float(rate))
def run_main(currency_from, currency_to, amount=None):
    get_info(currency_to, currency_from, amount);

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Terminal Currency')
    parser.add_argument('-t', '--tocur', help='Currency _TO_', required=True, type=str)
    parser.add_argument('-f', '--fromcur', help='Currency _FROM_', required=True, type=str)
    parser.add_argument('-a', '--amount', help='Amount', required=False, type=float)
    args = parser.parse_args()
    if args.amount:
        run_main(args.fromcur, args.tocur, args.amount)
    else:
        run_main(args.tocur, args.fromcur)
