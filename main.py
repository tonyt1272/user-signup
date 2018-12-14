from flask import Flask, request, redirect, render_template
import cgi
import re

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

##
@app.route("/")
def index():
	
    ##Regenerates Username
    if request.args.get("form_name"):
        user_name1 =  request.args.get("form_name")
    else:
        user_name1 = ''
    ##----------

    ##Regenerates email
    if request.args.get("form_email"):
        e_mail1 =  request.args.get("form_email")
    else:
        e_mail1 = ''
    ##----------

    ##Extract error values from previous form submission if they exist
    user_name_error1 = request.args.get("user_name_error")
    pass_word_error1 = request.args.get("pass_word_error")
    vpass_word_error1 = request.args.get("vpass_word_error")
    e_mail_error1 = request.args.get("e_mail_error")
    return render_template('index.html', form_name=user_name1, form_email=e_mail1, 
    user_name_error=user_name_error1 and cgi.escape(user_name_error1, quote=True),
    pass_word_error=pass_word_error1 and cgi.escape(pass_word_error1, quote=True),
    vpass_word_error=vpass_word_error1 and cgi.escape(vpass_word_error1, quote=True),
    e_mail_error=e_mail_error1 and cgi.escape(e_mail_error1, quote=True))
    ##----------


##Extract form data
@app.route("/submit", methods=['POST'])
def form_submission():
    form_error = False
    user_name = request.form['user_name']
    pass_word =	request.form['pass_word']
    vpass_word = request.form['vpass_word']
    e_mail = request.form['e_mail']
    cgi.escape(e_mail, quote=True)
    cgi.escape(user_name, quote=True)
    error_list=['None','None', 'None', 'None', user_name, e_mail]
##-------------

    ##username validation
    if not user_name:
        error_list[0] = "Please enter a valid username"
        # error_list[4] = ""
        # user_name='None'        
        form_error=True

    if " " in user_name:
        error_list[0] = "Username must not contain spaces"
        # error_list[4] = ""
        # user_name='None'
        form_error=True

    if len(user_name)<3 and len(user_name)>=1:
        error_list[0] = "Username too short, must be between 3 and 20 letters"
        # error_list[4] = ""
        # user_name='None'
        form_error=True

    if len(user_name)>20:
        error_list[0] = "Username too long, must be between 3 and 20 letters"
        # error_list[4] = ""
        # user_name='None'
        form_error=True
    ##-----------------

    ##password validation
    if not pass_word:
        error_list[1] = "Please enter a valid password"
        form_error=True

    if " " in pass_word:
        error_list[1] = "Password must not contain spaces"
        form_error=True

    if len(pass_word)<3 and len(pass_word)>=1:
        error_list[1] = "Password too short, must be between 3 and 20 letters"
        form_error=True

    if len(pass_word)>20:
        error_list[1] = "Password too long, must be between 3 and 20 letters"
        form_error=True

    if not vpass_word or pass_word != vpass_word:
    	error_list[2] = "Passwords don't match"
    	form_error=True
    ##-------------

    ##email validation
    if e_mail:
        atcount=e_mail.count('@')
        pcount=e_mail.count('.')
        scount=e_mail.count(' ')
        elength=len(e_mail)
        if (atcount != 1) or (pcount !=1) or (scount != 0) or (elength<3) or (elength>20):
            error_list[3] = "Invalid email address"
            e_mail='None'
            form_error=True
    ##-------------



    #Page render or redirect
    if form_error ==True:	
    	return redirect("/?user_name_error={}&pass_word_error={}&vpass_word_error={}&e_mail_error={}&form_name={}&form_email={}".format(*error_list))
    else:
        return render_template('welcome.html', success='Welcome',username=user_name)
app.run()