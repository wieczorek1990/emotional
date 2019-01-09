import random


MOOD_POSITIVE = 'positive'
MOOD_NEUTRAL= 'neutral'
MOOD_NEGATIVE = 'negative'

RESPONSES_POSITIVE = [
    'Positive about that.',
    'It\'s OK to say that.',
    'I\'m OK with that.',
    'You\'re right.',
    'Cool.'
]
RESPONSES_NEUTRAL = [
    'Neutral about that.',
    'If you say so.',
    'I don\'t mind.',
    'Sure.',
    'Naturally.'
]
RESPONSES_NEGATIVE = [
    'Negative about that.',
    'I don\'t like what you say.',
    'Please don\'t say that.',
    'You\'r thinking is wrong.',
    'Please change you\'r mind.'
]


class Chatbot:
    @staticmethod
    def get_response(mood):
        response_number = random.randint(0, 4)
        if mood == MOOD_POSITIVE:
            return RESPONSES_POSITIVE[response_number]
        elif mood == MOOD_NEUTRAL:
            return RESPONSES_NEUTRAL[response_number]
        else:
            return MOOD_NEGATIVE[response_number]


if __name__ == '__main__':
    import sys
    mood = sys.argv[1]
    print(Chatbot.get_response(mood))
