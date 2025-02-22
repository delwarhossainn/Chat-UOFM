from flask import Flask, request, jsonify
from transformers import pipeline
import sqlite3

app = Flask(__name__)

# Load the fine-tuned model
model = pipeline("text-generation", model="fine_tuned_model_1")

def get_student_details(name):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
    student = cursor.fetchone()
    conn.close()
    if student:
        return f"ID: {student[0]}, Name: {student[1]}, Major: {student[2]}, GPA: {student[3]:.2f}"
    else:
        return "Student not found."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("question", "")

    # Check if input contains a name
    if "my name is" in user_input.lower():
        words = user_input.lower().split("my name is")[-1].strip().split()
        name = " ".join(words[:2]).title()  # Take only the first two words
        print(name)

        response = get_student_details(name)
        
    else:
        response = model(user_input, max_length=100)[0]["generated_text"]

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)
