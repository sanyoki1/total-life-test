from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import relationship
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
CORS(app)

# db tables
class Clinician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    npi_number = db.Column(db.String(10), unique=True, nullable=False)
    patients = relationship('Patient', backref='clinician', lazy=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    clinician_id = db.Column(db.Integer, db.ForeignKey('clinician.id'), nullable=False)
    appointments = relationship('Appointment', backref='patient', lazy=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

# validating npi
def validate_npi(npi_number, first_name, last_name, state):
    url = f'https://npiregistry.cms.hhs.gov/api/?number={npi_number}&version=2.1'
    response = requests.get(url)
    # check npi exists
    # then check if it matches first name, last name, and state
    if response.status_code == 200:
        data = response.json()
        results = data.get('results')
        if results:
            provider = results[0]
            if (provider['basic']['first_name'].lower() == first_name.lower() and
                    provider['basic']['last_name'].lower() == last_name.lower() and
                    provider['addresses'][0]['state'].lower() == state.lower()):
                return True
    return False

# handle clinician CRUD operations
@app.route('/clinicians', methods=['GET', 'POST', 'DELETE'])
def handle_clinicians():
    # get clinicians
    if request.method == 'GET':
        clinicians = Clinician.query.all()
        clinicians_data = []
        for c in clinicians:
            clinicians_data.append({
                'id': c.id,
                'first_name': c.first_name,
                'last_name': c.last_name,
                'state': c.state,
                'npi_number': c.npi_number
            })
        return jsonify(clinicians_data), 200
    
    # add clinician
    elif request.method == 'POST':
        data = request.json
        # validate npi details
        if not validate_npi(data['npi_number'], data['first_name'], data['last_name'], data['state']):
            return jsonify({'error': 'Invalid NPI details'}), 400
        clinician = Clinician(
            first_name=data['first_name'].upper(),
            last_name=data['last_name'].upper(),
            state=data['state'],
            npi_number=data['npi_number']
        )
        db.session.add(clinician)
        db.session.commit()
        return jsonify({'message': 'Clinician created successfully'}), 201
    
    # delete clinician
    elif request.method == 'DELETE':
        data = request.json
        # check clinician exists
        clinician = Clinician.query.get(data['clinician_id'])
        if not clinician:
            return jsonify({'error': 'Clinician not found'}), 404
        db.session.delete(clinician)
        db.session.commit()
        return jsonify({'message': 'Clinician deleted successfully'}), 200

# handle patients crud operations
@app.route('/patients', methods=['GET', 'POST', 'DELETE'])
def handle_patients():
    # get patients
    if request.method == 'GET':
        patients = Patient.query.all()
        patients_data = []
        for p in patients:
            patients_data.append({
                'id': p.id,
                'first_name': p.first_name,
                'last_name': p.last_name,
                'clinician_id': p.clinician_id
            })
        return jsonify(patients_data), 200

    # add patient
    elif request.method == 'POST':
        data = request.json
        # check clinician exists
        clinician = Clinician.query.get(data['clinician_id'])
        if not clinician:
            return jsonify({'error': 'Clinician not found'}), 404
        patient = Patient(
            first_name = data['first_name'].upper(),
            last_name = data['last_name'].upper(),
            clinician_id = data['clinician_id']
        )
        db.session.add(patient)
        db.session.commit()
        return jsonify({'message': 'Patient created successfully'}), 201

    # delete patient
    elif request.method == 'DELETE':
        data = request.json
        # check patient exists
        patient = Patient.query.get(data['patient_id'])
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        db.session.delete(patient)
        db.session.commit()
        return jsonify({'message': 'Patient deleted successfully'}), 201

# handle appointments crud operations
@app.route('/appointments', methods=['GET', 'POST', 'DELETE'])
def handle_appointments():
    
    # get appointments
    if request.method == 'GET':
        appointments = Appointment.query.all()
        appointments_data = []
        for a in appointments:
            appointments_data.append({
            'id': a.id,
            'date': a.date,
            'time': a.time,
            'patient_id': a.patient_id
        })
        return jsonify(appointments_data), 200

    # add appointment
    elif request.method == 'POST':
        data = request.json
        # check patient exists
        patient = Patient.query.get(data['patient_id'])
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        appointment = Appointment(
            date = data['date'],
            time = data['time'],
            patient_id = data['patient_id']
        )
        db.session.add(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment created successfully'}), 201

    # delete appointment
    elif request.method == 'DELETE':
        data = request.json
        # check appointment exists
        appointment = Appointment.query.get(data['appointment_id'])
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment deleted successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)