from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['WTF_CSRF_ENABLED'] = False

db = SQLAlchemy(app)

class Highscore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playername = db.Column(db.String(200), nullable=True)
    totalScore = db.Column(db.Integer, nullable=True)

@app.route('/', methods=['GET', 'POST'])
def start_page():           
        
    daten = Highscore.query.all()
    return render_template('index.html', daten=daten)
    
@app.route('/saveScore', methods=['GET', 'POST'])
def saveScore():
    if request.method == 'POST':
    
        data = request.get_json()
        wert = data.get('totalScore')

        new_highscore = Highscore(
            playername = request.form['playername'],
            totalScore = wert
        )
        db.session.add(new_highscore)
        db.session.commit()
        return redirect(url_for('index.html'))
        
    
if __name__ == "__main__":
    app.run(debug=True)
