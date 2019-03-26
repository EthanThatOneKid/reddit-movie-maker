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
