from enum import Enum

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn 
from nltk import word_tokenize, pos_tag

class Util:

    lemmatizer = WordNetLemmatizer()

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

    def penn_to_wn(self, tag):
        if tag.startswith('J'):
            return wn.ADJ
        elif tag.startswith('N'):
            return wn.NOUN
        elif tag.startswith('R'):
            return wn.ADV
        elif tag.startswith('V'):
            return wn.VERB
        return None

    def getTokens(self, text):
        return word_tokenize(text)

    def getTagged(self, text):
        return pos_tag(text)

    def swn_polarity(self, text):
        sentiment = 0.0
        tokens = 0

        tagged_sentence = pos_tag(word_tokenize(text))

        for word, tag in tagged_sentence:
            wn_tag = self.penn_to_wn(tag)

            if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                continue

            lemma = self.lemmatizer.lemmatize(word, pos=wn_tag)
            if not lemma:
                continue
            
            synsets = wn.synsets(lemma, pos=wn_tag)
            if not synsets:
                continue
            
            synset = synsets[0]
            swm_synset = swn.senti_synset(synset.name())

            sentiment += swm_synset.pos_score() - swm_synset.neg_score()
            tokens += 1
        
        if not tokens:
            return 0
        
        if sentiment >= 0:
            return 1

        return 0
    
    def analyseEmotion(self, variablesTable):
        emotionResult = []
        
        for direction, tense, polarity, event in variablesTable:
            if direction == Util.Direction.SELF:
                if tense == Util.Tense.FUTURE:
                    if polarity == Util.OvSentPol.NEGATIVE:
                        if event == Util.EvtPol.NEGATIVE or event == Util.EvtPol.NEUTRAL:
                            emotionResult.append(Util.EmotionOfSent.FEAR)
                        else:
                            emotionResult.append(Util.EmotionOfSent.ITD)
                    elif polarity == Util.OvSentPol.POSITIVE:
                        if event == Util.EvtPol.POSITIVE or event == Util.EvtPol.NEUTRAL:
                            emotionResult.append(Util.EmotionOfSent.JOY)
                        else:
                            emotionResult.append(Util.EmotionOfSent.ITD)
                    else:
                        emotionResult.append(Util.EmotionOfSent.ITD)
                elif tense == Util.Tense.PRESENT:
                    if polarity == Util.OvSentPol.NEGATIVE:
                        if event == Util.EvtPol.NEGATIVE or event == Util.EvtPol.NEUTRAL:
                            emotionResult.append(Util.EmotionOfSent.SADNESS)
                        else:
                            emotionResult.append(Util.EmotionOfSent.ITD)
                    elif polarity == Util.OvSentPol.POSITIVE:
                        if event == Util.EvtPol.POSITIVE or event == Util.EvtPol.NEUTRAL:
                            emotionResult.append(Util.EmotionOfSent.JOY)
                        else:
                            emotionResult.append(Util.EmotionOfSent.ITD)
                    else:
                        emotionResult.append(Util.EmotionOfSent.ITD)
                else:
                    if polarity == Util.OvSentPol.NEGATIVE:
                        if event == Util.EvtPol.NEGATIVE or event == Util.EvtPol.NEUTRAL:
                            emotionResult.append(Util.EmotionOfSent.FEAR)
                        else:
                            emotionResult.append(Util.EmotionOfSent.SADNESS)
                    elif polarity == Util.OvSentPol.POSITIVE:
                            emotionResult.append(Util.EmotionOfSent.JOY)
                    else:
                        if event == Util.EvtPol.NEGATIVE:
                            emotionResult.append(Util.EmotionOfSent.SADNESS)
                        elif event == Util.EvtPol.POSITIVE:
                            emotionResult.append(Util.EmotionOfSent.JOY)
                        else:
                            emotionResult.append(Util.EmotionOfSent.ITD)
            else:
                if polarity == Util.OvSentPol.NEGATIVE:
                    if event == Util.EvtPol.NEGATIVE or event == Util.EvtPol.NEUTRAL:
                        emotionResult.append(Util.EmotionOfSent.SADNESS)
                    else:
                        emotionResult.append(Util.EmotionOfSent.DISGUST)
                elif polarity == Util.OvSentPol.POSITIVE:
                    emotionResult.append(Util.EmotionOfSent.JOY)
                else:
                    emotionResult.append(Util.EmotionOfSent.ANGER)
        return emotionResult
                

        