from rest_framework.exceptions import APIException
from rest_framework import status

'''
    Custom Exceptions for better error handling
'''

class MissingFieldsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Some required fields are missing."
    default_code = "missing_fields"

class OrganizationNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Organization not found."
    default_code = "organization_not_found"

class UserNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User not found."
    default_code = "user_not_found"

class InvalidCredentialsError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid credentials."
    default_code = "invalid_credentials"
