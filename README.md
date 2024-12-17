# Total Life Test Submission
My submission for the total life take home test.

## Prerequisites

1. **Python 3**
2. **Flask** + (flask-sqlalchemy flask-restful flask-cors)
3. **React**
4. **Node.js**
5. **axios**

## Installation

**Clone the repository**:
   ```bash
   git clone https://github.com/sanyoki1/total-life-test.git
   cd total-life-test
   ```

**Install dependencies and prerequisites**:
   ```bash
   pip install Flask
   pip install Flask-SQLAlchemy
   pip install flask-restful
   pip install flask-cors
   pip install requests
   npm install (should also install axios)
   ```

**Create the database and run the backend API**:
   ```bash
    cd backend
    py create_db.py
    py api.py
   ```
Make sure it is running (should be on http://localhost:5000/)

**Start the development server (/total-life-test/)**:
   ```bash
   cd ..
   npm run start
   ```
Should run on http://localhost:3000/ and will fetch and displays a list of appointments from the API (database.db already comes with a few clinicians with valid NPIs from the NPI registry, patients, and appointments as an example)