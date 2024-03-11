from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Establish a connection to the MySQL database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "2468",
    "database": "pycharm_projects"
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Material list to store passed materials
material_list = []

# Threshold values for materials
threshold_values = {
    'steel': {
        'tensile_strength': 500,
        'fracture_measurement': 50,
        'hardness': 200,
        'impact_strength': 40,
        'elastic_modulus': 200
    },
    'bronze': {
        'tensile_strength': 450,
        'fracture_measurement': 80,
        'hardness': 250,
        'impact_strength': 350,
        'elastic_modulus': 380
    },
    'iron': {
        'tensile_strength': 550,
        'fracture_measurement': 120,
        'hardness': 180,
        'impact_strength': 280,
        'elastic_modulus': 420
    },
    'aluminum': {
        'tensile_strength': 300,
        'fracture_measurement': 40,
        'hardness': 120,
        'impact_strength': 30,
        'elastic_modulus': 150
    },
    'copper': {
        'tensile_strength': 400,
        'fracture_measurement': 60,
        'hardness': 180,
        'impact_strength': 50,
        'elastic_modulus': 180
    },
    'gold': {
        'tensile_strength': 200,
        'fracture_measurement': 30,
        'hardness': 90,
        'impact_strength': 20,
        'elastic_modulus': 80
    },
    'silver': {
        'tensile_strength': 250,
        'fracture_measurement': 35,
        'hardness': 100,
        'impact_strength': 25,
        'elastic_modulus': 100
    },
    'nickel': {
        'tensile_strength': 350,
        'fracture_measurement': 55,
        'hardness': 150,
        'impact_strength': 35,
        'elastic_modulus': 170
    },
    'zinc': {
        'tensile_strength': 180,
        'fracture_measurement': 25,
        'hardness': 80,
        'impact_strength': 15,
        'elastic_modulus': 70
    },
    'platinum': {
        'tensile_strength': 600,
        'fracture_measurement': 70,
        'hardness': 250,
        'impact_strength': 60,
        'elastic_modulus': 250
    }
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    pass_fail_status = 'Pending'  # Default status

    if request.method == 'POST':
        # Get user input
        material = request.form['material']
        # Use the selected material to get its threshold values
        thresholds = threshold_values.get(material, {})
        # Other form fields processing...

        # Check if material passes the quality check
        passed = all(request.form[field] and float(request.form[field]) >= thresholds.get(field, 0.0) for field in thresholds)

        # Update pass/fail status
        pass_fail_status = 'Passed' if passed else 'Failed'

        # Add material to the list and the MySQL database
        material_list.append({
            'name': material,
            'tensile_strength': float(request.form['tensile_strength']),
            'fracture_measurement': float(request.form['fracture_measurement']),
            'hardness': float(request.form['hardness']),
            'impact_strength': float(request.form['impact_strength']),
            'elastic_modulus': float(request.form['elastic_modulus']),
            'pass_fail_status': pass_fail_status
        })

        # Insert the passed material into the MySQL database
        insert_query = "INSERT INTO blockchain1 (material, tensile_strength, fracture_measurement, hardness, impact_strength, elastic_modulus, pass_fail_status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (
            material,
            float(request.form['tensile_strength']),
            float(request.form['fracture_measurement']),
            float(request.form['hardness']),
            float(request.form['impact_strength']),
            float(request.form['elastic_modulus']),
            pass_fail_status
        )
        cursor.execute(insert_query, values)
        conn.commit()

    return render_template('add_material.html', pass_fail_status=pass_fail_status)

@app.route('/display_materials')
def display_materials():
    # Fetch materials from the MySQL database
    select_query = "SELECT * FROM blockchain1"
    cursor.execute(select_query)
    materials_from_db = cursor.fetchall()

    # Convert database results to a list of dictionaries
    material_list_db = [{'material': material[0], 'tensile_strength': material[1], 'fracture_measurement': material[2], 'hardness': material[3], 'impact_strength': material[4], 'elastic_modulus': material[5], 'pass_fail_status': material[6]} for material in materials_from_db]

    return render_template('display_all_materials.html', materials=material_list_db)

@app.route('/display_recent_materials')
def display_recent_materials():
    # Fetch recent materials from the in-memory list
    return render_template('display_materials.html', materials=material_list)

@app.route('/display_all_materials')
def display_all_materials():
    # Fetch all materials from the in-memory list
    return render_template('display_all_materials.html', materials=material_list)

if __name__ == '__main__':
    app.run(debug=True)
