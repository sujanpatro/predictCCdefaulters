import os
from flask import Flask, request, render_template, Response
from flask_cors import CORS, cross_origin
from predictFromModel import prediction
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation

os.putenv('LANG', 'en_us.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:
        if request.json['filepath'] is not None:
            path = request.json['filepath']
            train_valObj = train_validation(path)
            train_valObj.train_validation()

            trainModelObj = trainModel()
            trainModelObj.trainingModel()

    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)

    return Response("Training successful!!")


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        # print(request.form)
        # if request.get_json() is not None:
        #     print(str(1), "here")
        #     print(request.get_json())
        #     path = request.get_json()['filepath']
        #     pred_val = pred_validation(path)
        #     pred_val.prediction_validation()
        #     pred = prediction(path)
        #     path = pred.predictionFromModel()
        #     return Response("Prediction File created at %s" % path)

        if request.form is not None:
            # print(request.form['filepath'])
            path = request.form['filepath']
            # print(1)
            pred_val = pred_validation(path)
            # print(3)
            pred_val.prediction_validation()
            # print(2)
            pred = prediction(path)
            # print(1)
            path = pred.predictionFromModel()
            # print(2)
            return Response("Prediction File created at %s" % path)

    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


port = int(os.getenv("PORT", 5001))
if __name__ == '__main__':
    app.run(port=port, debug=True)
