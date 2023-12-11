from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///zestviewdata.db'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    cat1 = db.Column(db.String(20))
    cat2 = db.Column(db.String(20))
    cat3 = db.Column(db.String(20))
    privilege = db.Column(db.String(10),nullable=False)

    def __repr__(self):
        return '<Name %r>' %self.id

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(25),nullable=False)
    link = db.Column(db.String(50),nullable=False)
    title = db.Column(db.String(255),nullable=False)
    rating = db.Column(db.Integer)

@app.route("/")
def bienvenue():
    return render_template("accueil.html")

@app.route("/adminpanel",methods=['POST','GET'])
def adminpanel():

    #Add User
    if request.method == 'POST' and request.form['action'] == 'add_user':
        # Creating new user from HTML form
        new_user = Users(
            username=request.form['username'],
            password=request.form['password'],
            cat1=request.form['cat1'],
            cat2=request.form['cat2'],
            cat3=request.form['cat3'],
            privilege=request.form['privilege']) #type:ignore

        # Push to db
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/adminpanel')
        except:
            return "Error Adding User to DB"
        
    #Update User Data
    elif request.method == 'POST' and request.form['action'] == 'update_user_data':
        try:
            record = Users.query.get(request.form['userid'])
            record.username = request.form['username']#type: ignore
            record.password=request.form['password']#type: ignore
            record.privilege=request.form['privilege']#type: ignore
            db.session.commit()
            return redirect('/adminpanel')
        except:
            return "Error updating Data"
        
    #Delete User
    elif request.method == 'POST' and request.form['action'] =='delete_user':
        try:
            db.session.delete(Users.query.get(request.form['userid']))
            db.session.commit()
            return redirect('/adminpanel')
        except:
            return "Error, no User is associated with this ID."
        
    #Add Video
    elif request.method == 'POST' and request.form['action'] == 'add_video':
        # Creating new video from HTML form
        """ MODIFIER POUR INITIALISER LA VALEUR DU RATING A 0 """
        new_video = Video(
            category=request.form['category'],
            link=request.form['link'],
            title=request.form['title']) #type:ignore

        # Push to db
        try:
            db.session.add(new_video)
            db.session.commit()
            return redirect('/adminpanel')
        except:
            return "Error Adding Video to DB"
        
    #Update Video Data
    elif request.method == 'POST' and request.form['action'] == 'update_video_data':
        try:
            record = Video.query.get(request.form['videoid'])
            record.category=request.form['category'] #type:ignore
            record.link=request.form['link'] #type:ignore
            record.title=request.form['title'] #type:ignore
            db.session.commit()
            return redirect ('/adminpanel')
        except:
            return "Error updating Video Data"

    #Delete Video
    elif request.method == 'POST' and request.form['action'] =='delete_video':
        try:
            db.session.delete(Video.query.get(request.form['videoid']))
            db.session.commit()
            return redirect('/adminpanel')
        except:
            return "Error, no Video is associated with this ID."
        
    #SQL QUERY
    elif request.method == 'POST' and request.form['action'] == 'execute_query':
        user_input = request.form['sql_query']
        result = db.session.execute(text(user_input)) #type:ignore
        
        result = [row[0] for row in result]

        # If not requested from the adminpanel page, formating result for better compatibility
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(result) 
        
        # Process the result or send it to the template
        return render_template('adminpanel.html', result=result)
    userlist = Users.query.order_by(Users.id)
    vidlist = Video.query.order_by(Video.id)
    return render_template("adminpanel.html", userlist=userlist,vidlist=vidlist)

        
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