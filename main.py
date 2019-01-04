import os
import json
import flask
import random
from flask import Flask
app = Flask("video-search")


origin_video_dir = "/home/liuliang/Desktop/dataset/video"
video_dir = "static/video"

if not os.path.exists(video_dir):
    os.symlink(origin_video_dir, video_dir)

video_ids = os.listdir(video_dir)
video_ids.sort()


@app.route('/')
def do_home():
    return flask.render_template('home.html')

@app.route('/home/msg_init')
def do_msg_init():
    info = {}
    info['cnt'] = 10
    info['video_paths'] = []
    for i in range(info['cnt']):
        info['video_paths'].append(os.path.join(video_dir, video_ids[i]))
    return json.dumps(info)

@app.route('/home/msg_change')
def do_msg_change():
    info = {}
    info['cnt'] = 10
    info['video_paths'] = []
    inds = []
    cnts = range(len(video_ids))
    for i in range(info['cnt']):
        x = random.choice(cnts)
        while x in inds:
            x = random.choice(cnts)
        inds.append(x)
        info['video_paths'].append(os.path.join(video_dir, video_ids[x]))
        print(info['video_paths'])
    return json.dumps(info)

@app.route('/search/<filename>')
def do_msg_search(filename): 
    info = {}
    file_path = os.path.join(video_dir, filename)
    print("search video: ".format(file_path))
    if not os.path.exists(file_path):
        info['cnt'] = 0
        info['error'] = "video searched [{}] is not existed".format(filename)
        return json.dumps(info)
    info['cnt'] = 10
    info['video_paths'] = []
    info['video_scores'] = []
    for i in range(info['cnt']):
        info['video_paths'].append(os.path.join(video_dir, video_ids[i]))
        info['video_scores'].append("{:.3f}".format(random.random()))
    return json.dumps(info)

@app.route('/video/<filename>')
def get_video_file(filename):
    return flask.app.send_static_file(os.path.join(video_dir,  filename))




if __name__ == '__main__':
    app.run(host="219.224.168.78", port=5026, debug=True)
