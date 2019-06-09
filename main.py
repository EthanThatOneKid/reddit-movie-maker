# py main.py "b7oy9d"
# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

# Dependencies
import os, re, sys, json, shutil, requests, datetime, subprocess
# import numpy as np
from slugify import slugify
from gtts import gTTS
from moviepy.editor import *
import praw

# Helpers
def create_directory_name(title):
    cur_path = os.path.dirname(os.path.realpath(__file__))
    dir_name = datetime.datetime.today().strftime("%Y-%m-%d")
    return "{}/db/{}/{}".format(cur_path, dir_name, slugify(title))

def create_sketch_cmd(in_dir, out_dir):
    cmd_template = "{} --sketch={} --run \"{}\" \"{}\""
    cmd = cmd_template.format(env["processing-java"], env["sketch"], in_dir, out_dir)
    return cmd

def getAuthor(r):
    try:
        author = r.author.name
    except:
        author = "Anonymous"
    return author

def split_sentences(text):
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    sentences = list(filter(lambda s: len(s) > 1, sentences))
    return sentences

# Main Process
env = json.load(open("./helpers/dotenv.json"))
post_id = sys.argv[1]

## Signing into Reddit's Delicious Server
print("Signing into Reddit's Delicious Server")
try:
    reddit = praw.Reddit(
        client_id=env["client_id"],
        client_secret=env["client_secret"],
        user_agent=env["user_agent"]
    )
except:
    print("Sorry, Reddit is being a b*tch at the moment...")
    exit()

## Getting Comments from Reddit Submission Instance
print("Getting Comments from Reddit Submission Instance")
submission = reddit.submission(id=post_id)
submission.comment_sort = "top" # "confidence"
posts = [[submission.subreddit.display_name, getAuthor(submission), [submission.title]]]
for comment in submission.comments:
    if "body" not in comment.__dict__ or len(comment.body) < 3: break
    author = getAuthor(comment)
    body = split_sentences(comment.body)
    posts.append([submission.title, author, body])

## Preparing Data for Imaging
instance_root = create_directory_name(submission.title)
if os.path.isdir(instance_root):
    shutil.rmtree(instance_root)
os.makedirs(instance_root)
data_path = "{}/data.json".format(instance_root)
posts = posts[:5]
open(data_path, "w").write(json.dumps({"data": posts}))

## Creating Images
print("Creating Images")
out_dir = "{}/photos/".format(instance_root)
cmd = create_sketch_cmd(instance_root, out_dir)
subprocess.call(cmd)
#
# ## Synthesizing Speech
# print("Synthesizing Speech")
# cur_sentence = 0
# for i in range(len(posts)):
#     out_dir = "{}/audio/{}".format(instance_root, i)
#     os.makedirs(out_dir)
#     sentences = posts[i][2]
#     for j in range(len(sentences)):
#         sentence = sentences[j]
#         out_path = "{}/{}.mp3".format(out_dir, j)
#         try:
#             gTTS(text=sentence, lang='en').save(out_path)
#         except:
#             err_msg = "TTS API failed to synthesize: \"{}\"".format(sentence)
#             print(err_msg)
#             exit()
#         cur_sentence += 1
#     percentage_completed = int(100 * cur_sentence / total_sentences)
#     print("Speech synthesis {} percent complete!".format(percentage_completed))
#
# ## Creating Video Clips
# clips = []
# cur_sentence = 0
# path_template = "{}/{}/{}/{}.{}"
# for i in range(len(posts)):
#     sentences = posts[i][2]
#     for j in range(len(sentences)):
#         gimme_mp3 = path_template.format(instance_root, "audio", i, j, "mp3")
#         gimme_png = path_template.format(instance_root, "photos", i, j, "png")
#         gimme_audio = AudioFileClip(gimme_mp3)
#         gimme_clip = ImageClip(gimme_png).set_duration(gimme_audio.duration).set_audio(gimme_audio)
#         clips.append(gimme_clip)
#         cur_sentence += 1
#     percentage_completed = int(100 * cur_sentence / total_sentences)
#     print("Audio and image pairing {} percent complete!".format(percentage_completed))
#
# ## Exporting Final Product
# save_path = "{}/{}.mp4".format(instance_root, title)
# final_video = concatenate_videoclips(clips)
# final_video.set_fps(24).write_videofile(save_path)

print("😊 All Done! 😊")
