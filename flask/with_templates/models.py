# -*- coding: utf-8 -*-
import json
import datetime

class Storage(object):
    obj = None

    items = None

    @classmethod
    def __new__(cls, *args):
        if cls.obj is None:
            cls.obj = object.__new__(cls)
            cls.items = []
        return cls.obj


class BlogPostModel(object):
    def __init__(self, date, title, text,img):
        self.title = title
        self.text = text
        self.date = date
        self.img = img


class PostEncoder(json.JSONEncoder):
    def default(self, o):
        # print(o)
        if isinstance(o, BlogPostModel):
            return {
                'date': o.date.strftime('%d/%m/%Y %H:%M'),
                'title': o.title,
                'text': o.text,
                'img': o.img

            }
        else:
            return json.JSONEncoder().default(o)


class PostDecoder(json.JSONDecoder):
    def _parse_post(self, default_obj):

        return BlogPostModel(
            datetime.datetime.strptime(default_obj['date'],'%d/%m/%Y %H:%M'),
            default_obj['title'],
            default_obj['text'],
            default_obj['img']
        )

    def decode(self, json_string, **kwargs):
        default_obj = super(PostDecoder, self).decode(
                json_string, **kwargs)
        if isinstance(default_obj, (tuple, list)):
            return [self._parse_post(item) for item in default_obj]

        return self._parse_post(default_obj)

