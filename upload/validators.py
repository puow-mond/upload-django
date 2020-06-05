from django.core.exceptions import ValidationError

MAXIMUM_FILE_SIZE = 104857600


def validate_file_size(value):
    filesize = value.size
    if filesize > MAXIMUM_FILE_SIZE:
        raise ValidationError(
            "The maximum file size that can be uploaded is 100MB")
    else:
        return value
