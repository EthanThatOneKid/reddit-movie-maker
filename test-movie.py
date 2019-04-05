# py test-movie.py
import subprocess
from moviepy.editor import *

# Main Process
fps = 24
clip1PhotoPath = "C:\\Users\\acer\\Documents\\GitHub\\reddit-movie-maker\\db\\2019\\04\\01\\1554155961\\photos\\0\\0.jpeg"
clip1AudioPath = "C:\\Users\\acer\\Documents\\GitHub\\reddit-movie-maker\\db\\2019\\04\\01\\1554155961\\audio\\0\\0.mp3"
clip2PhotoPath = "C:\\Users\\acer\\Documents\\GitHub\\reddit-movie-maker\\db\\2019\\04\\01\\1554155961\\photos\\0\\1.jpeg"
clip2AudioPath = "C:\\Users\\acer\\Documents\\GitHub\\reddit-movie-maker\\db\\2019\\04\\01\\1554155961\\audio\\0\\1.mp3"

audClip1 = AudioFileClip(clip1AudioPath)
audClip2 = AudioFileClip(clip2AudioPath)
dur = audClip1.duration + audClip2.duration
clips = [
    ImageClip(clip1PhotoPath).set_fps(fps).set_duration(audClip1.duration).set_audio(audClip1),
    ImageClip(clip2PhotoPath).set_fps(fps).set_duration(audClip2.duration).set_audio(audClip2)
]

ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg.exe"
subprocess.call([
    ffmpeg,
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    "photos.txt",
    # "-vsync",
    # "vfr",
    # "-pix_fmt",
    # "yuv420p",
    "C:\\Users\\acer\\Documents\\GitHub\\reddit-movie-maker\\test1.mp4"
])

# write concat demuxer photos.txt for all images using audio durations
# ffmpeg -f concat -i photos.txt test1.mp4
# ffmpeg -f concat -i photos.txt -vsync vfr -pix_fmt yuv420p output.mp4
# write concat demuxer audio.txt for all audio files
# ffmpeg -f concat -i audio.txt test1.mp3
# ffmpeg -f concat -safe 0 -i audio.txt -c copy output.mp3
# combine the audio file and the video file
# ffmpeg -i test1.mp4 -i test1.mp3 -codec copy -shortest output.mp3

# final_video = concatenate_videoclips(clips, method='chain')
# final_video.write_videofile("test.mp4", fps=fps)
