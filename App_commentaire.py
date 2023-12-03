from flask import Flask, render_template, request

app = Flask(__name__)

'''Définin l'URL sur laquelle on veut agir'''
'''Nom de la fonction que l'on peut appeler dans le HTML au besoin'''
'''Return render_template --> renvoie sur une page html souhaté dans le dossier "templates"'''
@app.route("/")
def bienvenue():
    return render_template("accueil.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/create_account")
def create_account():
    return render_template("create_account.html")

@app.route("/traitement", methods=["POST"])
def traitement():
    '''request.form --> récupère les données selon le formulaire HTML sous la forme d'un dictionnaire'''
    donnees = request.form
    '''donnees --> dictionnaire et "username" --> clé pour accéder à la données passé par le HTML '''
    '''La clé correspond au nom de la balise dans le fichier HTML'''
    user = donnees['username']
    pw = donnees['password']
    print(user,pw)
    if user == "gwen" and pw == "1234":
        '''return f"Bienvenue {user}, vous êtes connecté."'''
        '''return f"<text>" --> créer une simple page html sans passer par un template...'''
        '''Les accolades permettent de renvoyer le contenue d'une variable (ici "gwen") directement dans la page'''
        return render_template("home.html", name_user=user)
        '''En plus de renvoyer vers un template HTML, on peut également renvoyer un paramètre pour qu'il soit traité dans le code HTML'''
    else:
        '''return "Une erreur est survenue"'''
        return render_template("login.html")
    '''Peut return sur une nouvelle page html potentiellement'''

'''Partie obligatoire'''
if __name__ == '__main__':
    app.run(debug=True)