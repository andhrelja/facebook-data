from datetime import datetime

from db.comment import Comment

POST_NAME = {
    'objavu': 'objava',
    'videozapis': 'videozapis',
    'vezu': 'veza',
    'videoprijenos': 'videoprijenos',
    'fotografiju': 'fotografija',
    'bilješku': 'bilješka',
    'album': 'album',
    'odgovara': 'odgovor',
    'događaj': 'događaj'
}

class Comment(dict):
    db_table = Comment
    
    def __init__(self, content, author, title, group, timestamp):
        self.content = content
        self.author = author
        self.title = title
        self.group = group
        self.timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        self.target_user = None
        self.target_post = None
    
    def process_title(self):
        processing = self.title.replace(self.author, '')
        processing = processing.replace('komentira', '')
        processing = processing.replace('.', '')
        processing = processing.strip()

        if 'svoju' in processing:
            self.target_user = self.author
            self.target_post = processing.replace('svoju', '').strip()
        else:
            processing_split = processing.split(' ')
            
            if 'od' in processing_split[1:]:
                processing_split.remove('od')
            
            if 'na' in processing_split[1:] and 'komentar' in processing_split[1:]:
                if 'svoj' in processing_split[1:]:
                    self.target_user = self.author
                    processing_split.remove('svoj')
                processing_split.remove('na')
                processing_split.remove('komentar')

            post_name = processing_split[0]
            if post_name in POST_NAME.keys():
                self.target_user = ' '.join(processing_split[1:])
                self.target_post = POST_NAME[post_name]

    def to_dict(self):
        return {
            'content': self.content,
            'author': self.author,
            'group': self.group,
            'timestamp': self.timestamp,
            'target_user': self.target_user,
            'target_post': self.target_post,
        }

    def __repr__(self):
        return "<Comment (author={})>".format(self.author)
    
    def __str__(self):
        return "<Comment (author={})>".format(self.author)
