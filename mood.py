import os

from watson_developer_cloud import ToneAnalyzerV3


MOOD_POSITIVE = 'positive'
MOOD_NEUTRAL= 'neutral'
MOOD_NEGATIVE = 'negative'
MOOD_MAPPING = {MOOD_POSITIVE: 1, MOOD_NEUTRAL: 0, MOOD_NEGATIVE: -1}
MOOD_REVERSE_MAPPING = {1: MOOD_POSITIVE, 0: MOOD_NEUTRAL, -1: MOOD_NEGATIVE}
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

    @staticmethod
    def get_next(current_mood, next_mood):
        current_index = MOOD_MAPPING[current_mood]
        next_index = MOOD_MAPPING[next_mood]
        index = current_index + next_index
        if index < -1:
            index = -1
        elif index > 1:
            index = 1
        return MOOD_REVERSE_MAPPING[index]


if __name__ == '__main__':
    import sys
    print(Mood().get(sys.argv[1]))
