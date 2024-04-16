"""
Program: cli_audiorecorder.py
Objektorientierte Programmierung SS 2024 - BHT Medieninformatik
Autor Erik Brodmann
"""

import urllib.request
import urllib.error
from urllib.parse import urlparse
import datetime
import argparse


def url_check(arg):
    """
    URL validation
    """
    url = urlparse(arg)
    if all((url.scheme, url.netloc)):
        return arg
    raise argparse.ArgumentTypeError('Invalid URL')


def record_audio(url, filename, duration, blocksize):
    """
    Records audio from the provided URL for the specified duration and saves it to a file.
    """
    start_time = datetime.datetime.now()
    punctuation = ['.', '..', '...']
    punctuation_index = 0

    try:
        with urllib.request.urlopen(url) as stream:
            with open(filename + '.mp3', 'wb') as outfile:
                while (datetime.datetime.now() - start_time).total_seconds() < duration:
                    data = stream.read(blocksize)
                    if not data:
                        break
                    outfile.write(data)
                    print("Recording" + punctuation[punctuation_index])
                    punctuation_index = (punctuation_index + 1) % len(punctuation)
    except urllib.error.URLError as e:
        print(e.reason)


if __name__ == '__main__':
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Radio Audiorecorder")

    # Adding optional parameters
    parser.add_argument('-url', type=url_check, help="URL of the audio stream & should end with /mp3/", required=True)
    parser.add_argument('-fn', '--filename', help="Name of recording", default="myRadioRecording")
    parser.add_argument('-dr', '--duration', type=int, help="Duration of recording in seconds", default=30)
    parser.add_argument('-bs', '--blocksize', type=int, help="Block size for read/write in bytes", default=64)

    # Parsing the arguments
    args = parser.parse_args()

    # Record audio
    record_audio(args.url, args.filename, args.duration, args.blocksize)

    # Print a message after recording ends
    print("Recording ended,", args.duration, "seconds.")

    # Print the file created
    print("File created =", args.filename + '.mp3')