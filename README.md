# Reddit Movie Maker

## Vision
Be able to input a comment thread or subreddit and have this program go through the most popular posts, visualize the text as an image, synthesize a voice to read off the text, place them together, and stitch all of the clips together to create a variable length video.
If this works, I can make countless Reddit videos daily and become a millionaire if the videos amass a big following. :)

## Plan

### Find Popular Posts
Use the [Reddit API](https://www.reddit.com/dev/api/). For subreddits, use `https://www.reddit.com/r/[subreddit].json`. For comment threads, use `https://www.reddit.com/r/all/comments/[post_id].json`. Maybe, I can try translating the text in different languages and get multiple versions of the same video.

### Visualize Text
Either create a webview using JavaScript and writing an html file with updated text and screenshot the views, or create a sketch in Processing and pass the text as a parameter and save screenshots from that.

### Voice Synthesis
Install gTTS: `sudo pip install gTTS`.
Example:
```
from gtts import gTTS
import os
tts = gTTS(text='Good morning', lang='en')
tts.save("good.mp3")
```

### Video Compiling
Use the [moviepy](https://github.com/Zulko/moviepy) Python library.
