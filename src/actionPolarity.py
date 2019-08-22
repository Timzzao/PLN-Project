import sys

from util import Util

class ActionPolarity:
    def getActionSent(self, depSentence):
        subj = None
        result = ''
        for governor, dep, nsubj in depSentence.triples():
            if dep == 'nsubj':
                subj = nsubj
                break
        if nsubj:
            for governor, dep, word in depSentence.triples():
                if governor == subj:
                    result += " "
                    result += word[0]
                if "VB" in (governor[1]) and governor[0] not in result:
                    result += " "
                    result += governor[0]
        return result

    def calculateActionPolarity(self, depSentence):
        util = Util()

        polarity = util.swn_polarity(text=self.getActionSent(depSentence))

        if polarity > 0:
            return Util.ActPol.POSITIVE
        elif polarity < 0:
            return Util.ActPol.NEGATIVE
        else:
            return Util.ActPol.NEUTRAL