import sys
import nltk
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.wsd import lesk
from nltk.corpus import sentiwordnet as swn
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv
from enum import Enum

class Direction(Enum):
    SELF = 1
    OTHER = 2

class Tense(Enum):
    PRESENT = 1
    PAST = 2
    FUTURE = 3

class OvSentPol(Enum):
    POSITIVE = 1
    NEUTRAL = 2
    NEGATIVE = 3

class EvtPol(Enum):
    POSITIVE = 1
    NEUTRAL = 2
    NEGATIVE = 3

class ActPol(Enum):
    POSITIVE = 1
    NEUTRAL = 2
    NEGATIVE = 3

class EmotionOfSent(Enum):
    JOY = 1
    FEAR = 2
    ANGER = 3
    SADNESS = 4
    DISGUST = 5
    ITD = 6

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

def getWSD(tokens):
    result = []
    for word in tokens:
        result.append(lesk(tokens, word))
    return result

def getDepParsed(sentence):
    parse, =  dep_parser.raw_parse(sentence)
    return parse

def filterSent(sentence):
    stopWords = set(nltk.corpus.stopwords.words('english')) 
    return [w for w in sentence if not w in stopWords]

def getDirection(depSentence):
    for governor, dep, dependent in depSentence.triples():
        if(dep == 'nsubj'):
            if 'i' or 'we' in dependent[0].lower():
                return Direction.SELF
            else:
                return Direction.OTHER
    return Direction.OTHER

def getTense(tagWords):
    for word, pos in tagWords:
        if "VB" in pos:
            if pos in ["VBD", "VBN"]:
                return Tense.PAST
            elif pos in ["VBG"]:
                return Tense.FUTURE
            else:
                return Tense.PRESENT

def calculateOverallPolarity(tokens):
    sid = SentimentIntensityAnalyzer()
    polarity = sid.polarity_scores(tokens)
    if polarity['compound'] > 0:
        return OvSentPol.POSITIVE
    elif polarity['compound'] < 0:
        return OvSentPol.NEGATIVE
    else:
        return OvSentPol.NEUTRAL

def getEventSent(depSentence):
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

def calculateEventPolarity(depSentence):
    sentence = getEventSent(depSentence)
    sid = SentimentIntensityAnalyzer()
    polarity = sid.polarity_scores(sentence)
    if polarity['compound'] > 0:
        return EvtPol.POSITIVE
    elif polarity['compound'] < 0:
        return EvtPol.NEGATIVE
    else:
        return EvtPol.NEUTRAL

def analyseEmotion(variablesTable):
    emotionResult = []
    print(variablesTable)
    for direction, tense, polarity, event in variablesTable:
        if direction == Direction.SELF:
            if tense == Tense.FUTURE:
                if polarity == OvSentPol.NEGATIVE:
                    if event == EvtPol.NEGATIVE or event == EvtPol.NEUTRAL:
                        emotionResult.append(EmotionOfSent.FEAR)
                    else:
                        emotionResult.append(EmotionOfSent.ITD)
                elif polarity == OvSentPol.POSITIVE:
                    if event == EvtPol.POSITIVE or event == EvtPol.NEUTRAL:
                        emotionResult.append(EmotionOfSent.JOY)
                    else:
                        emotionResult.append(EmotionOfSent.ITD)
                else:
                    emotionResult.append(EmotionOfSent.ITD)
            elif tense == Tense.PRESENT:
                if polarity == OvSentPol.NEGATIVE:
                    if event == EvtPol.NEGATIVE or event == EvtPol.NEUTRAL:
                        emotionResult.append(EmotionOfSent.SADNESS)
                    else:
                        emotionResult.append(EmotionOfSent.ITD)
                elif polarity == OvSentPol.POSITIVE:
                    if event == EvtPol.POSITIVE or event == EvtPol.NEUTRAL:
                        emotionResult.append(EmotionOfSent.JOY)
                    else:
                        emotionResult.append(EmotionOfSent.ITD)
                else:
                    emotionResult.append(EmotionOfSent.ITD)
            else:
                if polarity == OvSentPol.NEGATIVE:
                    if event == EvtPol.NEGATIVE or event == EvtPol.NEUTRAL:
                        emotionResult.append(EmotionOfSent.FEAR)
                    else:
                        emotionResult.append(EmotionOfSent.SADNESS)
                elif polarity == OvSentPol.POSITIVE:
                        emotionResult.append(EmotionOfSent.JOY)
                else:
                    emotionResult.append(EmotionOfSent.ITD)
        else:
            if polarity == OvSentPol.NEGATIVE:
                if event == EvtPol.NEGATIVE or event == EvtPol.NEUTRAL:
                    emotionResult.append(EmotionOfSent.SADNESS)
                else:
                    emotionResult.append(EmotionOfSent.DISGUST)
            elif polarity == OvSentPol.POSITIVE:
                emotionResult.append(EmotionOfSent.JOY)
            else:
                emotionResult.append(EmotionOfSent.ANGER)
    return emotionResult
                        
if __name__ == '__main__':
    fileName = sys.argv[1]
    content  = input("Phrase:")
    ranking  = []

    

    for (i, sentence) in enumerate(nltk.sent_tokenize(content)):
        tokens          = nltk.word_tokenize(sentence)
        tagged          = nltk.pos_tag(tokens)
        tense           = getTense(tagged)
        ovPol           = calculateOverallPolarity(content)
        depParsed       = getDepParsed(sentence)
        direction       = getDirection(depParsed)
        evPol           = calculateEventPolarity(depParsed)

    ranking.append((direction, tense, ovPol, evPol))

    emos = analyseEmotion(ranking)

    for i in range(len(emos)):
        print(str(emos[i]))