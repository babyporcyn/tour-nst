# นำเข้าโมดูล 
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#กำหนดที่อยู่ DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nst.db_owner:2S3yVUCJgFMT@ep-royal-cake-a5mvmads.us-east-2.aws.neon.tech/nst.db?sslmode=require'
db = SQLAlchemy(app)

#สร้าง class ตาราง
class Tournst(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    opening_hours = db.Column(db.String(100))
    image_url = db.Column(db.String(200))

#การอ่านข้อมูลทั้งหมด
@app.route('/tournst', methods=['GET'])
def get_all_tournst():
    tournsts = Tournst.query.all()
    result = [
        {
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'opening_hours': t.opening_hours,
            'image_url': t.image_url
        } for t in tournsts
    ]
    return jsonify(result)

#การอ่านข้อมูลตามID
@app.route('/tournst/<int:id>', methods=['GET'])
def get_tournst(id):
    tournst = Tournst.query.get_or_404(id)
    return jsonify({
        'id': tournst.id,
        'name': tournst.name,
        'description': tournst.description,
        'opening_hours': tournst.opening_hours,
        'image_url': tournst.image_url
    })

#การเพิ่มข้อมูล
@app.route('/tournst', methods=['POST'])
def add_tournst():
    data = request.json
    new_tournst = Tournst(
        name=data['name'],
        description=data['description'],
        opening_hours=data['opening_hours'],
        image_url=data['image_url']
    )
    db.session.add(new_tournst)
    db.session.commit()
    return jsonify({'message': 'Tournst added successfully', 'id': new_tournst.id}), 201

#การอัพเดทข้อมูล
@app.route('/tournst/<int:id>', methods=['PUT'])
def update_tournst(id):
    tournst = Tournst.query.get_or_404(id)
    data = request.json
    tournst.name = data['name']
    tournst.description = data['description']
    tournst.opening_hours = data['opening_hours']
    tournst.image_url = data['image_url']
    db.session.commit()
    return jsonify({'message': 'Tournst updated successfully'})

#การลบข้อมูล
@app.route('/tournst/<int:id>', methods=['DELETE'])
def delete_tournst(id):
    tournst = Tournst.query.get_or_404(id)
    db.session.delete(tournst)
    db.session.commit()
    return jsonify({'message': 'Tournst deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
