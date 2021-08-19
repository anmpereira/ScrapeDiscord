import requests
import json
import secretfiles


def retrieve_messages(channel_id, authorization):
    headers = {
        'authorization': authorization
    }

    r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers)
    jsonn = json.loads(r.text)
    for value in jsonn:
        print(value['timestamp'], value['content'], '\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    retrieve_messages(secretfiles.channel_id, secretfiles.authorization)
