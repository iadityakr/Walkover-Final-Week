from flask import *
import time
import string
from flask_mail import *
from random import *
import random
import mysql.connector as sql
from datetime import datetime
app = Flask(__name__)

mydb = sql.connect(host="tutorial-dakshas.clmbpfr9muzj.ap-south-1.rds.amazonaws.com", user="akash", password="Akash123", database="test")
cur = mydb.cursor()

mail = Mail(app)
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'homea5154@gmail.com'
app.config['MAIL_PASSWORD'] = 'pdzgfoexyepzwzqz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = random.randint(100000, 999999)
str = random.choice(string.ascii_letters)
otp = otp + str


def shuffle(q):
 cur.execute("SELECT * FROM questions;")
 ques = cur.fetchall()
 selected_ques = []
 i = 0
 while i < len(q):
  current_selection = choice(ques)
  current_selection = list(current_selection)
  if current_selection not in selected_ques:
   selected_ques.append(current_selection)
   i = i+1
 return selected_ques

@app.route('/')
def index():
    return render_template("admin1.html")


@app.route('/verify', methods=["POST"])
def verify():
    global email
    email = request.form["email"]
    if email == "aditya7549602102@gmail.com":
        cur.execute("SELECT * FROM submissions")
        submissions = cur.fetchall()
        return  render_template("admin_login.html", sub = submissions)
    msg = Message('OTP', sender='akashkumar8462@gmail.com', recipients=[email])
    msg.body = str(otp)
    mail.send(msg)
    return render_template('admin2.html')


@app.route('/validate', methods=["POST"])
def validate():
    user_otp = request.form['otp']
    if otp == user_otp:
        return render_template("user_login.html")
    return "<h3>failure, OTP does not match</h3>"

@app.route('/attempt', methods=['POST'])
def quiz():
 cur.execute("SELECT * FROM questions;")
 ques = cur.fetchall()
 questions_shuffled = shuffle(ques)
 for i in ques:
  random.shuffle(list(i[1:5]))
 return render_template('main.html', q = questions_shuffled)

@app.route('/quiz', methods=['POST'])
def quiz_answers():
 cur.execute("SELECT * FROM questions;")
 ques = cur.fetchall()
 correct = 0
 for i in ques:
  i = list(i)
  answered = request.form[i[0]]
  if i[5] == answered:
   correct = correct+1
 now = datetime.now()
 cur.execute("INSERT INTO submissions VALUES ('{}','{}',{});".format(email,now,correct))
 mydb.commit()
 return '<h1>Correct Answers: <u>'+str(correct)+'</u></h1>'

@app.route('/add', methods=['POST'])
def save():
 return render_template('save.html')

@app.route('/save', methods=['POST'])
def saving():
 q = request.form.get("ques")
 o1 = request.form.get("opt1")
 o2 = request.form.get("opt2")
 o3 = request.form.get("opt3")
 o4 = request.form.get("opt4")
 ans = request.form.get("ans")
 cur.execute("INSERT INTO questions VALUES ('{}','{}','{}','{}','{}','{}');".format(q, o1, o2, o3, o4, ans))
 mydb.commit()
 return "<h2>Saved Successfully</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


# sudo chown ubuntu:ubuntu -R *
