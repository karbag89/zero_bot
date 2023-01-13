from flask import json


class Error:
    def errorMessage(error_code, error_message) -> json:
        '''Creating error log message in JSON body.'''
        data = {"code": error_code,
                "message": error_message}
        return data
