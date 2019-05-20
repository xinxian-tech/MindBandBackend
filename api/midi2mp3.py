#!/usr/bin/env python3

import mimi
import argparse
import os
import sys


def args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'input', nargs='+', help="Input midi files")
    parser.add_argument(
        '-o', dest="output", help="Output directory")
    parser.add_argument(
        '-f', dest="format", help="Output format",
        choices=["mp3", "wav", "png"], default="mp3")

    return parser.parse_args()


def midi2mp3(input: str, output: str):
    print(output)
    try:
        os.remove(output)
    except:
        pass

    f = mimi.MidiFile(input)

    if output.endswith(".mp3"):
        f.save_mp3(output)

    if output.endswith(".wav"):
        f.save_mp3(output.replace(".wav", ".mp3"))
        os.system('ffmpeg -i %s %s' % (output.replace(".wav", ".mp3"), output))

    if output.endswith(".png"):
        f.save_png(output)


if __name__ == '__main__':
    args = args()

    if len(args.input) == 1 and (
        args.output.endswith(".mp3") or
        args.output.endswith(".wav") or
        args.output.endswith(".png")
    ):
        midi2mp3(args.input[0], args.output)

    else:
        directory = os.path.abspath(args.output)
        for file in args.input:
            output = os.path.join(directory, '%s.%s' % (
                os.path.splitext(os.path.basename(file))[0],
                args.format
            ))
            midi2mp3(file, output)


# midi2mp3(args.input, args.output)
