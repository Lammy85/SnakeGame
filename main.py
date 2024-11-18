from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Highscore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playername = db.Column(db.String(200), nullable=True)
    totalScore = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now)

    @app.route('/', methods=['GET', 'POST'])
    def start_page():

        if request.method == 'POST':

            new_highscore = Highscore(
                playername = request.form['playername'],
                totalScore = request.form['totalScore']            
            )
            db.session.add(new_highscore)
            db.session.commit()

            return redirect('/')
        
        daten = Highscore.query.all()
        return render_template('index.html', daten=daten)
    
if __name__ == "__main__":
    app.run()
