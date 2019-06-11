# Dependencies
import os, re, sys, json, math, time, shutil, requests, datetime, subprocess
from slugify import slugify
from gtts import gTTS
from moviepy.editor import *
from art import *
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

def get_author(r):
    try:
        author = r.author.name
    except:
        author = "Anonymous"
    return author

def render_progress(ratio, width=40):
    completed_units = int(ratio * width)
    remaining_units = width - completed_units
    completion = "{}>{}".format("=" * completed_units, " " * remaining_units)
    render = "[{}] {}% Complete".format(completion, int(100 * ratio))
    sys.stdout.write('\r')
    sys.stdout.write(render)
    sys.stdout.flush()
    return render

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
end_card = ["Thanks!", "EthanThatOneKid", ["Thanks for watching! Please consider liking this video and subscribing to my channel!"]]
comment_limit = 25

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
sort = "top" # "confidence"
title = "{} ({} comments)".format(submission.subreddit.display_name, sort)
submission.comment_sort = sort
posts = [[title, get_author(submission), [submission.title]]]
total_sentences = 0
for comment in submission.comments[:comment_limit]:
    if "body" not in comment.__dict__ or len(comment.body) < 3: break
    comment_sentences = split_sentences(comment.body)
    total_sentences += len(comment_sentences)
    posts.append([submission.title, get_author(comment), comment_sentences])
posts.append(end_card)

## Preparing Data for Imaging
print("Preparing Data for Imaging")
instance_root = create_directory_name(submission.title)
if os.path.isdir(instance_root):
    shutil.rmtree(instance_root)
os.makedirs(instance_root)
data_path = "{}/data.json".format(instance_root)
open(data_path, "w").write(json.dumps({"data": posts}))

## Generating YouTube Description
print("Generating YouTube Description")
description_template_path = "static/description_template.txt"
description_save_path = "{}/description.txt".format(instance_root)
description = open(description_template_path, "r", encoding="utf8").read()
question_url = "http://jservice.io/api/random"
question_data = requests.get(question_url).json()[0]
description = description.replace("{SUB}", submission.subreddit.display_name)
description = description.replace("{POST}", post_id)
description = description.replace("{DATE}", datetime.datetime.today().strftime("%Y-%m-%d"))
description = description.replace("{DIFFICULTY}", str(question_data["value"]))
description = description.replace("{CATEGORY}", question_data["category"]["title"])
description = description.replace("{QUESTION}", question_data["question"])
description = description.replace("{ANSWER}", text2art(question_data["answer"], "mirror_flip"))
description = description.replace("{MOOD}", art("rand"))
open(description_save_path, "w", encoding="utf8").write(description)

## Creating Images
print("Creating Images")
out_dir = "{}/photos/".format(instance_root)
cmd = create_sketch_cmd(instance_root, out_dir)
subprocess.call(cmd)

## Synthesizing Speech
print("Synthesizing Speech")
cur_sentence, cur_post = 0, 0
for i in range(len(posts)):
    out_dir = "{}/audio/{}".format(instance_root, i)
    os.makedirs(out_dir)
    sentences = posts[i][2]
    gimme_lang = "en-uk" if cur_post % 2 == 1 else "en-au"
    for j in range(len(sentences)):
        sentence = sentences[j]
        out_path = "{}/{}.mp3".format(out_dir, j)
        try:
            gTTS(text=sentence, lang=gimme_lang).save(out_path)
        except:
            err_msg = "TTS API failed to synthesize: \"{}\"".format(sentence)
            print(err_msg)
            exit()
        cur_sentence += 1
        render_progress(cur_sentence / total_sentences)
    cur_post += 1
print("")

## Creating Video Clips
print("Creating Video Clips")
clips = []
cur_sentence = 0
path_template = "{}/{}/{}/{}.{}"
for i in range(len(posts)):
    sentences = posts[i][2]
    for j in range(len(sentences)):
        gimme_mp3 = path_template.format(instance_root, "audio", i, j, "mp3")
        gimme_png = path_template.format(instance_root, "photos", i, j, "png")
        gimme_audio = AudioFileClip(gimme_mp3)
        gimme_clip = ImageClip(gimme_png).set_duration(gimme_audio.duration).set_audio(gimme_audio)
        clips.append(gimme_clip)
        cur_sentence += 1
        render_progress(cur_sentence / total_sentences)
print("")

## Concatenating Videoclips
print("Concatenating Videoclips")
final_video = concatenate_videoclips(clips)

## Layering Music
print("Layering Music")
bg_music = AudioFileClip("static/music/0.mp3")
bg_music_repeats = math.floor(final_video.duration / bg_music.duration)
bg_music_remainder = final_video.duration % bg_music.duration
bg_music_audioclips = [bg_music] * bg_music_repeats + [bg_music.set_end(bg_music_remainder)]
bg_music = concatenate_audioclips(bg_music_audioclips)
final_video.audio = CompositeAudioClip([final_video.audio, bg_music.volumex(0.2)])

## Exporting Final Product
print("Exporting Final Product")
save_path = "{}/{}.mp4".format(instance_root, "final")
final_video.write_videofile(save_path, fps=24)

## Deleting All Temporary Files
print("Deleting All Temporary Files")
shutil.rmtree("{}/audio/".format(instance_root))
shutil.rmtree("{}/photos/".format(instance_root))
os.remove("{}/data.json".format(instance_root))

## All Done!
print("😊 All Done! 😊")
print("Final Product saved as...")
print(save_path)
exit()
