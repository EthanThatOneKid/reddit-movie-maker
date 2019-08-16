# 📽 Reddit Movie Maker
> This project makes use of Python, Processing, and REST APIs to create Reddit-themed YouTube videos

## Requirements
* see the [`requirements.txt`](requirements.txt) for python modules
* secrets requirements (found in `helpers/dotenv.json` file):
  * a processing executable (must place full path to exe)
  * reddit api authentication, a `client_id`, `client_secret`, and `user_agent`.
  * for `sketch`, just put your full path to [the processing sketch's directory](helpers/post_maker)
* perhaps you should use a [python venv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) to keep this project self-contained.

## Sample Scripts
* `py main.py "POST_ID"`
  * saves video as `db/DATE/[TITLE]/final.mp4`
  * example: `py main.py "b7oy9d"`

## Vision
Be able to input a comment thread or subreddit and have this program go through the most popular posts, visualize the text as an image, synthesize a voice to read off the text, place them together, and stitch all of the clips together to create a variable length video.
If this works, I can make countless Reddit videos daily and become a millionaire if the videos amass a big following. :)

## Plan

### Find Popular Posts
Use the [Reddit API](https://www.reddit.com/dev/api/). For subreddits, use `https://www.reddit.com/r/[subreddit].json`. For comment threads, use `https://www.reddit.com/r/all/comments/[post_id].json` or just use a Reddit API wrapper like praw. Maybe for a future update, I can try translating the text in different languages and get multiple versions of the same video.

### Visualize Text
I wrote a processing (java) script that loads the comment data through a given JSON file. It generates an image for each sentence of each comment and places it in a temporary directory. The code for this can be viewed [here](helpers/post_maker/post_maker.pde).

### Voice Synthesis
Install gTTS: `sudo pip install gTTS`.
Example:
```
from gtts import gTTS
tts = gTTS(text='Good morning', lang='en')
tts.save("good.mp3")
```

### Video Compiling
Use the [moviepy](https://github.com/Zulko/moviepy) Python library.

## Main Process Summary
> All of the following will take place in a database of which the naming convention shall be `./YY/MM/DD/[timestamp]`.

1. Parse all of the posts/comments from a subreddit/post.
1. Convert each body of text into arrays of sentences and save it in a json file.
1. Pass the above json file's full path as an argument for the processing sketch to create images for each iteration of images (For each post/comment, create a directory (0-based), and in each directory have another directory called *photos* and save the generated photos in it (also 0-based)).
1. Create an audio file using voice synthesis for each sentence. As the audio files are made, save them in their respective post/comment's directory under a directory *audio*. Once done saving the audio for a post, save a json file in the directory called *meta* to keep track of the durations of each audio file and know how many there are.
1. For each post/comment directory, append each photo in order to the video for a length determined by the respective meta file and pair it with the audio file.
1. Render and save the video file.
