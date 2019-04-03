# py test-movie.py
from moviepy.editor import *

# Main Process
fps = 24
clip1PhotoPath = "C:\\Users\\acer\\Documents\\GitHub\\reddit-movie-maker\\db\\2019\\04\\01\\1554155961\\photos\\0\\0.jpeg"
clip1AudioPath = "C:\\Users\\acer\\Documents\\GitHub\\reddit-movie-maker\\db\\2019\\04\\01\\1554155961\\audio\\0\\0.mp3"
clip2PhotoPath = "C:\\Users\\acer\\Documents\\GitHub\\reddit-movie-maker\\db\\2019\\04\\01\\1554155961\\photos\\0\\1.jpeg"
clip2AudioPath = "C:\\Users\\acer\\Documents\\GitHub\\reddit-movie-maker\\db\\2019\\04\\01\\1554155961\\audio\\0\\1.mp3"

audClip1 = AudioFileClip(clip1AudioPath)
audClip2 = AudioFileClip(clip2AudioPath)
clips = [
    ImageClip(clip1PhotoPath).set_fps(fps).set_duration(audClip1.duration).set_audio(audClip1),
    ImageClip(clip2PhotoPath).set_fps(fps).set_duration(audClip2.duration).set_audio(audClip2)
]

final_video = concatenate_videoclips(clips, method='chain')
final_video.write_videofile("test.mp4", fps=fps)
