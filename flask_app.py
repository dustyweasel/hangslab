from flask import Flask, request, redirect, session
import cgi
import os
import jinja2
import random

template_dir = os.path.join(os.path.dirname(__file__),'templates')

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)

app.config['DEBUG'] = True

app.secret_key="hi"

def filegrabber():
    ix=0
    for filenames in os.listdir("/home/laconiclizard/mysite/static/mainimages/silestone"):
    #for filenames in os.listdir("./static/mainimages/silestone"):
        ix+=1

    num=random.randint(1,ix)

    ix=0
    for filenames in os.listdir("/home/laconiclizard/mysite/static/mainimages/silestone"):
    #for filenames in os.listdir("./static/mainimages/silestone"):
        ix+=1
        if(ix>=num):
            return filenames

    return NULL;

#slabpic=filegrabber()
#letters_guessed=""
#secret_word=slabpic[0:len(slabpic)-3]
MAXGUESSES=10
#guesses_left=MAXGUESSES
#gameover=0

@app.route("/", methods=['GET','POST'])
def index():
    #global secret_word
    #global letters_guessed
    #global slabpic
    global MAXGUESSES
    #global guesses_left
    #global gameover

    letter=""
    if request.method == 'POST' and session['gameover'] == 0:
        try:
            letter=request.form['letter']
            if(letter and len(letter)==1 and letter[0].isalpha() and letter not in session['letters_guessed']):
                session['letters_guessed']=session['letters_guessed']+letter.upper()
                if(letter not in session['secret_word']):
                    session['guesses_left']-=1
                    if(session['guesses_left']<=0):
                        session['gameover']=1
                else:
                    session['gameover']=2
                    for ix in range(len(session['secret_word'])):
                        if(session['secret_word'][ix].isalpha() and session['secret_word'][ix] not in session['letters_guessed']):
                            session['gameover']=0
        except KeyError:
            letter="#"

    elif request.method == 'POST':
        try:
            val=request.form['next']
            session['slabpic']=filegrabber()
            session['letters_guessed']=""
            session['secret_word']=session['slabpic'][0:len(session['slabpic'])-3]
            session['guesses_left']=MAXGUESSES
            session['gameover']=0
        except KeyError:
            val="oops"

    else:
        if 'slabpic' not in session:
            session['slabpic']=filegrabber()
            session['letters_guessed']=""
            session['secret_word']=session['slabpic'][0:len(session['slabpic'])-3]
            session['guesses_left']=MAXGUESSES
            session['gameover']=0

    hidden_word=""
    for ix in range(len(session['secret_word'])):
        if(ix!=0):
            hidden_word+=" "
        if(session['secret_word'][ix] in session['letters_guessed']):
            hidden_word+=session['secret_word'][ix]
        elif(not session['secret_word'][ix].isalpha()):
            hidden_word+=chr(160)
        else:
            hidden_word+="_"
    #/home/laconiclizard/mysite/templates/hangslab.html
    template = jinja_env.get_template('hangslab.html')
    return template.render(guessed_letters=session['letters_guessed'], underscore_word=hidden_word, loadimage=session['slabpic'], tries_left=session['guesses_left'], total_guesses=MAXGUESSES, state=session['gameover'])

#added this after upload
if __name__ == '__main__':
    app.run()
