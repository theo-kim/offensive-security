#!/usr/bin/env python3

from flask import Flask, render_template, send_from_directory, request, redirect
from werkzeug import secure_filename
from Note import Note

import subprocess # sometimes i just like to import subprocess ¯\_(ツ)_/¯
import pickle
import os

NOTE_FOLDER='notes/'

def save_note(note, image):
    note_file=open(NOTE_FOLDER + secure_filename(note.title + '.pickle'), 'wb')
    note_file.write(pickle.dumps(note))
    note_file.close()

    image.save(NOTE_FOLDER + note.image_filename)

def load_note(note_name):
    print(note_name)
    note_file=open(NOTE_FOLDER + note_name, 'rb')
    a = pickle.loads(note_file.read())
    print(a)
    # print(a.title)
    return a

def load_all():
    notes=[]
    for filename in os.listdir(NOTE_FOLDER):
        if filename.endswith('.pickle'):
            notes.append(load_note(filename))
    return notes


app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', notes=load_all())

@app.route('/view/<file_name>')
def note_view(file_name): 
    ##################################################################
    # let me go ahead and unpickle whatever file is being requested...
    ##################################################################
    note=load_note(file_name)
    return render_template('view.html', note=note)

@app.route('/img/<file_name>')
def note_image(file_name):
    ##################################################################
    # let me go ahead and send whatever file is being requested...
    ##################################################################
    return send_from_directory(NOTE_FOLDER, file_name)

@app.route('/new', methods=['GET', 'POST'])
def note_new():
    if request.method == "POST":
        image=request.files.get('image')
        if not image.filename.endswith('.png'):
            return 'nah bro png images only!', 403
        new_note=Note(
            request.form.get('title'),
            request.form.get('content'),
            image_filename=image.filename
        )
        save_note(new_note, image)
        return redirect(new_note.get_link())
    return render_template('new.html')

if __name__ == "__main__":
    app.run(
        # host='0.0.0.0',
        # port=5000
    )
