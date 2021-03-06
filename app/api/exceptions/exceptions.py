class ApiException(Exception):
    # API status code
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """
        Parse object to json response.
        """
        rv = dict(self.payload or ())
        rv['status'] = self.status_code
        rv['message'] = self.message
        return rv


class EnoughFunds(ApiException):
    status_code = 421
    pass


class InvalidUnspent(ApiException):
    status_code = 422
    pass


class InvalidOutputs(ApiException):
    status_code = 423
    pass
