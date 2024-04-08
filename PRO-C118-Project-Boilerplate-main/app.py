from flask import Flask, render_template, request, jsonify
import prediction

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# API listening to POST requests and predicting sentiments
@app.route('/predict', methods=['POST'])
def predict():
    response = {}
    review = request.json.get('customer_review')
    if not review:
        response = {'status': 'error',
                    'message': 'Empty Review'}
    else:
        # calling the predict method from prediction.py module
        sentiment, path = prediction.predict(review)
        response = {'status': 'success',
                    'message': 'Got it',
                    'sentiment': sentiment,
                    'path': path}
    return jsonify(response)

# Creating an API to save the review, user clicks on the Save button
@app.route('/save', methods=['POST'])  # Corrected route and added methods
def save():
    # extracting date, product name, review, sentiment associated from the JSON data
    date = request.json.get('date')  # Replace with the correct key for date
    product = request.json.get('product')  # Replace with the correct key for product
    review = request.json.get('review')  # Replace with the correct key for review
    sentiment = request.json.get('sentiment')  # Replace with the correct key for sentiment

    # creating a final variable separated by commas
    data_entry = f"{date},{product},{review},{sentiment}\n"  # Compose the data entry as a string

    # open the file in the 'append' mode
    with open('reviews.log', 'a') as file:
        # Log the data in the file
        file.write(data_entry)

    # return a success message
    return jsonify({'status': 'success',
                    'message': 'Data Logged'})

if __name__ == "__main__":
    app.run(debug=True)
