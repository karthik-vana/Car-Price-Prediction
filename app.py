from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('car_price_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Age = 2024 - int(request.form['Year'])
        Fuel_Type = request.form['Fuel_Type']
        Seller_Type = request.form['Seller_Type']
        Transmission = request.form['Transmission']

        # Manual Logic for One-Hot Encoding
        Fuel_Type_Diesel = 1 if Fuel_Type == 'Diesel' else 0
        Fuel_Type_Petrol = 1 if Fuel_Type == 'Petrol' else 0
        Seller_Type_Individual = 1 if Seller_Type == 'Individual' else 0
        Transmission_Manual = 1 if Transmission == 'Manual' else 0

        prediction = model.predict([[Present_Price, Kms_Driven, Owner, Age, 
                                     Fuel_Type_Diesel, Fuel_Type_Petrol, 
                                     Seller_Type_Individual, Transmission_Manual]])

        output = round(prediction[0], 2)
        return render_template('index.html', prediction_text=f"Estimated Selling Price: ₹{output} Lakhs")

if __name__ == "__main__":
    app.run(debug=True)