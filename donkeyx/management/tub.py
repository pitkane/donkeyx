"""
tub.py

Manage tubs
"""

import os
import sys
import time
import json
import tornado.web
from stat import S_ISREG, ST_MTIME, ST_MODE, ST_CTIME, ST_ATIME


class TubsView(tornado.web.RequestHandler):

    def initialize(self, data_path):
        self.data_path = data_path

    def get(self):
        import fnmatch
        dir_list = fnmatch.filter(os.listdir(self.data_path), '*')
        dir_list.sort()
        data = {"tubs": dir_list}
        self.render("tub_web/tubs.html", **data)


class TubView(tornado.web.RequestHandler):

    def get(self, tub_id):
        data = {}
        self.render("tub_web/tub.html", **data)


class TubApi(tornado.web.RequestHandler):

    def initialize(self, data_path):
        self.data_path = data_path

    def image_path(self, tub_path, frame_id):
        return os.path.join(tub_path, str(frame_id) + "_cam-image_array_.jpg")

    def record_path(self, tub_path, frame_id):
        return os.path.join(tub_path, "record_" + frame_id + ".json")

    def clips_of_tub(self, tub_path):
        seqs = [int(f.split("_")[0])
                for f in os.listdir(tub_path) if f.endswith('.jpg')]
        seqs.sort()

        entries = ((os.stat(self.image_path(tub_path, seq))
                    [ST_ATIME], seq) for seq in seqs)

        (last_ts, seq) = next(entries)
        clips = [[seq]]
        for next_ts, next_seq in entries:
            if next_ts - last_ts > 100:  # greater than 1s apart
                clips.append([next_seq])
            else:
                clips[-1].append(next_seq)
            last_ts = next_ts

        return clips

    def get(self, tub_id):
        clips = self.clips_of_tub(os.path.join(self.data_path, tub_id))

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps({'clips': clips}))

    def post(self, tub_id):
        tub_path = os.path.join(self.data_path, tub_id)
        old_clips = self.clips_of_tub(tub_path)
        new_clips = tornado.escape.json_decode(self.request.body)

        import itertools
        old_frames = list(itertools.chain(*old_clips))
        new_frames = list(itertools.chain(*new_clips['clips']))
        frames_to_delete = [str(item)
                            for item in old_frames if item not in new_frames]
        for frm in frames_to_delete:
            os.remove(self.record_path(tub_path, frm))
            os.remove(self.image_path(tub_path, frm))
