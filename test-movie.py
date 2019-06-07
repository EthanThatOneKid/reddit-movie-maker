# py test-movie.py
from moviepy.editor import *

# Main Process
clip1PhotoPath = "C:/Users/acer/Documents/GitHub/reddit-movie-maker/test/0.png"
clip1AudioPath = "C:/Users/acer/Documents/GitHub/reddit-movie-maker/test/0.mp3"

audClip1 = AudioFileClip(clip1AudioPath)
clip = ImageClip(clip1PhotoPath).set_duration(audClip1.duration).set_audio(audClip1)

# audClip1 = AudioFileClip(clip1AudioPath)
# audClip2 = AudioFileClip(clip2AudioPath)
# clips = [
#     ImageClip(clip1PhotoPath).set_duration(audClip1.duration).set_audio(audClip1),
#     ImageClip(clip2PhotoPath).set_duration(audClip2.duration).set_audio(audClip2)
# ]
#
# final_video = concatenate_videoclips(clips)
# final_video.write_videofile("test.mp4")

clip.write_videofile("./test/test.mp4", fps=24)



# write concat demuxer photos.txt for all images using audio durations
# ffmpeg -f concat -i photos.txt test1.mp4
# ffmpeg -f concat -i photos.txt -vsync vfr -pix_fmt yuv420p output.mp4
# write concat demuxer audio.txt for all audio files
# ffmpeg -f concat -i audio.txt test1.mp3
# ffmpeg -f concat -safe 0 -i audio.txt -c copy output.mp3
# combine the audio file and the video file
# ffmpeg -i test1.mp4 -i test1.mp3 -codec copy -shortest output.mp3
