from flask import Flask, render_template, request
import pandas as pd
from fuzzywuzzy import process

app = Flask(__name__)

# Load the data
df = pd.read_csv('merged_allergies_symptoms.csv')
#df=df.drop_duplicates()

# Home page with the form
@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        input_value = request.form['input_value']
        search_type = request.form['search_type']
        results = search_allergy_symptom(input_value, search_type)
        #print(results)  # Add this line to print the results
    return render_template('index.html', results=results)


def search_allergy_symptom(input_value, search_type):
    if search_type == 'allergy':
        # Get the best matches for the input value
        best_matches = process.extractBests(input_value, df['DESCRIPTION'], limit=10, score_cutoff=70)
        # Get the indices of the best matches
        match_indices = [df[df['DESCRIPTION'] == match[0]].index[0] for match in best_matches]
        # Filter the DataFrame based on the indices of the best matches
        results = df.iloc[match_indices].drop_duplicates(subset=['DESCRIPTION', 'Symptom 1', 'Symptom 2', 'Symptom 3', 'Symptom 4', 'Symptom 5'])
    elif search_type == 'symptom':
        symptoms = [symptom.strip() for symptom in input_value.split(',')]
        columns = ['Symptom 1', 'Symptom 2', 'Symptom 3', 'Symptom 4', 'Symptom 5']
        results = df[df[columns].apply(lambda row: all(row.str.contains(symptom, case=False).any() for symptom in symptoms), axis=1)].drop_duplicates(subset=['DESCRIPTION', 'Symptom 1', 'Symptom 2', 'Symptom 3', 'Symptom 4', 'Symptom 5'])
    return results

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
