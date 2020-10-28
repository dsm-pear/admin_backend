from rest_framework.exceptions import APIException


class InvalidSort(APIException):
    status_code = 404
    default_detail = "Please enter sort again."
