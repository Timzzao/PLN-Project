import sys
import csv

from util import Util
from actionPolarity import ActionPolarity
from direction import Direction
from eventPolarity import EventPolarity
from overallPolarity import OverallPolarity
from tense import Tense

from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk import sent_tokenize

dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')

def getSentences(fileName):
    with open(fileName) as csv_file:
        result = []
        csv_reader = csv.reader(csv_file, delimiter='|')
        isHeader = True
        for row in csv_reader:
            if isHeader:
                isHeader = False
            else:
                result.append(row[40])
        return result

def getDepParsed(sentence):
    parse, =  dep_parser.raw_parse(sentence)
    return parse
        
if __name__ == '__main__':
    fileName = sys.argv[1]
    content  = getSentences(fileName)
    ranking  = []

    util = Util()
    tense = Tense()
    direction = Direction()
    eventPolarity = EventPolarity()
    overallPolarity = OverallPolarity()

    j = 0

    
    for sent in content:
        vTense = None
        vDirection = None
        vOvPol = None
        vEvPol = None        

        for (i, sentence) in enumerate(sent_tokenize(sent)):
            if i == 0:
                depParsed        = getDepParsed(sentence)

                tokens           = util.getTokens(text=sentence)
                tagged           = util.getTagged(tokens)
                vTense           = tense.getTense(tagged)
                vOvPol           = overallPolarity.calculateOverallPolarity(sent)
                vDirection       = direction.getDirection(depParsed)
                vEvPol           = eventPolarity.calculateEventPolarity(depParsed)

                ranking.append((vDirection, vTense, vOvPol, vEvPol))

    emos = util.analyseEmotion(ranking)

    stats = {}

    for i in range(len(emos)):
        if emos[i] not in stats.keys():
            stats[emos[i]] = 0
        stats[emos[i]] += 1

    for key, value in stats.items():
        print(f"{key}: {value}")
