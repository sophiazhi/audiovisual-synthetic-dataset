#!/bin/bash                      
#SBATCH -t 36:00:00
#SBATCH --gres gpu:QUADRORTX6000:1
#SBATCH --cpus-per-task 24 
#SBATCH --ntasks 1 
#SBATCH --constraint high-capacity
#SBATCH --mem 35G

audio_list='audio_jsons/fourth2500.json'
base_video='base_videos/IMG_7797.MOV'
video_corpus='/om2/user/szhi/corpora/childes_synthetic_video_doublepad60fps'


### start wav2lip-local singularity image ###
module load openmind/singularity/3.4.1
cd /om2/user/szhi/synthetic_dataset

# # call speech_to_video
singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video.py --audio_list $audio_list --base_video $base_video --video_corpus $video_corpus
### end wav2lip-local singularity image ###