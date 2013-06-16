#!/bin/bash
MYDIR=~/terminal-currency/currency.py
if [ $# -ne 3 ]; then
    python ${MYDIR}
else
    python ${MYDIR} $1 $2 $3
fi
