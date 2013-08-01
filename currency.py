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

def printInfo2(name1,name2,rate):
    sys.stdout.write('The rate from ')
    printout(name1,RED)
    sys.stdout.write(' to ')
    printout(name2,GREEN)
    sys.stdout.write(' is ')
    printout(str(rate)+'\n',YELLOW)

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
    if amount1 == None:
        printInfo2(CODES[curFrom],CODES[curTo],rate)
    else:
        printInfo(CODES[curFrom],CODES[curTo],amount1,getAmount2(rate,amount1))

def runMain(cur1,cur2,amount=None):
    getInfo(cur1,cur2,amount)

if __name__ == "__main__":
    try: 
	cur1 = sys.argv[1].upper()
	cur2 = sys.argv[2].upper()
        amount=0
	try:
            amount = sys.argv[3]
            runMain(cur1,cur2,amount)
        except IndexError:
            runMain(cur1,cur2)
    except IndexError:
	print 'usage: python ' + sys.argv[0] + ' <currency> <currency> <OPTIONS: amount>'
