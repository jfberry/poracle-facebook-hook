# Poracle (Discord Webhook) to Facebook Messenger

Listens on a port to discord webhook style events and gates them to
Facebook Messenger Groups

1. Find the messenger group ID by looking at the facebook URL in messenger eg: `https://www.messenger.com/t/1559473960429236`
1. Use this number for configuring poracle, eg:
    1. `/channel add namehundos http://127.0.0.1:8111/1559473960429236`
    1. `/area add mycity namehundos`
    1. `/track everything iv100 namehundos`
    
It doesn't take everything from the webhook, but rather just the title, description, and image.
It will post a facebook pinned location if it sees a location field. In Poracle I do:

```
"location": {
    "latitude": "{{latitude}}",
    "longitude": "{{longitude}}"
},
```

at the same level as the embed.

## Known issues

I think the code should probably be reading from the embeds array and this only
works because Poracle sends the embeds twice, probably incorrectly.
If anyone can confirm this from other webhook sources I'll fix it (or send me a pull request)

No logging, so best run it under something like pm2 that will capture that

## Installation

Needs Python 3.7+

### Config
`cp config.ini.example config.ini`

Fill in the config fields. 

### Python requirements
`pip install -r requirements.txt`

## Running
`python3 main.py`