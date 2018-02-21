#!/usr/bin/env python3

import bisect

THRESHOLD_GC = 64

class SequenceNumberStats(object):

    def __init__(self):
        self.db = []
        self.reset()

    def feed(self, seq_no):
        if seq_no in self.db:
            self._duplicates += 1
            return
        if len(self.db) > 0 and self.db[-1] + 1 != seq_no:
            # not the expected packet
            self._reordering += 1
        bisect.insort(self.db, seq_no)
        self._update()

    def missing(self):
        return self._missing + self._missing_outdated

    def duplicates(self):
        return self._duplicates

    def reordering(self):
        return self._reordering

    def reset(self):
        self._missing_outdated = 0
        self._missing = 0
        self._duplicates = 0
        self._reordering = 0

    def _update(self):
        if len(self.db) < THRESHOLD_GC or len(self.db) % 2 != 0:
            # only allowed to gc if div by 2 possible
            self._missing = self._calc_missing(self.db)
            return
        to_be_removed = self.db[:len(self.db) // 2]
        self.db = self.db[len(self.db) // 2:]
        self._missing_outdated += self._calc_missing(to_be_removed)
        self._missing = self._calc_missing(self.db)

    def _calc_missing(self, array):
        if len(array) <= 1:
            return 0
        cnt_diff = (array[-1] - array[0]) + 1
        return abs(cnt_diff - len(array))



if __name__ == '__main__':

    s = SequenceNumberStats()
    s.feed(1)
    s.feed(1)
    s.feed(1)

    s.feed(2)
    s.feed(3)

    s.feed(7)
    s.feed(6)
    s.feed(5)
    s.feed(4)

    s.feed(8)
    # 9 missing
    s.feed(10)

    for i in range(11, 3000):
        if i == 25:
            continue
        if i == 23:
            continue
        s.feed(i)

    print(s.db)

    print("missing: " + str(s.missing()))
    print("duplicates: " + str(s.duplicates()))
    print("reordering: " + str(s.reordering()))
