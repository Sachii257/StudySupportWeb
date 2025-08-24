from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
import os

app = Flask(__name__)

# A secret key is required for showing messages (like on the feedback form)
app.secret_key = 'your_very_secret_key_change_this'

# Configure the main folder where your files are stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# FINAL DATA STRUCTURE
# The keys ("computer_science_engineering", "aiml", "cn", etc.) exactly match your folder names.
# The "qps" key has been completely removed from every subject.
departments_data = {
    "computer_science_engineering": {
        "display_name": "Computer Science Engineering",
        "subjects": {
            "set": {
                "display_name": "Software Engineering and Testing",
                "notes": ["se(se and testing).pdf.pdf",
                          "st(se and testing).pdf"] # Add your filenames here, e.g., "SET_Notes.pdf"
            },
            "cn": {
                "display_name": "Computer Network",
                "notes": ["cn1.pdf",
                          "cn2.pdf"
                          ]
            },
            
            "aiml": {
                "display_name": "Artificial Intelligence and Machine Learning",
                "notes": ["ai and ml1.pdf",
                          "ai and ml2.pdf"
                          ]
            },
            
            "diot": {
                "display_name": "Design of IoT System",
                "notes": ["design of iot1.pdf",
                          "iot2.pdf"]
            },
            "rmipr": {
                "display_name": "Research Methodology and PIR",
                "notes": ["rm and ipr1.pdf",
                          "rm and ipr2.pdf"]
            },
            "es": {
                "display_name": "Environment Studies",
                "notes": ["ens1.pdf",
                          "ens2,pdf"]
            }
        }
    }
}


# --- Page Routes ---

@app.route('/')
def home():
    """Renders the homepage."""
    return render_template('index.html')

@app.route('/departments')
def show_departments():
    """Renders the page that lists all departments."""
    return render_template('departments.html', departments=departments_data)

@app.route('/department/<department_name>')
def show_subjects(department_name):
    """Renders the page that lists all subjects for a chosen department."""
    department = departments_data.get(department_name)
    if not department:
        return "Department not found", 404
    return render_template('subjects.html', department_name=department_name, department=department)

@app.route('/department/<department_name>/<subject_name>/<file_type>')
def show_files(department_name, subject_name, file_type):
    """Renders the page that lists the downloadable notes for a subject."""
    # Note: file_type will always be 'notes' based on our simplified templates.
    files_list = departments_data.get(department_name, {}).get("subjects", {}).get(subject_name, {}).get(file_type, [])
    department_display_name = departments_data.get(department_name, {}).get("display_name")
    subject_display_name = departments_data.get(department_name, {}).get("subjects", {}).get(subject_name, {}).get("display_name")
    title = "Notes"  # The title is now always "Notes"

    return render_template(
        'files.html',
        department_name=department_name,
        subject_name=subject_name,
        files=files_list,
        file_type=file_type,
        title=title,
        department_display_name=department_display_name,
        subject_display_name=subject_display_name
    )

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Handles the feedback page and form submission."""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # For this project, we just print the feedback to the terminal.
        print(f"--- Feedback Received ---\nName: {name}\nEmail: {email}\nMessage: {message}\n-------------------------")

        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('feedback'))

    return render_template('feedback.html')


# --- File Download Route ---

@app.route('/download/<department_name>/<subject_name>/<file_type>/<filename>')
def download_file(department_name, subject_name, file_type, filename):
    """
    Constructs the correct file path and serves the file for download.
    This function dynamically uses the folder names from the URL.
    """
    directory_path = os.path.join(app.config['UPLOAD_FOLDER'], department_name, subject_name, file_type)
    return send_from_directory(directory_path, filename, as_attachment=True)


# --- Main execution point to run the application ---

if __name__ == "__main__":
    app.run(debug=True)