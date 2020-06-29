from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
import os
import parsecontent

app = Flask(__name__)

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)
db = client.gittracker

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/addRepo', methods=['POST'])
def write_repo():
    trackerGithubUrl_receive = request.form['trackerGithubUrl']
    trackerComment_receive = request.form['trackerComment']

    trackerContent = parsecontent.getContent(trackerGithubUrl_receive)
    trackerReadme = parsecontent.getReadme(trackerGithubUrl_receive)

    repo = {
        'trackerContent': trackerContent,
        'trackerReadme': trackerReadme,
        'trackerComment': trackerComment_receive
    }

    db.repos.insert_one(repo)

    return jsonify({'result': 'success', 'msg': '추가완료'})
    # add repository default information (url, user comment)


@app.route('/getRepo', methods=['GET'])
def read_repo():
    repos = list(db.repos.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'repos': repos})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
