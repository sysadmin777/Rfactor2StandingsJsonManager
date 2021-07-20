import os
import uuid
from flask import Flask, render_template, request,flash, redirect, session, send_file
from standings import GetDrivers, GetPosition, GetPoints, ReadStandings, PenaltyGetPosition, PenaltyGetPoints, GetDriverCount, GetRoundCount, AddDriver
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = ['json', 'JSON']
app.secret_key='de3fr4gt5DE#FR$GT%'
app.config['SESSION_TYPE'] = 'filesystem'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def render_static():
    return render_template('index.html')

@app.route("/standings/<id>")
def drivers(id):
    session['classid'] = id
    if session['assesspenalty'] == 1:
            return redirect('/penaltystandings/'+str(id))
    if session['adddriver'] == 1:
            return redirect('/adddriver/'+str(id))
    positionlist = GetPosition(id)
    return render_template('standings.html', positions=positionlist)

@app.route("/penaltystandings/<id>")
def penaltystandings(id):
    positionlist = PenaltyGetPosition(id)
    points = []
    for round in positionlist:
            points.append(round[3])
    return render_template('penaltystandings.html', positions=positionlist, points=points)

@app.route('/penaltygenjson',methods = ['POST'])
def penaltygenjson():
    newpoints = {}
    filename = session['filename']
    tmpfields = []
    tmpfields2 = []
    drivercount = GetDriverCount()
    sepfield = []
    roundcount = GetRoundCount()
    counter = 1
    if request.method == 'POST':
        for fields in request.form:
            if request.form[fields] == '':
                error = 'Point value cannot be empty!'
                return render_template('uploadfile.html', error=error)
            tmpfields.append(request.form[fields])
        for d in range(drivercount):  
            for i in range(roundcount):
                tmpfields2.append(tmpfields[counter - 1])
                counter += 1
            sepfield.append(tuple(tmpfields2))
            tmpfields2.clear()
        gpoints = PenaltyGetPoints(sepfield)
        
    else:
        return "You have to use the form"

    return render_template('newstandings.html', positions=gpoints, filename=filename)

@app.route('/genjson',methods = ['POST'])
def genjson():
    newpoints = {}
    filename = session['filename']
    if request.method == 'POST':
        for fields in request.form:
            if request.form[fields] == '':
                error = 'Point value cannot be empty!'
                return render_template('uploadfile.html', error=error)
            gpoints = GetPoints(fields, int(request.form[fields]))
            newpoints.update({fields: gpoints})
 
    else:
        return "You have to use the form"
    newlist = GetDrivers(newpoints)

    return render_template('newstandings.html', positions=newlist, filename=filename)

@app.route("/uploadstandings")
def upload_file():
    session['assesspenalty'] = 0
    session['adddriver'] = 0
    return render_template('uploadfile.html')

@app.route("/checkstandingfile", methods=['GET', 'POST'])
def check_upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            error = 'No file detected. Please upload a file'
            return render_template('uploadfile.html', error=error)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file and allowed_file(file.filename):
            my_id = uuid.uuid1()
            filename = secure_filename(file.filename)+str(my_id)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            error = 'JSON files only!'
            return render_template('uploadfile.html', error=error)
        f = ReadStandings(filename)
        session['filename'] = filename
        if session['assesspenalty'] == 1:
            return redirect('/penaltystandings/'+str(id))
        if session['adddriver'] == 1:
            return redirect('/adddriver/'+str(id))
        return redirect('/standings/'+str(id))

@app.route("/downloads/<filename>", methods = ['GET'])
def download_file(filename):
    filename=filename
    return send_file('downloads/'+filename, as_attachment=True, attachment_filename='')

@app.route("/uploadpenaltystandings")
def upload_penalty():
    session['assesspenalty'] = 1
    session['adddriver'] = 0
    return render_template('uploadpenaltystandings.html')

@app.route("/uploaddriver")
def upload_driver():
    session['adddriver'] = 1
    session['assesspenalty'] = 0
    return render_template('uploaddriver.html')

@app.route("/adddriver/<id>", methods=['GET', 'POST'])
def add_driver(id):
    return render_template('adddriver.html')


@app.route("/commitdriver", methods=['POST'])
def commit_driver():
    if request.method == 'POST':
        filename = session['filename']
        DriverName = request.form['driverName']
        DriverNumber = request.form['carNumber']
        TeamName = request.form['teamName']
        vehicleName = request.form['vehicleName']
        AddDriver(DriverName, DriverNumber, TeamName, vehicleName)
        return render_template('driveradded.html', filename=filename)
    else:
        return "<h2>Use the form...</h2>"


if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key='de3fr4gt5DE#FR$GT%'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()

