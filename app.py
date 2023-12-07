from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///zestviewdata.db'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return '<Name %r>' %self.id

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(25),nullable=False)
    link = db.Column(db.String(50),nullable=False)
    title = db.Column(db.String(255),nullable=False)
    rating = db.Column(db.Integer)

"""@app.route("/")
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
"""
@app.route('/')
def index():
    return render_template('execute_query.html')  # Render the execute_query form

@app.route('/execute_query', methods=['POST'])
def execute_query():
    user_input = request.form.get('sql_query')
    
    # Use SQLAlchemy ORM to perform safe database operations
    result = db.session.execute(text(user_input)) #type:ignore

    names = [row[0] for row in result]

    print("Data in 'names' :",names)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(names)
    
    # Process the result or send it to the template
    return render_template('result.html', result=names)

if __name__ == '__main__':
    app.run(debug=True)