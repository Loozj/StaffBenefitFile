from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Load CSV data into memory
data = pd.read_csv('benefit.csv')

# Ensure the EmpNo column is treated as strings
data['EmpNo'] = data['EmpNo'].astype(str).str.strip()

@app.route('/')
def home():
    # Render the HTML template
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_employee():
    try:
        # Get employee number from query parameters
        employee_number = request.args.get('employeeNumber', '').strip()
        print(f"Received request for employee number: {employee_number}")

        # Search for the employee in the dataset
        result = data[data['EmpNo'] == employee_number]

        if result.empty:
            print(f"Employee number {employee_number} not found.")
            return render_template('index.html', error='Employee not found')
        else:
            # Fetch the matching row
            row = result.iloc[0]
            print(f"Found employee: {row['Name']}, Benefit: {row['BENEFIT']}")
            return render_template(
                'index.html',
                result={'name': row['Name'], 'benefit': row['BENEFIT']}
            )
    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template('index.html', error='Internal server error')

if __name__ == '__main__':
    app.run(debug=True)
