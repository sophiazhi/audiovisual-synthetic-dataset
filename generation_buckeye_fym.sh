#!/bin/bash                      
#SBATCH -t 16:00:00
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
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s1201a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s1201b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s1202a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s1202b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s1203a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s1203b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s1204a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus

# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s2101a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s2101b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s2102a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s2102b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus

# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3101a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3101b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3102a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3102b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3103a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus

# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3701a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3701b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3702a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3702b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3703a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
# singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3703b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus

singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3901a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3901b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3902a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3902b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3903a.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
singularity exec --nv --bind /om2/user/szhi/ /om2/user/szhi/vagrant/wav2lip-local.simg python speech_to_video_buckeye.py buckeye_audio_jsons_short/s3903b.json --base_video $base_video --video_corpus $video_corpus --audio_corpus $audio_corpus
### end wav2lip-local singularity image ###