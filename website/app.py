from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

def pred(lst):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['POST', 'GET'])
def index():
    prediction = 0

    if request.method == 'POST':
        yom = request.form['yom']
        engine = request.form['engine']
        mileage = request.form['mileage']
        brand = request.form['brand']
        fuel = request.form['fuel']
        gear = request.form['gear']
        leasing = request.form['leasing']
        condition = request.form['condition']
        ac = request.form['ac']
        ps = request.form['ps']
        pm = request.form['pm']
        pw = request.form['pw']

        feature_list = []
        feature_list.append(int(yom))
        feature_list.append(float(engine))
        feature_list.append(float(mileage))

        brand_list = ['others', 'honda', 'hyundai', 'kia', 'mazda', 'mercedes-benz', 
                       'micro', 'mitsubishi', 'nissan', 'perodua', 'suzuki', 'tata',
                       'toyota']
        lease_list = ['ls-ongoing', 'ls-no-ongoing']
        conditions_list = ['new', 'used']
        ac_type = ['ac-available', 'ac-not-available']
        ps_type = ['ps-available', 'ps-not-available']
        pm_type = ['pm-available', 'pm-not-available']
        pw_type = ['pw-available', 'pw-not-available']
        gear_type = ['Automatic', 'Manual']
        fuel_type = ['Petrol', 'Diesel', 'Hybrid', 'Electric']

        def traverse(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)

        traverse(brand_list, brand)
        traverse(lease_list, leasing)
        traverse(conditions_list, condition)
        traverse(ac_type, ac)
        traverse(ps_type, ps)
        traverse(pm_type, pm)
        traverse(pw_type, pw)
        traverse(gear_type, gear)
        traverse(fuel_type, fuel)

        prediction = pred(feature_list)
        prediction = np.round(prediction[0], 2)

    return render_template("index.html", prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)