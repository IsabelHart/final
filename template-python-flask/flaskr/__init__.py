import os

from flask import Flask, session
from flask import Flask, render_template, request
from flask_session import Session


#######################################################################
#App configurations
#######################################################################
def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )
    Session(app)
    app.config['SESSION_TYPE'] = 'filesystem'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
#######################################################################
#App configurations ended
#######################################################################


#######################################################################
#Classic Mode
####################################################################
    #Home Page
    @app.route('/')
    def index():
        session['score'] = 0
        #First Question

        return render_template('index.html')

    #######################################################################
    #This function is the way you will change your score
    #The texts are going to be the text that will be shown in the next screen
    def button_clicking(intro_text, a_text,b_text,c_text, print_message_for_debug):
        print("##################################")
        if request.method == "POST":
            print("You sent a post request")
            if request.form.get("submit_a"):
                session['score'] = session['score']+1
                print('User should have selected a')

            elif request.form.get("submit_b"):
                session['score'] = session['score']+2
                print('User should have selected b')

            elif request.form.get("submit_c"):
                session['score'] = session['score']+3
                print('User should have selected c')

            else:
                print("MAJOR ISSUE!! User choice was neither a,b, or c")
                pass

            session['intro_text'] = intro_text
            session['choice_a_text'] = a_text
            session['choice_b_text'] = b_text
            session['choice_c_text'] = c_text
            print('message: ', print_message_for_debug)
            print('new score: ', session['score'])
            
        else:
            print("MAJOR ERROR IN BUTTON CLICK FUNCTION IF NOT GOING INTO THE FIRST ROUND")
            print("If you did get this message you sent a get request instead of a post request")
        print("##################################")


    #######################################################################
    #1st Question function
    @app.route("/classic_mode_q1",methods=['GET', 'POST'])
    def first_question():
        session['intro_text'] = "When do you brush your teeth in the morning?"
        session['choice_a_text'] = 'Right when I wake up'
        session['choice_b_text'] = 'After breakfast'
        session['choice_c_text'] = 'In the middle of breakfast'
        message = 'Classic Mode was selected'
        next_page = '/classic_mode_q2'

        button_clicking(session['intro_text'], session['choice_a_text'], session['choice_b_text'], session['choice_c_text'], message)
        
        return render_template('classic_mode.html', intro = session['intro_text'], a_text = session['choice_a_text'], b_text = session['choice_b_text'], c_text = session['choice_c_text'], pg_u_goto_after_clicked = next_page) 

    #######################################################################
    #2nd Question function
    @app.route("/classic_mode_q2", methods=['GET','POST'])    
    def second_question():

        new_intro_text =  "Where do you put your tongue when you drink from a cup?"
        new_a_text = "Inside the cup"
        new_b_text = 'Outside the cup'
        new_c_text = 'Behind my teeth'
        message = 'User just answered Q1'
        next_page = '/classic_mode_q3'

        button_clicking(new_intro_text, new_a_text, new_b_text, new_c_text, message)
        return render_template('classic_mode.html', intro = session['intro_text'], a_text = session['choice_a_text'], b_text = session['choice_b_text'], c_text = session['choice_c_text'], pg_u_goto_after_clicked = next_page ) 
      
    #######################################################################
    #3rd Question function
    @app.route("/classic_mode_q3", methods=['GET','POST'])
    def third_question():

        new_intro_text =  'How tall do you feel(regardless of actual height)?'
        new_a_text = "7ft"
        new_b_text = '6ft'
        new_c_text = '5ft'
        message = 'User just answered Q2'
        next_page = '/classic_mode_q4'

        
        button_clicking(new_intro_text, new_a_text, new_b_text, new_c_text, message)
        return render_template('classic_mode.html', intro = session['intro_text'], a_text = session['choice_a_text'], b_text = session['choice_b_text'], c_text = session['choice_c_text'], pg_u_goto_after_clicked = next_page) 

    #######################################################################
    #4th Question function
    @app.route("/classic_mode_q4", methods=['GET','POST'])
    def fourth_question():

        new_intro_text =  "What is your favorite meal?"
        new_a_text = 'Breakfast'
        new_b_text = 'Lunch'
        new_c_text = 'Dinner'
        message = 'User just answered Q3'
        next_page = '/classic_mode_q5'

        button_clicking(new_intro_text, new_a_text, new_b_text, new_c_text, message)
        
    
        return render_template('classic_mode.html', intro = session['intro_text'], a_text = session['choice_a_text'], b_text = session['choice_b_text'], c_text = session['choice_c_text'], pg_u_goto_after_clicked = next_page) 

    #######################################################################
    #5th Question function 
    @app.route("/classic_mode_q5", methods=['GET','POST'])
    def fifth_question():
        score = session['score']
        new_intro_text =  'Where do you look when you are at the dentist?'
        new_a_text = 'The Ceiling'
        new_b_text = "Into the Dentists Eyes"
        new_c_text = 'I Close my Eyes'
        message = 'User just answered Q4'
        next_page = '/end_screen/'
        
        button_clicking(new_intro_text, new_a_text, new_b_text, new_c_text, message)
        return render_template('classic_mode.html', intro = session['intro_text'], a_text = session['choice_a_text'], b_text = session['choice_b_text'], c_text = session['choice_c_text'], pg_u_goto_after_clicked = next_page)

    #######################################################################
    #Classic Mode End Screen
    @app.route("/end_screen/", methods=['POST'])
    def ending():
        button_clicking('', '', '', '', 'Answered Q5 and below will be the final score')  
        score = session['score']
        print('Final score: ', score)
        if score == 15 or score == 8:
            picture_url = 'https://raw.githubusercontent.com/IsabelHart/Isabel_Hart_HTML_Learning/main/download-5.jpg'
            last_scene = render_template('end_screen.html', ending_text = 'Your emoji is:')
        elif score == 6:
            picture_url = 'https://raw.githubusercontent.com/IsabelHart/Isabel_Hart_HTML_Learning/main/download-4.jpg'
            last_scene = render_template('end_screen.html', ending_text = 'Your emoji is:')
        elif score == 12:
            picture_url = 'https://raw.githubusercontent.com/IsabelHart/Isabel_Hart_HTML_Learning/main/download.jpg'
            last_scene = render_template('end_screen.html', ending_text = 'Your emoji is:')
        elif score == 10:
            picture_url = 'https://raw.githubusercontent.com/IsabelHart/Isabel_Hart_HTML_Learning/main/download-1.jpg'
            last_scene = render_template('end_screen.html', ending_text = 'Your emoji is:')
        elif score == 5:
            picture_url = 'https://raw.githubusercontent.com/IsabelHart/Isabel_Hart_HTML_Learning/main/download-3.jpg'
            last_scene = render_template('end_screen.html', ending_text = 'Your emoji is:')
        elif score == 7 or score == 9:
            picture_url = 'https://raw.githubusercontent.com/IsabelHart/Isabel_Hart_HTML_Learning/main/download-2.jpg'
            last_scene = render_template('end_screen.html', ending_text = 'Your emoji is:')
        else:
            picture_url = 'https://raw.githubusercontent.com/IsabelHart/Isabel_Hart_HTML_Learning/main/download-6.jpg'
            last_scene = render_template('end_screen.html', ending_text = "Your emoji is:")

        print("##################################")
        return render_template('end_screen.html',ending_text = 'RESULTS', picture = picture_url)
    
#######################################################################
#Classic mode ended
#######################################################################
    #Help
    @app.route("/help_page", methods=['GET','POST'])
    def help():
        score = session['score']
        new_intro_text =  ''
        next_page = '/'
        
        return render_template('help.html', intro = session['intro_text'], a_text = session['choice_a_text'], b_text = session['choice_b_text'], c_text = session['choice_c_text'], pg_u_goto_after_clicked = next_page,)


#######################################################################
#Create session & run the application
    sess = Session()
    sess.init_app(app)

    return app








#helpful websites
#https://stackoverflow.com/questions/15557392/how-do-i-display-images-from-google-drive-on-a-website
#https://unsplash.com/images/stock/blogging
#https://getbootstrap.com/docs/3.3/components/#btn-groups
#https://www.w3schools.com/bootstrap/bootstrap_theme_me.asp
#https://stackoverflow.com/questions/42601478/flask-calling-python-function-on-button-onclick-event