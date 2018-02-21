#!/usr/bin/env python3

class SequenceNumberStats(object):

    def __init__(self):
        pass

    def feed(self, seq_no):
        pass

    def loss(self):
        pass



if __name__ == '__main__':

    s = SequenceNumberStats()
    s.feed(1)
    s.feed(2)
    s.feed(3)
    print(s)
