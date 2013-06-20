'''
Get the Exchange Rates on your terminal!

It  uses some code from the Python Cookbook
'''

import sys,json,re
from curCodes import CODES
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
def getAmount2(rate,amount):
	return  round(rate*float(amount), 2)

def printInfo(name1,name2,amount1,amount2):
	sys.stdout.write(str(amount1) + ' ')
 	printout(name1+'(s)',RED)
 	sys.stdout.write(' is exquivalent to ' + str(amount2) + ' ')
 	printout(name2+'(s)\n',GREEN)

def getInfo(currency1,currency2,amount1):
	url = 'http://rate-exchange.appspot.com/currency?from=%s&to=%s' % (currency1,currency2)
        try:
            content = json.loads(urlopen(url).read())
            curTo = content['to']
            curFrom = content['from']
            rate = content['rate']
	except (KeyError,ValueError):
            print 'One of the currencies is not in the database...'
            sys.exit(0)
        printInfo(CODES[curFrom],CODES[curTo],amount1,getAmount2(rate,amount1))

try: 
	amount1 = sys.argv[1]
	cur1 = sys.argv[2].upper()
	cur2 = sys.argv[3].upper()
	getInfo(cur1,cur2,amount1)
except IndexError:
	print 'usage: python ' + sys.argv[0] + ' <amount> <currency> <currency>'
