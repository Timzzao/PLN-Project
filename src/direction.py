import sys

from util import Util

class Direction:
    def getDirection(self, depSentence):
        for governor, dep, dependent in depSentence.triples():
            if dep == 'nsubj':
                if 'i' or 'we' in dependent[0].lower():
                    return Util.Direction.SELF
                else:
                    return Util.Direction.OTHER
        return Util.Direction.OTHER