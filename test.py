import os
from trainingModel import trainModel
from training_Validation_Insertion import train_validation

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

try:

    path = 'Training_Batch_Files'
    train_valObj = train_validation(path)

    train_valObj.train_validation()

    trainModelObj = trainModel()
    trainModelObj.trainingModel()


except ValueError:

    print("Error Occurred! %s" % ValueError)

except KeyError:

    print("Error Occurred! %s" % KeyError)

except Exception as e:

    print("Error Occurred! %s" % e)








