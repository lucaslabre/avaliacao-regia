from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Rota para listar dados
@app.route("/companhias", methods=["GET"])
def listar_companhias():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM companhias")
    rows = cursor.fetchall()

    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)
