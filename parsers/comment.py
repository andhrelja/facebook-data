import os
from progress.bar import Bar


from stage.comment import Comment
from config import COMMENTS_DIR, COMMENTS_OUTPUT
from utils import read_initial_json, read_json, write_json


class CommentParser(object):
    def __init__(self, comments_dir='comments.json'):
        self.comments_dir = os.path.join(COMMENTS_DIR, comments_dir)
        self.comment_data = list()
        self.comments = list()
    
    def set_comments(self, limit=None):
        if not os.path.isfile(COMMENTS_OUTPUT):
            comments = self.collect_comments(limit)
            self._set_comments(comments)
            self.write_to_json()
        else:
            comments = read_json(COMMENTS_OUTPUT)
            self._set_comments(comments[:limit])

    def _set_comments(self, comments):
        bar = Bar('Setting up comments', max=len(comments))

        test = set()
        for comment in comments:
            comm = Comment(**comment)
            comm = self.process_data(comm)
            # test.add(comm.target_post)
            self.comments.append(comm)

            self.comment_data.append(comment)
            bar.next()
        
        bar.finish()

    def collect_comments(self, limit):
        authors = set()
        comments = list()

        comment_data = read_initial_json(self.comments_dir)
        comment_list = comment_data['comments'][:limit]

        bar = Bar('Collecting comments', max=len(comment_list))
        for comment in comment_list:
            comment = self._collect_comment_data(authors, comment)
            comments += comment
            bar.next()
        bar.finish()
        return comments
    
    def _collect_comment_data(self, authors, comment):
        _comments = list()
        if 'data' in comment.keys():
            for cmnt in comment['data']:
                try:
                    author = cmnt['comment']['author']
                    authors.add(author)
                except KeyError:
                    if len(authors) > 1:
                        raise Exception('Multiple comment authors')
                    author = list(authors)[0]
                
                try:
                    group = comment['comment']['group']
                except KeyError:
                    group = None
                
                _comment = {
                    'content': cmnt['comment']['comment'],
                    'author': author,
                    'title': comment['title'],
                    'timestamp': cmnt['comment']['timestamp'],
                    'group': group
                }


                _comments.append(_comment)

        return _comments

    def process_data(self, comment):
        comment.process_title()
        return comment


    def get_initial_data(self):
        return read_initial_json(self.comments_dir)

    def write_to_json(self):
        write_json(COMMENTS_OUTPUT, self.comment_data)
    