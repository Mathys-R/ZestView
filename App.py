from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///friends.db'

db = SQLAlchemy(app)

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return '<Name %r>' %self.id

@app.route("/")
def bienvenue():
    return render_template("accueil.html")

@app.route("/friends",methods=['POST','GET'])


def friends():
    if request.method =="POST":
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name) # type: ignore

        #push to db
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "Error"
    else:
        friends = Friends.query.order_by(Friends.name)
        return render_template("friends.html",friends=friends)

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