import sys

from util import Util

class Tense:
    def getTense(self, tagWords):
        for word, pos in tagWords:
            if "VB" in pos:
                if pos in ["VBD", "VBN"]:
                    return Util.Tense.PAST
                elif pos in ["VBG"]:
                    return Util.Tense.FUTURE
                else:
                    return Util.Tense.PRESENT