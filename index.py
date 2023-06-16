
"""
"""

from irc import *

import sys

class _():

    def __init__(self):
        pass

if __name__ == '__main__':
    if len(sys.argv) == 1:
        nick = 'alexandrogonsan'
    else:
        nick = sys.argv[1]
    irc = IRCClient('irc.db', nick)
    irc.db_cursor.execute("SELECT DISTINCT server, channel FROM channels")
    rows = irc.db_cursor.fetchall()
    for row in rows:
        server, channel = row
        irc.connect(server, 6667)
        irc.join_channel(channel)
    def _(tag, func, args=[]):
        with open(tag) as f: all = f.read().split('\n')
        for each in all:
            aux =  [each] + args
            func(*aux)
    evts = [
        ['servers', 'channels'],
        [irc.connect, irc.join_channel],
        [[6667], []]
    ]
    for tag, func, args in zip(*evts):
        _(tag, func, args)
    with open('channels') as f: all = f.read().split('\n')
    for each in all:
        irc.join_channel(each)
    irc.cmdloop('Iniciando prompt de comando...')