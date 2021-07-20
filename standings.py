import json
from flask import jsonify, session

def ReadStandings(filename):
    with open('uploads/'+filename, 'r') as myfile:
        classandobj = []
        data=myfile.read()
        obj = json.loads(data)
        classandobj.append(obj)
    return classandobj

def GetObj(filename):
    with open('uploads/'+filename, 'r') as myfile:
        data=myfile.read()
        obj = json.loads(data)
    return obj

def GetDriverCount():
    obj =  GetObj(session['filename'])
    drivers = obj['standings']
    return len(drivers)

def GetRoundCount():
    obj =  GetObj(session['filename'])
    rounds = obj['standings'][0]['rounds']
    return len(rounds)

def GetDrivers(dictPositions):
    obj =  GetObj(session['filename'])
    drivers = obj['standings']
    drivernames = []
    tmp = []
    poscounter = 1
    cposcounter = 1
    for key in dictPositions:
        castpos = 0
        for entries in drivers:
            if entries['position'] == int(key):
                obj['standings'][castpos].update({'previousPosition': int(key)})
                obj['standings'][castpos].update({'previousClassPosition': int(key)})
                drivernames.append({'driverName':entries['driverName'], 'totalPoints':dictPositions[key], 'position':int(key), 'previousPosition':int(key)})
                castpos = 0
            else:
                castpos += 1
   
    sort_drivers = sorted(drivernames, key=lambda x: x['totalPoints'], reverse=True)
    for dictx in sort_drivers:
        dictx.update({'position':poscounter})
        poscounter += 1
        tmp.append(dictx)
   
    for d in tmp:
        castpos = 0
        for e in obj['standings']:
            if d['driverName'] == e['driverName']:
                obj['standings'][castpos].update({'position': cposcounter})
                obj['standings'][castpos].update({'classPosition': cposcounter})
                cposcounter += 1
            else:
                castpos += 1
    sort_obj = sorted(obj['standings'], key=lambda x: x['position'], reverse=False)
    obj['standings'] = sort_obj
    with open('downloads/'+session['filename'], 'w') as outfile:
        json.dump(obj, outfile, indent=4)
    return tmp

def PenaltyGetPosition(id):
    positions = []
    obj =  GetObj(session['filename'])
    sort_obj = sorted(obj['standings'], key=lambda x: x['position'], reverse=False)
    obj['standings'] = sort_obj
    with open('uploads/'+session['filename'], 'w') as outfile:
        json.dump(obj, outfile, indent=4)
    obj =  GetObj(session['filename'])

    drivers = obj['standings']
    for entries in drivers:
        positions.append((entries['driverName'],entries['position'],entries['previousPosition'],entries['rounds']))
    sort_positions = sorted(positions, key=lambda x: x[1], reverse=False)
    return sort_positions

def GetPosition(id):
    positions = []
    obj =  GetObj(session['filename'])
    sort_obj = sorted(obj['standings'], key=lambda x: x['position'], reverse=False)
    obj['standings'] = sort_obj
    with open('uploads/'+session['filename'], 'w') as outfile:
        json.dump(obj, outfile, indent=4)
    obj =  GetObj(session['filename'])

    drivers = obj['standings']
    for entries in drivers:
        positions.append((entries['driverName'],entries['position'],entries['previousPosition']))
    sort_positions = sorted(positions, key=lambda x: x[1], reverse=False)
    return sort_positions

