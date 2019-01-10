emotional
=========

Emotional chatbot.

## Usage

Please provide the environment variables for those commands.

Installing requirements:

```bash
pip3 install -r requirements.txt
```

Starting server:

```bash
IAM_API_KEY= FB_PAGE_TOKEN= FB_VERIFY_TOKEN= FLASK_APP=server.py flask run -h 0.0.0.0 -p 80
```

Mood testing:

```bash
IAM_API_KEY= python3 mood.py 'I feel great.'
positive
IAM_API_KEY= python3 mood.py 'I feel very bad about this. I feel great.'
neutral
IAM_API_KEY= python3 mood.py 'I feel very bad about this.'
negative
```

## Time spent

### Day 1.

9:08-11.48

13:19-15:06

15:39-18:54

### Day 2.

9:42-
