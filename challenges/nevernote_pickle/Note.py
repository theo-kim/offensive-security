from werkzeug import secure_filename

class Note(object):
    def __init__(self, title, content, image_filename):
        self.title=title
        self.content=content
        self.image_filename=secure_filename(image_filename)

    def get_link(self):
        return '/view/' + secure_filename(self.title) + '.pickle'

    def get_image_link(self):
        return '/img/' + self.image_filename