def PenaltyGetPoints(points):
    obj =  GetObj(session['filename'])
    sort_obj = sorted(obj['standings'], key=lambda x: x['position'], reverse=False)
    obj['standings'] = sort_obj
    with open('uploads/'+session['filename'], 'w') as outfile:
        json.dump(obj, outfile, indent=4)
    obj =  GetObj(session['filename'])
    drivers = obj['standings']
    totalpoints = 0
    counter = 0
    driverlist = []
    pos = 1
    for p in points:
        totalpoints = 0
        counter = 0
        for pp in p:
            if pp == 'None':
                obj['standings'][pos-1]['rounds'][counter].update({'points': None})
                counter += 1
            else:
                obj['standings'][pos-1]['rounds'][counter].update({'points': int(pp)})
                totalpoints += int(pp)
                obj['standings'][pos-1].update({'totalPoints': totalpoints})        
                counter += 1
        currentpos = obj['standings'][pos-1]['position']
        obj['standings'][pos-1]['previousPosition'] = currentpos
        pos += 1

    sort_obj = sorted(obj['standings'], key=lambda x: x['totalPoints'], reverse=True)
    obj['standings'] = sort_obj

    newpos = 1
    for entry in obj['standings']:
        obj['standings'][newpos - 1]['position'] = newpos
        newpos += 1

    with open('downloads/'+session['filename'], 'w') as outfile:
        json.dump(obj, outfile, indent=4)
    
    with open('uploads/'+session['filename'], 'w') as outfile:
        json.dump(obj, outfile, indent=4)

    obj =  GetObj(session['filename'])
    drivers = obj['standings']

    for entries in drivers:
        driverlist.append({'driverName':entries['driverName'], 'totalPoints':entries['totalPoints'], 'position':entries['position'], 'previousPosition':entries['previousPosition']})

    return driverlist

def GetPoints(pos,points):
    obj =  GetObj(session['filename'])
    sort_obj = sorted(obj['standings'], key=lambda x: x['position'], reverse=False)
    obj['standings'] = sort_obj
    with open('uploads/'+session['filename'], 'w') as outfile:
        json.dump(obj, outfile, indent=4)
    obj =  GetObj(session['filename'])
    drivers = obj['standings']
    allpoints = []
    totalpoints = 0
    counter = 0
    for entries in drivers:
        if int(pos) == entries['position']:
            allpoints.append(entries['rounds'])
    for value in allpoints[0]:
        if value['points'] == None:
            continue
        else:
            totalpoints += int(value['points'])
    totalpoints += points
    castpos = int(pos) - 1
    test = obj['standings'][int(castpos)]['rounds']
    for i in test:
        if i['points'] == None:
            obj['standings'][castpos]['rounds'][counter].update({'points': int(points)})
            break
        else:
            counter += 1
    obj['standings'][castpos].update({'totalPoints': totalpoints})
    with open('uploads/'+session['filename'], 'w') as outfile:
        json.dump(obj, outfile, indent=4)
    return totalpoints

def AddDriver(DriverName, DriverNumber, TeamName, vehicleName):
    obj =  GetObj(session['filename'])
    sort_obj = sorted(obj['standings'], key=lambda x: x['position'], reverse=False)
    obj['standings'] = sort_obj
    with open('uploads/'+session['filename'], 'w') as outfile:
        json.dump(obj, outfile, indent=4)
    obj =  GetObj(session['filename'])
    roundcount = obj['totalRounds']
    nullpoints = []
    position = len(obj['standings']) + 1
    previousPosition = position
    for i in range(roundcount):
        nullpoints.append({"points": None})
    obj['standings'].append({'position': position, \
        "classPosition": position, \
        "previousPosition": previousPosition, \
        "previousClassPosition": previousPosition, \
        "carNumber":  DriverNumber, \
        "driverName": DriverName, \
        "teamName": TeamName, \
        "vehicleName": vehicleName, \
        "vehicleFile": "VEHICLEFILEHERE.VEH", \
        "carClass": "Default", \
        "totalPoints": 0, \
        "rounds": nullpoints})
    sort_obj = sorted(obj['standings'], key=lambda x: x['position'], reverse=False)
    obj['standings'] = sort_obj
    
    with open('uploads/'+session['filename'], 'w') as outfile:
        json.dump(obj, outfile, indent=4)

    with open('downloads/'+session['filename'], 'w') as outfile:
        json.dump(obj, outfile, indent=4)

