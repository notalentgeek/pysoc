from   flask          import Flask, render_template
from   flask_socketio import emit
from   flask_socketio import SocketIO               as sio
import rethinkdb      as     r

def ConnDB():

    conn = r.connect(
        host="198.211.123.92",
        port="28015")

    db = r.db("sociometric_server")

    return [conn, db]

app = Flask(__name__)
sIO = sio(app)

cDB = ConnDB()
conn = cDB[0]
db = cDB[1]

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/api/client")
def APIClient():
    return str(list(db.table("client_name").run(conn)))
@app.route("/api/cam/<_clientName>")
def APICam(_clientName):
    return str(list(db.table(_clientName + "_cam").run(conn)))
@app.route("/api/ir/<_clientName>")
def APIIR(_clientName):
    return str(list(db.table(_clientName + "_ir").run(conn)))
@app.route("/api/mic/<_clientName>")
def APIMic(_clientName):
    return str(list(db.table(_clientName + "_mic").run(conn)))

@sIO.on("latestInputRequest")
def LatestInput():

    clientList      = []
    latestInput     = None
    latestInputComp = None

    clientNameArray = None
    camTable        = None
    irTable         = None
    micTable        = None

    userDictArray   = [];

    try: clientNameArray = list(db.table("client_name").run(conn))
    except r.errors.ReqlOpFailedError as error: clientNameArray = None

    if clientNameArray != None:

        for c in clientNameArray:

            clientList.append(c.get("client_name"))

            latestInputTemp = c.get("latest_input")
            latestInputCompTemp = float(latestInputTemp)/1000

            if latestInputComp == None:

                latestInput = latestInputTemp
                latestInputComp = latestInputCompTemp

            if latestInputComp < latestInputCompTemp:

                latestInput = latestInputTemp
                latestInputComp = latestInputCompTemp

        for c in clientList:

            userDict = {};
            userDict["client_name"] = c;


            try:
                db.table(c + "_cam").run(conn)
                camTable = db.table(c + "_cam")
            except r.errors.ReqlOpFailedError as error: camTable = None

            try:
                db.table(c + "_ir").run(conn)
                irTable = db.table(c + "_ir")
            except r.errors.ReqlOpFailedError as error: irTable = None

            try:
                db.table(c + "_mic").run(conn)
                micTable = db.table(c + "_mic")
            except r.errors.ReqlOpFailedError as error: micTable = None

            if camTable != None:

                camTableConn = camTable.get(latestInput).run(conn)
                if camTableConn: userDict["faces"] = camTableConn.get("faces")

            if irTable != None:

                irTableConn = irTable.get(latestInput).run(conn)
                if irTableConn: userDict["ir_code"] = irTableConn.get("ir_code")

            if micTable != None:

                micTableConn = micTable.get(latestInput).run(conn)

                if micTableConn:
                    userDict["pitch"] = micTableConn.get("pitch")
                    userDict["volume"] = micTableConn.get("volume")

            userDictArray.append(userDict)

        emit("latestInputSend", userDictArray)

if __name__ == "__main__":
    sIO.run(app)