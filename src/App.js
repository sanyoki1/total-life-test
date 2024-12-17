import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const [appointments, set_appointments] = useState([]);
  const [filtered_appointments, set_filtered_appointments] = useState([]);
  const [patients, set_patients] = useState([]);
  const [start_date_time, set_start_date_time] = useState('');
  const [end_date_time, set_end_date_time] = useState('');

  // fetch appointments and patients from the backend
  useEffect(() => {
    const fetch_appointments_and_patients = async () => {
      try {
        const [appointments_response, patients_response] = await Promise.all([
          axios.get('http://localhost:5000/appointments'),
          axios.get('http://localhost:5000/patients'),
        ]);
        set_appointments(appointments_response.data);
        set_patients(patients_response.data);
        set_filtered_appointments(appointments_response.data);
      } catch (error) {
        console.error('Error', error);
      }
    };
    fetch_appointments_and_patients();
  }, []);

  // get patient's full name based on patient_id
  const get_patient_name = (patientId) => {
    const patient = patients.find((p) => p.id === patientId);
    if (patient) {
      return `${patient.first_name} ${patient.last_name}`;
    }
  };
  
  // convert 24 hour time to 12 hour time
  const get_twelve_hour_time = (date, time) => {
    return new Date(date + 'T' + time + ':00Z').toLocaleString('en-US',
      {timeZone:'GMT',hour12:true,hour:'numeric',minute:'numeric'}
    );
  }

  // filter appointments based on date/time range
  const handle_filter = () => {
    // check both fields are filled in before updating
    if (!start_date_time || !end_date_time) {
      set_filtered_appointments(appointments);
      return;
    }
    const start = new Date(start_date_time);
    const end = new Date(end_date_time);

    const filtered = appointments.filter((appt) => {
      const appt_date_time = new Date(`${appt.date}T${appt.time}`);
      return appt_date_time >= start && appt_date_time <= end;
    });
    set_filtered_appointments(filtered);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="mb-2 p-2 rounded flex gap-4 bg-gray-200">
        <div>
          <label className="block mb-2 font-poppins">Start Date and Time</label>
          <input
            type="datetime-local"
            value={start_date_time}
            onChange={(e) => set_start_date_time(e.target.value)}
            className="p-1 rounded"
          />
        </div>
        <div>
          <label className="block mb-2 font-poppins">End Date and Time</label>
          <input
            type="datetime-local"
            value={end_date_time}
            onChange={(e) => set_end_date_time(e.target.value)}
            className="p-1 rounded"
          />
        </div>
        <button
          onClick={handle_filter}
          className="self-center bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-400 mt-8 font-poppins"
        > Filter
        </button>
      </div>
      <div className="bg-white rounded px-1 pb-1">
      <h1 className="pt-2 pl-4 rounded text-2xl font-poppins">Appointments</h1>
          {filtered_appointments.map((appt) => (
            <li
              key={appt.id}
              className="p-4 flex m-2 rounded w-1/3 bg-gray-200 hover:bg-gray-100"
            >
              <div>
                <p className="text-lg font-poppins capitalize">
                  {get_patient_name(appt.patient_id).toLowerCase()}
                </p>
                <div className="flex gap-4">
                  <p className="text-sm font-thin text-gray-600">
                    {appt.date}
                  </p>
                  <p className="text-sm font-thin text-gray-600">
                    {get_twelve_hour_time(appt.date, appt.time)}
                  </p>
                </div>
              </div>
            </li>
          ))}
      </div>
    </div>
  );
};

export default App;
