import textgrid as tg
import pandas as pd
import json
import argparse
import os
from pathlib import Path
import buckeye


def parse_args():
    parser = argparse.ArgumentParser(description='Parse arguments for csv-to-textgrid conversion')
    
    parser.add_argument('audio_json')
    parser.add_argument('--csv_path', default='/home/szhi/corpora/buckeye_segments')
    parser.add_argument('--textgrid_path', default='/home/szhi/corpora/buckeye_segments')
    parser.add_argument('--buckeye_path', default='/home/szhi/corpora/Buckeye')
    parser.add_argument('--utt_id', default=None)

    args = parser.parse_args()
    return args

def get_csv_list(audio_json):
    with open(audio_json, 'r') as f:
        audio_list = json.load(f)
    
    csv_list = [audio_name[:-4]+'.csv' for audio_name in audio_list]
    return csv_list

def csv2tg(csv_list, csv_path, textgrid_path):
    for csv_name in csv_list:
        alignment_csv = pd.read_csv(os.path.join(csv_path, csv_name))
        
        phone_tier = tg.IntervalTier('phones')
        for idx,phone in alignment_csv.iterrows():
            phone_tier.add(phone['Begin'] + 0.5, phone['End'] + 0.5, phone['Label'])
        phone_tier.add(phone['End'] + 0.5, phone['End'] + 1.0, "") # for 0.5s silence at end
        
        utt_id = Path(csv_name).stem
        textgrid = tg.TextGrid(utt_id)
        textgrid.append(phone_tier)
        
        textgrid.write(os.path.join(textgrid_path, csv_name[:-4]+'_deepfake.TextGrid'))

def buckeye2tg(utt_id, buckeye_path, textgrid_path):
    track = buckeye.Track(name=utt_id,
                      words=os.path.join(buckeye_path, f'{utt_id}.words'),
                      phones=os.path.join(buckeye_path, f'{utt_id}.phones'),
                      log=os.path.join(buckeye_path, f'{utt_id}.log'),
                      txt=os.path.join(buckeye_path, f'{utt_id}.txt'),
                      wav=os.path.join(buckeye_path, f'{utt_id}.wav') # wav is optional
                      )
    word_tier = tg.IntervalTier('words')
    for word in track.words:
        if isinstance(word, buckeye.containers.Word):
            word_tier.add(word.beg, word.end, word.orthography)
        elif isinstance(word, buckeye.containers.Pause):
            word_tier.add(word.beg, word.end, word.entry)

    phone_tier = tg.IntervalTier('phones')
    for phone in track.phones:
        phone_tier.add(phone.beg, phone.end, phone.seg)

    textgrid = tg.TextGrid(utt_id)
    textgrid.append(word_tier)
    textgrid.append(phone_tier)
    
    textgrid.write(os.path.join(textgrid_path, utt_id[:3], f'{utt_id}.TextGrid'))

if __name__ == '__main__':
    args = parse_args()
    
    if args.utt_id:
        buckeye2tg(args.utt_id, args.buckeye_path, args.textgrid_path)
    else:
        csv_list = get_csv_list(args.audio_json)
        csv2tg(csv_list, args.csv_path, args.textgrid_path)
