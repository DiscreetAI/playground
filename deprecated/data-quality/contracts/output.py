def make_success_object():
    return {"Success": True}, 200

def make_error_object(error_code, error_message):
    error_object = {
        "Success": False,
        "Error": {
            "Code": error_code,
            "Message": error_message
        }
    }
    return error_object, 400
