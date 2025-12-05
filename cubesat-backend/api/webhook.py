import requests

from config import slack_webhook_url


def send_webhook_message(markdown_text: str):
    # Only send webhook message to Slack if webhook is defined
    if slack_webhook_url:
        requests.post(slack_webhook_url, json={
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": markdown_text,
                    }
                }
            ]
        })