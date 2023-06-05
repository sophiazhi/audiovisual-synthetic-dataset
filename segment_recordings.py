import buckeye
import pandas as pd
import argparse
from tqdm import tqdm
from pathlib import Path
import glob
import os
import subprocess
import json

def parse_args():
    parser = argparse.ArgumentParser(description='Parse arguments for Buckeye audio segmentation')
    
    parser.add_argument('--buckeye_path', default='/home/szhi/corpora/Buckeye')
    parser.add_argument('--segments_path', default='/home/szhi/corpora/buckeye_segments')

    args = parser.parse_args()
    return args

def generate_tracks(buckeye_path):
    wav_paths = sorted(glob.glob(os.path.join(buckeye_path, 's[0-4][0-9]0[0-5][ab].wav')))
    # wav_paths = [os.path.join(buckeye_path, 's0101a.wav')]
    
    for wav_path in wav_paths:
        rec_id = Path(wav_path).stem
        if rec_id == 's3504a':
            # this file is formatted differently and isn't easily parseable for now
            continue
        path_prefix = os.path.join(buckeye_path, rec_id)
        track = buckeye.Track(name=rec_id,
                              words=f'{path_prefix}.words',
                              phones=f'{path_prefix}.phones',
                              log=f'{path_prefix}.log',
                              txt=f'{path_prefix}.txt',
                              wav=f'{path_prefix}.wav',
                             )
        yield track

def _segment2df(segment, rec_id):
    segment_timestamp = segment[0].beg
    pre_df = [{
             'Begin': p.beg-segment_timestamp, 
             'End': p.end-segment_timestamp, 
             'Label': p.seg,
             'Type': 'phones', 
             'Speaker': rec_id[:3],
             'Recording_begin': p.beg, 
             'Recording_end': p.end}
            for p in segment
            ]
    return pd.DataFrame(pre_df)

def segment_track(track, segments_path):
    segments = []
    
    current_segment = []
    current_duration = 0
    for phone in track.phones:
        phone_seg = phone.seg
        if phone.seg is None:
            phone_seg = 'SIL'
        
        # if phone_seg == '{B_TRANS}':
        #     continue
        # if phone_seg.startswith('<EXCLUDE') \
        # or (phone_seg == 'SIL' and current_duration >= 5) \
        # or phone_seg == '{E_TRANS}' \
        # or (any(c.isupper() for c in phone_seg) and (current_duration > 20 or phone.dur > 2)) \
        # :
        if any(c.isupper() for c in phone_seg) \
        :
            if len(current_segment) == 0:
                continue
            segments.append(current_segment)
            current_segment = []
            current_duration = 0
            
            if phone_seg == '{E_TRANS}':
                # catch s2902b, where transcript continues after {E_TRANS} phone / end of .wav
                break
        else:
            current_segment.append(phone)
            current_duration += phone.dur
    
    # remove leading or trailing noise from each segment
    # then remove empty segments
    i = 0
    while i < len(segments):
        segment = segments[i]
        
        # while beginning is noise, remove phone until not noise
        while len(segment) > 0 and any(c.isupper() for c in segment[0].seg):
            segment.pop(0)
        # while end is noise, remove phone until not noise
        while len(segment) > 0 and any(c.isupper() for c in segment[-1].seg):
            segment.pop(-1)
        
        if len(segment) == 0:
            segments.pop(i)
        else:
            i += 1
    
    # save segment .wavs and .csv alignments
    speaker_dir = os.path.join(segments_path, track.name[:3])
    if not os.path.exists(speaker_dir):
        subprocess.run(f'mkdir {speaker_dir}', shell=True)
    
    track_dur = track.wav.getnframes()/track.wav.getframerate()
    idx = 0
    while idx < len(segments):
        segment = segments[idx]
        if segment[-1].end > track_dur:
            # s1003a
            # s1901b
            print(track.name, track_dur, segment[-1].end)
            break
        path_prefix = os.path.join(speaker_dir, f'{track.name}_{str(idx).zfill(3)}')
        _segment2df(segment, track.name).to_csv(path_prefix+'.csv', index=False)
        track.clip_wav(path_prefix+'.wav', segment[0].beg, segment[-1].end)
        idx += 1
    
    return idx
    

def write_audio_json(track, num_segments):
    rec_name = track.name
    speaker_name = rec_name[:3]
    paths = [f'{speaker_name}/{rec_name}_{str(idx).zfill(3)}.wav' for idx in range(num_segments)]
    with open(f'audio_jsons/{rec_name}.json', 'w') as f:
        json.dump(paths, f)

if __name__ == '__main__':
    args = parse_args()
    for track in tqdm(generate_tracks(args.buckeye_path)):
        num_segments = segment_track(track, args.segments_path)
        write_audio_json(track, num_segments)
    