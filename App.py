from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///zestviewdata.db'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return '<Name %r>' %self.id

@app.route("/")
def bienvenue():
    #A modifier pour push dans le main -> remettre home.html
    return render_template("accueil.html")

@app.route("/adminpanel",methods=['POST','GET'])


def adminpanel():
    if request.method =="POST":
        #Creating new user from HTML form
        new_user = Users(name=request.form['username'],password=request.form['password']) # type: ignore

        #Push to db
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/adminpanel')
        except:
            return "Error"

    else:
        userlist = Users.query.order_by(Users.id)
        return render_template("adminpanel.html",userlist=userlist)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/create_account")
def create_account():
    return render_template("create_account.html")

@app.route("/traitement", methods=["POST"])

def traitement():
    donnees = request.form
    user = donnees['username']
    pw = donnees['password']
    print(user,pw)
    if user == "gwen" and pw == "1234":
        '''return f"Bienvenue {user}, vous êtes connecté."'''
        return render_template("home.html", name_user=user)
    else:
        '''return "Une erreur est survenue"'''
        return render_template("login.html")
    '''Peut return sur une nouvelle page html potentiellement'''


if __name__ == '__main__':
    app.run(debug=True)