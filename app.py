from flask import Flask, render_template, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
import os
import io

app = Flask(__name__)

# Ensure image directory exists
IMAGE_DIR = 'static/images'
os.makedirs(IMAGE_DIR, exist_ok=True)

# Load datasets
members_data = pd.read_csv('gym_members_exercise_tracking.csv')
exercise_data = pd.read_csv('megaGymDataset (3).csv')

@app.route('/', methods=['GET', 'POST'])
def analyze_data():
    average_calories = None
    total_sessions = None
    filtered_data = members_data

    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        workout_type = request.form.get('workout_type')

        if age:
            filtered_data = filtered_data[filtered_data['Age'] == int(age)]
        if gender:
            filtered_data = filtered_data[filtered_data['Gender'] == gender]
        if workout_type:
            filtered_data = filtered_data[filtered_data['Workout_Type'] == workout_type]

        average_calories = filtered_data['Calories_Burned'].mean()
        total_sessions = filtered_data.shape[0]

    return render_template('analysis.html', average_calories=average_calories, total_sessions=total_sessions)

# Visualization endpoints with filtering and saving images
@app.route('/heart_rate_analysis', methods=['GET', 'POST'])
def heart_rate_analysis():
    filtered_data = apply_filters(request.form)
    plt.figure(figsize=(12, 6))
    plt.plot(filtered_data['Session_Duration'], filtered_data['Avg_BPM'], label='Avg BPM', color='royalblue')
    plt.xlabel('Session Duration')
    plt.ylabel('Average BPM')
    plt.title('Average BPM Trend Over Sessions')
    plt.legend()
    plt.grid(True)

    img_path = os.path.join(IMAGE_DIR, 'heart_rate_analysis.png')
    plt.savefig(img_path)
    plt.close()
    return send_file(img_path, mimetype='image/png')

@app.route('/calories_by_workout', methods=['GET', 'POST'])
def calories_by_workout():
    filtered_data = apply_filters(request.form)
    calories_by_workout = filtered_data.groupby('Workout_Type')['Calories_Burned'].mean().sort_values()
    plt.figure(figsize=(10, 6))
    calories_by_workout.plot(kind='bar', color='salmon')
    plt.xlabel('Workout Type')
    plt.ylabel('Average Calories Burned')
    plt.title('Average Calories Burned per Workout Type')
    plt.xticks(rotation=45)

    img_path = os.path.join(IMAGE_DIR, 'calories_by_workout.png')
    plt.savefig(img_path)
    plt.close()
    return send_file(img_path, mimetype='image/png')

@app.route('/workout_frequency_by_age', methods=['GET', 'POST'])
def workout_frequency_by_age():
    filtered_data = apply_filters(request.form)
    workout_freq = filtered_data.groupby('Age')['Workout_Frequency'].mean()
    plt.figure(figsize=(10, 6))
    workout_freq.plot(kind='bar', color='lightgreen')
    plt.xlabel('Age')
    plt.ylabel('Workout Frequency (Days/Week)')
    plt.title('Workout Frequency by Age Group')
    plt.xticks(rotation=45)

    img_path = os.path.join(IMAGE_DIR, 'workout_frequency_by_age.png')
    plt.savefig(img_path)
    plt.close()
    return send_file(img_path, mimetype='image/png')

@app.route('/bmi_distribution', methods=['GET', 'POST'])
def bmi_distribution():
    filtered_data = apply_filters(request.form)
    plt.figure(figsize=(10, 6))
    plt.hist(filtered_data['BMI'], bins=20, color='skyblue', edgecolor='black')
    plt.xlabel('BMI')
    plt.ylabel('Frequency')
    plt.title('BMI Distribution')

    img_path = os.path.join(IMAGE_DIR, 'bmi_distribution.png')
    plt.savefig(img_path)
    plt.close()
    return send_file(img_path, mimetype='image/png')

@app.route('/fat_vs_calories', methods=['GET', 'POST'])
def fat_vs_calories():
    filtered_data = apply_filters(request.form)
    plt.figure(figsize=(10, 6))
    plt.scatter(filtered_data['Fat_Percentage'], filtered_data['Calories_Burned'], color='purple', alpha=0.5)
    plt.xlabel('Fat Percentage')
    plt.ylabel('Calories Burned')
    plt.title('Fat Percentage vs. Calories Burned')

    img_path = os.path.join(IMAGE_DIR, 'fat_vs_calories.png')
    plt.savefig(img_path)
    plt.close()
    return send_file(img_path, mimetype='image/png')

@app.route('/workout_type_popularity', methods=['GET', 'POST'])
def workout_type_popularity():
    filtered_data = apply_filters(request.form)
    workout_counts = filtered_data['Workout_Type'].value_counts()
    plt.figure(figsize=(10, 6))
    workout_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    plt.title('Workout Type Popularity')
    plt.ylabel('')

    img_path = os.path.join(IMAGE_DIR, 'workout_type_popularity.png')
    plt.savefig(img_path)
    plt.close()
    return send_file(img_path, mimetype='image/png')

# Helper function to apply filters
def apply_filters(form):
    filtered_data = members_data
    age = form.get('age')
    gender = form.get('gender')
    workout_type = form.get('workout_type')

    if age:
        filtered_data = filtered_data[filtered_data['Age'] == int(age)]
    if gender:
        filtered_data = filtered_data[filtered_data['Gender'] == gender]
    if workout_type:
        filtered_data = filtered_data[filtered_data['Workout_Type'] == workout_type]

    return filtered_data

if __name__ == '__main__':
    app.run(debug=True)
