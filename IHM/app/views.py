from flask import render_template, redirect, request
from datetime import datetime, timedelta
import os

from app import app, nucleo


def get_temp(sauvegardeStatus):
    nucleo_board = nucleo.Nucleo()
    temperature = nucleo_board.get_value()
    nucleo_board.close()
    if sauvegardeStatus == True:
        enregistrement(temperature)
    return temperature


def enregistrement(temperature):
    d = datetime.now()
    annee = str(d)[:4]
    jour = str(d)[:10]
    repertoire = './temperatures/' + annee + '/'
    if not os.path.isdir(repertoire):
        os.makedirs(repertoire)
    fich_Temp = repertoire + jour + '.txt'
    if os.path.exists(fich_Temp):
        f = open(fich_Temp, "a")
    else:
        f = open(fich_Temp, "w")
    time = d.strftime("%H:%M")
    print(str(time) + " " + str(temperature), file=f)
    f.close()


def fichierVersListe(cheminFich):
    f = open(cheminFich, "r")
    points = []
    temperatures = []
    for line in f:
        points.append([line[0:2], line[3:5], line[6:len(line) - 1]])
        temperatures.append(float(line[6:len(line) - 1]))
    f.close()
    return [points, temperatures]


def moyenneListe(liste):
    res = 0
    for i in liste:
        res += i
    return (res/len(liste))


@app.route('/')
def index():
    return graphTemp(None)


@app.route("/<date>")
def graphTemp(date):
    if date is None:
        d = datetime.now()
        titre = "Température actuelle : " + str(get_temp(False)) + " °C"
    else:
        d = datetime.strptime(date, '%Y%m%d')
        strMonth = str(d.month)
        strDay = str(d.day)
        if len(strMonth) == 1:
            strMonth = "0" + strMonth
        if len(strDay) == 1:
            strDay = "0" + strDay
        dateTitle = strDay + "/" + strMonth + "/" + str(d.year)
        titre = "Statistiques du " + dateTitle
    pointsAndTemp = fichierVersListe(
        "./temperatures/" + str(d)[:4] + "/" + str(d)[:10] + ".txt")
    temperatures = pointsAndTemp[1]
    nextDate = d + timedelta(days=1)
    prevDate = d - timedelta(days=1)
    return render_template(
        'index.html',
        d=d.strftime("%Y-%m-%d"),
        titre=titre,
        temp=get_temp(True),
        points=pointsAndTemp[0],
        tempMin=round(min(temperatures), 1),
        tempMax=round(max(temperatures), 1),
        tempMoy=round(moyenneListe(temperatures), 1),
        prevDate=prevDate.strftime("%Y%m%d"),
        nextDate=nextDate.strftime("%Y%m%d")
    )


@app.route('/send', methods=['POST'])
def send():
    nucleo_board = nucleo.Nucleo()
    temperature = request.form['temperature']
    nucleo_board.send_value(temperature)
    nucleo_board.close()
    return redirect('/', code=302)


@app.errorhandler(404)
def redirected(error):
    return redirect('/', code=302)
