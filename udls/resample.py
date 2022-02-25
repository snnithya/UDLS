from pathlib import Path
from os import system, path, makedirs
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Audio dataset preprocessing')
    parser.add_argument(
        '--ext',
        nargs='+',
        default=["wav", "mp3", "opus", "ogg", "aif", "aiff", "flac"],
        help='input dataset format')
    parser.add_argument('--sr', default="44100", help='target sampling rate')
    parser.add_argument("--output", default=".", help="output directory location")
    parser.add_argument("--input", default=".", help="input directory location")
    parser.add_argument("--len",
                        default=600,
                        help="length (in second) of target audio")

    args = parser.parse_args()

    out_dir = path.join(args.output, f"out_{args.sr}")
    makedirs(out_dir)

    files = []
    for ext in args.ext:
        for f in Path(args.input).rglob("*." + ext):
            files.append(f)

    for i, elm in enumerate(files):
        elm = str(elm)
        print(f"resampling {path.basename(elm)}")

        out_name = f"audio_{i:05d}_%05d.wav"
        cmd = f"ffmpeg -loglevel panic -hide_banner "
        cmd += f"-i \"{elm}\" -f segment -segment_time {args.len} "
        cmd += "-af \"dynaudnorm, silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-60dB\" "
        cmd += f"-ar {args.sr} -ac 1 {path.join(out_dir, out_name)}"

        system(cmd)

if __name__=="__main__":
    sys.exit(main())