#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kristjan.vilgo
#
# Created:     16.03.2018
# Copyright:   (c) kristjan.vilgo 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from __future__ import print_function

import os
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from SEND_REPORT_EMAIL import send_report_email


ALLOWED_EXTENSIONS = set(['xml'])

# http://127.0.0.1:5000/
# flask run --host=0.0.0.0 # to make visible for all

app = Flask(__name__)
app.secret_key = 'katsetuste_arvuti'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "recieved_files")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def instructions():
    return '<a href="/ESTFEED_INBOUND">Service to recive EstFeed push files -> /ESTFEED_INBOUND</a>'

@app.route('/ESTFEED_INBOUND', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        raw_header_data = request.headers
        raw_data        = request.data
        #raw_data = request.__dict__["environ"]["wsgi.input"].read()#request.get_data()#request.input_stream.read(0)
        send_report_email("New request recieved", "raw header:\n{}\n raw data \n {}".format(raw_header_data, raw_data), ["kristjan.vilgo@elering.ee, georg.rute@elering.ee"],[])
        #print(raw_data)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            file_full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(file_full_path)

            send_report_email("New file recieved", "Recived file is attached, raw header:\n{}\n raw data \n {}".format(raw_header_data, raw_data), ["kristjan.vilgo@elering.ee, georg.rute@elering.ee"],[file_full_path])


            return '''File recieved: {}'''.format(filename)

    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload .xml files only</h1>
    <form method=post enctype=multipart/related>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0', port=80)

