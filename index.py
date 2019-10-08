import subprocess
import json

def _to_mbit(bits):
    return round(bits / (1000 * 1000), 2)

def gather_info():
    print("Gathering info . . .")
    result = subprocess.check_output(["speedtest-cli", "--json"])
    output = json.loads(result)
    ping = output["ping"]
    download = output["download"]
    upload = output["upload"]
    print("Ping: {ping} ms, Download: {download} MBit, Upload: {upload} MBit".format(ping=ping, download=_to_mbit(download), upload=_to_mbit(upload)))
    return output

def run():
    info = gather_info()
    print("Finished gathering info for {timestamp}".format(timestamp=info["timestamp"]))

run()
