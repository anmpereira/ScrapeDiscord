""" Copyright (C) 2020  André Pereira
"""

import requests
import json
import datetime
import analysistools
import secretfiles


def order_x_y(x, y):
    """
    Returns list x ordered according to the sorted y

    :param x: list
    :param y: list
    :return: list
    """
    return [x for (y, x) in sorted(zip(y, x), key=lambda pair: pair[0])]


def retrieve_messages(channel_id, authorization):
    """
    Returns a list with timestamp and content of message that was posted on the discord channel

    :param channel_id: string of digits identifying the target channel
    :param authorization: string token of authorization (OAUTH2?)
    :return: list of dicts
    """
    headers = {
        'authorization': authorization
    }

    r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers)
    jsonn = json.loads(r.text)

    return [{'timestamp': value['timestamp'], 'content': value['content']} for value in jsonn]


def parse_messages(messages_list):
    """
    Returns a list of pairs (timestamp, weight), parsed from a list of messages

    Currently, the only type of messages allowed are purely numeric

    :param messages_list: list of messages from the retrieve messages function
    :return: list of timestamps, list of weights
    """
    parsed_dates = []
    parsed_times = []
    parsed_weights = []

    for message in messages_list:
        try:
            content = message['content']
            if content[:2] == 'd:':
                # message starts with date; weight taken at a different time from the message
                date, weight = content[2:].split(' ')

                timestamp = datetime.datetime.strptime(date, '%Y-%m-%d')
                parsed_dates.append(timestamp)

                timestamp = timestamp.timestamp() / 86400
                parsed_times.append(timestamp)

                weight = float(weight.replace(',', '.'))
                parsed_weights.append(weight)

            elif message['content'].replace('.', '', 1).isdigit():
                # Only weight was written; taken when message was sent
                timestamp = datetime.datetime.strptime(message['timestamp'][:19], '%Y-%m-%dT%H:%M:%S')
                parsed_dates.append(timestamp)

                timestamp = timestamp.timestamp() / 86400
                parsed_times.append(timestamp)

                weight = float(message['content'].replace(',', '.'))
                parsed_weights.append(weight)

            else:
                continue

        except ValueError:
            # not a valid message, skip
            continue

    parsed_dates = order_x_y(parsed_dates, parsed_times)
    parsed_weights = order_x_y(parsed_weights, parsed_times)
    parsed_times = order_x_y(parsed_times, parsed_times)

    return parsed_dates, parsed_times, parsed_weights


if __name__ == '__main__':
    messages = retrieve_messages(secretfiles.channel_id, secretfiles.authorization)
    dates, timestamps, weights = parse_messages(messages)

    result = analysistools.linear_regression(timestamps, weights)
    print('Losing {:.2f} Kg per month'.format(-result['slope']*30))

    analysistools.plot_data(dates, timestamps, weights, result['regressor'])
