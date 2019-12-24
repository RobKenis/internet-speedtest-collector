import subprocess
import json

import boto3

client = boto3.client(
    'dynamodb',
    region_name='eu-west-1',
    aws_access_key_id='_SET_THIS_DURING_BUILD_',
    aws_secret_access_key='_SET_THIS_DURING_BUILD_'
)
TABLE = '_SET_THIS_DURING_BUILD_'


def _store_in_dynamo(timestamp, ping, download, upload):
    print('Saving to DynamoDB')
    client.put_item(
        TableName=TABLE,
        Item={
            'timestamp': {'S': timestamp},
            'ping': {'S': str(ping)},
            'download': {'S': str(download)},
            'upload': {'S': str(upload)},
        }
    )


def _to_mbit(bits):
    return round(bits / (1000 * 1000), 2)


def gather_info():
    print("Gathering info . . .")
    result = subprocess.check_output(["speedtest-cli", "--json"])
    output = json.loads(result)
    ping = output["ping"]
    download = output["download"]
    upload = output["upload"]
    print("Ping: {ping} ms, Download: {download} MBit, Upload: {upload} MBit".format(ping=ping,
                                                                                     download=_to_mbit(download),
                                                                                     upload=_to_mbit(upload)))
    return output


def run():
    info = gather_info()
    _store_in_dynamo(info['timestamp'], info['ping'], info['download'], info['upload'])
    print("Finished gathering info for {timestamp}".format(timestamp=info["timestamp"]))


run()
