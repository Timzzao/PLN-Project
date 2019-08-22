import sys

from util import Util
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class OverallPolarity:
    def calculateOverallPolarity(self, tokens):
        sid = SentimentIntensityAnalyzer()
        polarity = sid.polarity_scores(tokens)
        if polarity['compound'] > 0:
            return Util.OvSentPol.POSITIVE
        elif polarity['compound'] < 0:
            return Util.OvSentPol.NEGATIVE
        else:
            return Util.OvSentPol.NEUTRAL