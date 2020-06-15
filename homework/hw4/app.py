from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/orders', methods=['POST'])
def write_orders():
    orderName_receive = request.form['orderName_give']
    orderSelect_receive = request.form['orderSelect_give']
    orderAddress_receive = request.form['orderAddress_give']
    orderPhone_receive = request.form['orderPhone_give']

    order = {
      'orderName': orderName_receive,
      'orderSelect': orderSelect_receive,
      'orderAddress': orderAddress_receive,
      'orderPhone': orderPhone_receive
    }

    db.orders.insert_one(order)

    return jsonify({'result': 'success', 'msg': '주문이 완료되었습니다.'})


@app.route('/orders', methods=['GET'])
def read_orders():
    orders = list(db.orders.find({},{'_id':0}))
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
