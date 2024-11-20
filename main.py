from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class Highscore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playername = db.Column(db.String(200), nullable=False)
    totalScore = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def start_page():           
        
    daten = Highscore.query.order_by(Highscore.totalScore.desc()).all()
    return render_template('index.html', daten=daten)
    
@app.route('/saveScore', methods=['POST'])

def save_score():
    
    data = request.get_json()
    
    playername = data.get('playername')
    total_score = data.get('totalScore')
        
    new_highscore = Highscore(playername=playername, totalScore=total_score)
    
    db.session.add(new_highscore)
    db.session.commit()
    return jsonify({"message": "Daten erfolgreich gespeichert"})
    
if __name__ == "__main__":
    app.run(debug=True)
