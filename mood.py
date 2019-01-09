import json
import os

from watson_developer_cloud import ToneAnalyzerV3

from chatbot import MOOD_POSITIVE, MOOD_NEUTRAL, MOOD_NEGATIVE


TONE_POSITIVE = {'joy'}
TONE_NEGATIVE = {'anger', 'fear', 'sadness'}


class Mood:
    API_KEY = os.environ.get('IAM_API_KEY')
    API_URL = 'https://gateway-lon.watsonplatform.net/tone-analyzer/api'
    TONE_THRESHOLD = 0.75

    def __init__(self):
        self.tone_analyzer = ToneAnalyzerV3(
            version='2017-09-21',
            iam_apikey=self.API_KEY,
            url=self.API_URL)

    def get(self, text):
        analysis = self.tone_analyzer.tone({'text': text},
                                           'application/json').get_result()

        tones = []
        for tone in analysis['document_tone']['tones']:
            if tone['score'] > self.TONE_THRESHOLD:
                tones.append(tone)

        for tone in tones:
            tone_id = tone['tone_id']
            if tone_id in TONE_POSITIVE:
                return MOOD_POSITIVE
            elif tone_id in TONE_NEGATIVE:
                return MOOD_NEGATIVE

        return MOOD_NEUTRAL


if __name__ == '__main__':
    import sys
    print(Mood().get(sys.argv[1]))
