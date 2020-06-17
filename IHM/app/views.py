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
    # On recupere de datetime.now l'annee & le jour et on le stocke
    annee = str(d)[:4]
    jour = str(d)[:10]
    repertoire = './temperatures/' + annee + '/'
    # On verifie que le repertoire existe. S'il n'existe pas : on le cree
    if not os.path.isdir(repertoire):
        os.makedirs(repertoire)
    fich_Temp = repertoire + jour + '.txt'
    # On ouvre le fichier ayant pour nom la date_du_jour.txt en fonction de s'il existe ou pas : en add ou en write
    if os.path.exists(fich_Temp):
        # Le fichier existe, on l'ouvre en mode ajout
        f = open(fich_Temp, "a")
    else:
        # Le fichier n'existe pas, on le cree et on l'ouvre
        f = open(fich_Temp, "w")
    # Enfin, on ajoute une ligne dans le fichier au format : HH:MM Temp _ Exemple : 10:15 27.02
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
        # On a entre 192.xx.xx.xx/graphTemp sans indiquer de date, on affiche donc le graph du jour
        d = datetime.now()
        titre = "Temperature actuelle : " + str(get_temp(False))
    else:
        # Sinon, on affiche le graph de la date donnee | Ex : 192.xx.xx.xx/graphTemp/20180618
        d = datetime.strptime(date, '%Y%m%d')
        # Les 6 prochaines lignes permettent d'avoir un titre type : 08/09/2018 au lieu de 8/9/2018
        strMonth = str(d.month)
        strDay = str(d.day)
        if len(strMonth) == 1:
            strMonth = "0" + strMonth
        if len(strDay) == 1:
            strDay = "0" + strDay
        dateTitle = strDay + "/" + strMonth + "/" + str(d.year)
        titre = "Statistiques du " + dateTitle
    # Liste contenant deux liste :
    # pointsAndTemp[0] : coordonnees des points du graph;
    # pointsAndTemp[1] : temperatures, permet de faire des stats : max,min,moy
    pointsAndTemp = fichierVersListe(
        "./temperatures/" + str(d)[:4] + "/" + str(d)[:10] + ".txt")
    temperatures = pointsAndTemp[1]
    # On calcule des dates precedantes et suivantes pour la navigation entre les jours
    nextDate = d + timedelta(days=1)
    prevDate = d - timedelta(days=1)
    # On retourne tout a la page graphTemp.html
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
