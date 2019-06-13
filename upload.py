import json, subprocess
d = json.loads(open("upload_data.json", "r", encoding="utf8").read())
cmd = "youtube-upload\\upload.sh {} {} {} {}".format(d[0], d[1], d[2], d[3])
subprocess.call(cmd)
