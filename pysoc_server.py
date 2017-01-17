from flask import Flask, render_template
import rethinkdb as r

app = Flask(__name__)
conn = None
db = None

conn = r.connect(
    host="198.211.123.92",
    port="28015")

db = r.db("sociometric_server")

#print(db.table("client_name").run(conn))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/client")
def api_client():
    return str(list(db.table("client_name").run(conn)))

@app.route("/api/cam/<_clientName>")
def api_cam(_clientName):
    return str(list(db.table(_clientName + "_cam").run(conn)))

@app.route("/api/ir/<_clientName>")
def api_ir(_clientName):
    return str(list(db.table(_clientName + "_ir").run(conn)))

@app.route("/api/mic/<_clientName>")
def api_mic(_clientName):
    return str(list(db.table(_clientName + "_mic").run(conn)))

if __name__ == "__main__":
    app.run()