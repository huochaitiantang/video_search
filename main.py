import os
import json
import flask
import random
from flask import Flask
app = Flask("video-search")

# get all video ids
def get_video_ids():
    origin_video_dir = "/home/liuliang/Desktop/dataset/video"
    video_dir = "static/video"
    
    if not os.path.exists(video_dir):
        os.symlink(origin_video_dir, video_dir)
    
    video_ids = os.listdir(video_dir)
    video_ids.sort()
    return video_dir, video_ids

# get video matches by rank_opt.txt, pick up whose accuracy of top10 > 8( with same label)
def get_video_matches():
    thresh = 8 # 0 - 10
    f = open('data/rank_opt.txt')
    lls = f.readlines()
    matches = []

    for line in lls:
        items = line.replace('(', '').replace(')', '').split(' ')
        match = {}
        match['src'] = int(items[0])
        match['src_label'] = int(items[1])
        match['ress'] = []
        match['res_labels'] = []
        match['right'] = 0
        
        # top 10 results
        for i in range(2, 32, 3):
            ind = int(items[i])
            lab = int(items[i + 2])
            if lab == match['src_label']:
                match['right'] += 1
            match['ress'].append(ind)
            match['res_labels'].append(lab)
        
        matches.append(match)
    
    # get only right number > 8
    #matches = sorted(matches, key=lambda x : x['right'], reverse=True)
    matches = filter(lambda x: x['right'] >= thresh, matches)
    print("Valid Search Videos: {}".format(len(matches)))
    f.close()
    return matches


video_dir, video_ids = get_video_ids()
video_matches = get_video_matches()


@app.route('/')
def do_home():
    return flask.render_template('home.html')

@app.route('/home/msg_init')
def do_msg_init():
    info = {}
    info['cnt'] = 10
    info['video_paths'] = []
    for i in range(info['cnt']):
        ind = video_matches[i]['src']
        info['video_paths'].append(os.path.join(video_dir, video_ids[ind]))
    return json.dumps(info)

@app.route('/home/msg_change')
def do_msg_change():
    info = {}
    info['cnt'] = 10
    info['video_paths'] = []
    inds = []
    cnts = range(len(video_matches))
    for i in range(info['cnt']):
        x = random.choice(cnts)
        while x in inds:
            x = random.choice(cnts)
        inds.append(x)
        ind = video_matches[x]['src']
        info['video_paths'].append(os.path.join(video_dir, video_ids[ind]))
        #print(info['video_paths'])
    return json.dumps(info)

@app.route('/search/<filename>')
def do_msg_search(filename): 
    info = {}
    
    if not filename in video_ids:
        info['cnt'] = 0
        info['error'] = "video searched [{}] is not existed".format(filename)
        return json.dumps(info)

    src_ind = video_ids.index(filename)
    src_matches = filter(lambda x: x['src'] == src_ind, video_matches)

    if len(src_matches) <= 0:
        info['cnt'] = 0
        info['error'] = "video searched [{}] is not in test list".format(filename)
        return json.dumps(info)

    src_match = src_matches[0]

    info['cnt'] = len(src_match['ress'])
    info['video_paths'] = []
    info['video_scores'] = []
    for i in range(info['cnt']):
        ind = src_match['ress'][i]
        lab = src_match['res_labels'][i]
        info['video_paths'].append(os.path.join(video_dir, video_ids[ind]))
        info['video_scores'].append("#{}".format(i+1))
    return json.dumps(info)

@app.route('/video/<filename>')
def get_video_file(filename):
    return flask.app.send_static_file(os.path.join(video_dir,  filename))

if __name__ == '__main__':
    app.run(host="219.224.168.78", port=5050, debug=True)
