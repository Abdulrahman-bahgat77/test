from flask import Flask, request, jsonify
import pandas as pd

# Initialize Flask app
app = Flask(__name__)


data = pd.read_excel("/Users/Abdo/Desktop/task/model2/egypt_landmarks.xlsx")


# Define the function to get tourist spots
def get_tourist_spots_with_details(province_name):
    filtered_data = data[data['addressObj/city'].str.contains(province_name, case=False, na=False)]

    if filtered_data.empty:
        return f"There are no tourist places in the governorate '{province_name}'."

    spots = filtered_data[['addressObj/city', 'name', 'address', 'image']].to_dict('records')
    return spots


# Define the API route
@app.route('/')
def home():
    return  "tourist_Spots"

@app.route('/tourist_spots', methods=['POST'])
def tourist_spots():
    # Get the governorate name from the request body
    request_data = request.get_json()  # Parse JSON body
    province_name = request_data.get('governorate')  # Extract governorate name

    if not province_name:
        return jsonify({"error": "Please provide a governorate name in the request body."}), 400

    # Get tourist spots
    places = get_tourist_spots_with_details(province_name)

    if isinstance(places, str):
        return jsonify({"message": places}), 404
    else:
        return jsonify({"governorate": province_name, "tourist_spots": places}), 200



if __name__ == '__main__':
    app.run(debug=True)
