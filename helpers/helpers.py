import os, re, sys, json, requests, datetime

def create_directory_name():
    full_path = os.path.dirname(os.path.realpath(__file__))
    dir_name = datetime.datetime.today().strftime("%Y/%m/%d")
    timestamp = int(datetime.datetime.now().timestamp())
    return "{}/db/{}/{}".format(full_path, dir_name, timestamp)

def create_sketch_cmd(env, in_path, out_dir):
    cmd_template = "{} --sketch={} --run \"{}\" \"{}\""
    cmd = cmd_template.format(env["processing-java"], env["sketch"], in_path, out_dir)
    return cmd

def get_subreddit_posts(r):
    print(r)
    posts = []
    for child in r["data"]["children"]:
        gimme_data = child["data"]
        if len(gimme_data["selftext"]) == 0: continue
        posts.append([
            gimme_data["title"],   # title
            gimme_data["author"],  # user
            gimme_data["selftext"] # body
        ])
    return posts

def get_post_comments(r):
    posts = []
    title = r[0]["data"]["children"][0]["data"]["title"]
    for child in r[1]["data"]["children"]:
        if child["kind"] != "t1": continue
        gimme_data = child["data"]
        if len(gimme_data["body"]) == 0: continue
        posts.append([
            title,                # title
            gimme_data["author"], # user
            gimme_data["body"]    # body
        ])
    return posts

def create_reddit_url(env, config):
    endpoint = env[config]
    url = endpoint["head"] + id + endpoint["foot"]
    return url

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
    return sentences
