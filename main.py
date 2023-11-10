from googletrans import Translator
import pysrt
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument(
    '-f',
    '--file',
    type=str,
    help='select srt file'
)
parser.add_argument(
    '-d',
    '--dir',
    type=str,
    help='select directory'
)

translator = Translator()

def translate(fp):
    subs = pysrt.open(fp)
    arrayToTranslate = []
    translatedArray = []
    for sub in subs:
        stripSub = sub.text.strip()
        stringToTranslate = '\n\n'.join(arrayToTranslate)
        if len(stringToTranslate + stripSub) > 5000:
            result = translator.translate(stringToTranslate, dest='fa')
            translatedArray.extend(result.text.split('\n\n'))
            arrayToTranslate.clear()
        arrayToTranslate.append(stripSub)
    
    stringToTranslate = '\n\n'.join(arrayToTranslate)
    result = translator.translate(stringToTranslate, dest='fa')
    translatedArray.extend(result.text.split('\n\n'))
    
    for i in range(len(subs)):
        subs[i].text = translatedArray[i]
    subs.save(
        os.path.join(
            os.path.dirname(fp),
            'fa-' + os.path.basename(fp)
        ),
        encoding='utf-8'
    )
    
args = parser.parse_args()

if args.file and os.path.isfile(args.file):
    translate(args.file)
elif args.dir and os.path.isdir(args.dir):
    for p in os.listdir(args.dir):
        rp = os.path.join(args.dir, p)
        if os.path.isfile(rp) and os.path.splitext(rp)[1] == '.srt':
            translate(rp)