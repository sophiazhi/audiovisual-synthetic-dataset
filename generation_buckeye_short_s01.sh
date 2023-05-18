#!/bin/bash                      
#SBATCH -t 12:00:00
#SBATCH --gres gpu:QUADRORTX6000:1
#SBATCH --cpus-per-task 24 
#SBATCH --ntasks 1 
#SBATCH --constraint high-capacity
#SBATCH --mem 35G


base_video='base_videos/IMG_7797.MOV'
video_corpus='/om2/user/szhi/corpora/buckeye_synthetic_video_short_new16'
audio_corpus='/om2/user/szhi/corpora/buckeye_segments_short'


### start wav2lip-local singularity image ###
module load openmind/singularity/3.4.1
cd /om2/user/szhi/synthetic_dataset

# # call speech_to_video
singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s0101a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s0101b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s0102a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s0102b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s0103a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
### end wav2lip-local singularity image ###