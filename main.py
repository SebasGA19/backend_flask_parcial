import hashlib
import flask
import time
import jwt
from datetime import datetime, timedelta
import flask
import sqlite3
from flask import g
DATABASE = 'database.db'

app = flask.Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/login", methods=["POST"])
def login():
    conn = get_db_connection()
    req = flask.request.get_json()
    username = req["username"]
    password = hashlib.sha512(req["password"].encode()).hexdigest()
    user = conn.execute(
        'SELECT id, username, password FROM users WHERE username = ? AND password = ?', (username, password)).fetchall()
    data =[]
    for row in user:
        data.append({
            'id': row[0]
        })
    id = data[0]['id']
    conn.close()
    if user is not None:
        return flask.jsonify({"jwt": jwt.new_jwt(id, username)})
    return "Unauthorized", 401


@app.route("/products", methods=["POST"])
def products():
    if "Session" not in flask.request.headers:
        return "Unauthorized", 401
    jwt_payload = jwt.authorize(flask.request.headers["Session"])
    print(jwt_payload)
    if jwt_payload is None:
        return "Unauthorized", 401
    conn = get_db_connection()
    # req = flask.request.get_json()
    products = conn.execute('SELECT * FROM products').fetchall()
    data = []
    for row in products:
        data.append({
            'id': row[0],
            'name': row[2],
            'store': row[3],
            'image_url': row[4],
            'raing': row[5]
        })
    conn.close()
    if products is not None:
        return flask.jsonify(data)
    return "Unauthorized", 401

@app.route("/favorites", methods=["PUT", "POST", "DELETE"])
def addFavorites():
    if "Session" not in flask.request.headers or not jwt.authorize(flask.request.headers["Session"]):
        return "Unauthorized", 401
    request = flask.request
    jwt_payload = jwt.authorize(flask.request.headers["Session"])
    conn = get_db_connection()
    
    if request.method == "POST":
        products = conn.execute('SELECT * FROM favorites WHERE user_id = ?',(jwt_payload["id"],)).fetchall()
        data = []
        for row in products:
            data.append({
                'product_id': row[2],
                'user_id': row[3]
            })
        conn.close()
        if products is not None:
            return flask.jsonify(data)
        return "Unauthorized", 401
    
    if request.method == "PUT":
        try:
            req = flask.request.get_json()
            product_id = req["product_id"]
            user_id = jwt_payload["id"]
            conn.execute('INSERT INTO favorites (product_id, user_id) VALUES (?, ?)',(product_id, user_id))
            conn.commit()
            conn.close()
            return "Favorites added succesfully"
        except:
            return "Already in favorites", 409
    
    if request.method == "DELETE":
        req = flask.request.get_json()
        product_id = req["product_id"]
        user_id = jwt_payload["id"]
        conn.execute('DELETE FROM favorites WHERE product_id= ? AND user_id= ?',(product_id, user_id))
        conn.commit()
        conn.close()
        return "Favorites deleted succesfully"

@app.route("/valid", methods=["POST"])
def valid():
    req = flask.request.get_json()
    return flask.jsonify({"valid": jwt.authorize(req["jwt"])})


def main():
    app.run("0.0.0.0", 5000)


if __name__ == "__main__":
    main()
