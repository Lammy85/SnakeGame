from flask import Flask, render_template, request, jsonify
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

    #gets the data for the highscore table           
        
    daten = Highscore.query.order_by(Highscore.totalScore.desc()).all()

    #Top ten -> we only want the first 10 entries

    top_daten = daten[:10]
    return render_template('index.html', daten=top_daten)

#endpoint for score saving
    
@app.route('/saveScore', methods=['POST'])

def save_score():

    #receives the data sent with sendData()
    
    data = request.get_json()
    
    playername = data.get('playername')
    total_score = data.get('totalScore')

    #generating a new Highscore objekt with the data
        
    new_highscore = Highscore(playername=playername, totalScore=total_score)

    #saving the objekt in the database
    
    db.session.add(new_highscore)
    db.session.commit()

    #return as json important!

    return jsonify({"message": "Data successfully saved"})

    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
