import uuid

from flask_injector import inject

from services.dbinterfacer import DBInterfacer
from validators.fitbit_validator import FitbitValidator

from contracts.output import make_success_object, make_error_object

class FitbitValidation(object):
    @staticmethod
    def post(DBInterfacer: DBInterfacer, data: dict):
        """
        This function will validate the fitbit data and send it to
        the DB Interfacer to store it on the database.

        For now, it will do all the validation and then send the OK
        signal to the sender. In the future, it will kick off a thread
        and run the validation on the background and send the OK right
        away (an asynchronous model).
        """
        # Validate data
        validator = FitbitValidator(data)
        validated_data = validator.validate()

        # Check if hard failure
        if validated_data == None:
            return make_error_object(100, "An error occurred.")

        # Send validated data to DB Interfacer
        DBInterfacer.send(validated_data)

        return make_success_object()

class_instance = FitbitValidation()
