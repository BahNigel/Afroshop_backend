from storages.backends.s3boto3 import S3StaticStorage, S3Boto3Storage

class StaticStorage(S3StaticStorage):
    location = 'static'
    file_overwrite = False

class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
