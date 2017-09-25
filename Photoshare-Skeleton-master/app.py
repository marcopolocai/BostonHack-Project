######################################
# author ben lawson <balawson@bu.edu> 
######################################
# Some code adapted from 
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask.ext.login as flask_login

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '7896320145'
app.config['MYSQL_DATABASE_DB'] = 'teamformation'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users") 
users = cursor.fetchall()

def getUserList():
    cursor = conn.cursor()
    cursor.execute("SELECT email from Users") 
    return cursor.fetchall()

def getSkillId(name):
    cursor = conn.cursor()
    cursor.execute("SELECT skill_id FROM Skills WHERE name = '{0}'".format(name))
    return cursor.fetchone()[0]

def getUserSkills(uid):
    cursor = conn.cursor()
    # uid = getUserIdFromEmail(email)
    cursor.execute("SELECT name FROM Skills JOIN (SELECT skill_id FROM Owns WHERE user_id = '{0}' ) temp on temp.skill_id = Skills.skill_id".format(uid))
    return [x[0] for x in cursor.fetchall()] #NOTE list of tuples, [(imgdata, pid), ...]

def getUserIdFromEmail(email):
    cursor = conn.cursor()
    cursor.execute("SELECT user_id  FROM Users WHERE email = '{0}'".format(email))
    return cursor.fetchone()[0]

'''
A new page looks like this:
@app.route('new_page_name')
def new_page_function():
    return new_page_html
'''

#you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html', supress='True')  

@app.route("/register", methods=['POST'])
def register_user():
    try:
        email=request.form.get('email')
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        skills=request.form.get('skills')
    except:
        print "couldn't find all tokens" #this prints to shell, end users will not see this (all print statements go to shell)
        return flask.redirect(flask.url_for('register'))
    cursor = conn.cursor()
    test =  isEmailUnique(email)
    if test:
        print cursor.execute("INSERT INTO Users (email, fname, lname) VALUES ('{0}', '{1}', '{2}')".format(email, fname, lname))
        conn.commit()
        enterUserSkills(email, skills)

        return flask.redirect('http://127.0.0.1:5000/')
    else:
        print "email is not unique"
        return render_template('register.html')
        # return flask.redirect('http://127.0.0.1:5000/')

def enterUserSkills(email, skills):
    skills = skills.split(',')
    for  skill in skills:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Skills (name) VALUES ('{0}')".format(skill))
        except:
            print skill
        sid = getSkillId(skill)
        uid = getUserIdFromEmail(email)
        try:
            cursor.execute("INSERT INTO Owns (user_id,skill_id) VALUES ('{0}','{1}')".format(uid,sid))
        except:
            print "Error enterUserSkills"
        conn.commit()
    print 'skills recorded'

def isEmailUnique(email):
    #use this to check if a email has already been registered
    cursor = conn.cursor()
    if cursor.execute("SELECT email  FROM Users WHERE email = '{0}'".format(email)): 
        #this means there are greater than zero entries with that email
        return False
    else:
        return True

#task page
@app.route("/task", methods=['GET'])
def task():
    return render_template('task.html', supress='True')  

@app.route("/task", methods=['POST'])
def cover_task():
    try:
        name=request.form.get('name')
        skills=request.form.get('skills')
    except:
        print "couldn't find all tokens" #this prints to shell, end users will not see this (all print statements go to shell)
        return flask.redirect(flask.url_for('task'))
    skills = skills.split(',')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id,fname,lname FROM Users ")
    usersInfo =  [list(x) + [getUserSkills(x[0])] for x in list(cursor.fetchall())]

    print skills 
    print name 
    return render_template('task.html', message = greedy_cover(usersInfo, skills))
    print greedy_cover(usersInfo, skills)

def greedy_cover(users, uncovered):
    uncovered = set(uncovered)
    max_intercept = 0 
    output = []
    best = 0 
    while len(uncovered)>0:
        for i in range(len(users)):
            user = users[i]
            temp = len(set(user[3]) & uncovered)
            if temp>max_intercept:
                max_intercept = temp
                best = i
        uncovered = uncovered - set(users[best][3])
        output.append(users[best])
        del users[best]
    return output


#default page  
@app.route('/', methods=['GET'])
def hello():
    cursor = conn.cursor()
    cursor.execute("SELECT user_id,fname,lname FROM Users ")
    usersInfo = [list(x) + [', '.join(getUserSkills(x[0]))] for x in list(cursor.fetchall())]
    # print usersInfo
    return render_template('hello.html', message='Welecome to Team Formation', participants = usersInfo)


if __name__ == "__main__":
    #this is invoked when in the shell  you run 
    #$ python app.py 
    app.run(port=5000, debug=True)
