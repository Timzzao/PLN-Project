import sys

from util import Util

class EventPolarity:
    def getEventSent(self, depSentence):
        obj = None
        result = ''
        for governor, dep, dobj in depSentence.triples():
            if dep == 'dobj' or 'mod' in dep:
                obj = dobj
                break
        if obj:
            for word in obj:
                result += " "
                result += word
            for governor, dep, word in depSentence.triples():
                if governor == obj:
                    result += " "
                    result += word[0]
                if "VB" in [governor[1]] and governor[0] not in result:
                    result += " "
                    result += governor[0]
        return result

    def calculateEventPolarity(self, depSentence):
        util = Util()

        polarity = util.swn_polarity(text=self.getEventSent(depSentence))

        if polarity > 0:
            return Util.EvtPol.POSITIVE
        elif polarity < 0:
            return Util.EvtPol.NEGATIVE
        else:
            return Util.EvtPol.NEUTRAL