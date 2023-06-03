from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from storages.utils import clean_name


class FixUlrStorage(S3Boto3Storage):
    def url(self, name, parameters=None, expire=None, http_method=None):
        # Preserve the trailing slash after normalizing the path
        name = self._normalize_name(clean_name(name))
        params = parameters.copy() if parameters else {}
        if expire is None:
            expire = self.querystring_expire

        params['Bucket'] = self.bucket.name
        params['Key'] = name
        url = self.bucket.meta.client.generate_presigned_url('get_object', Params=params,
                                                             ExpiresIn=expire, HttpMethod=http_method)

        url = str(url).replace(self.endpoint_url, settings.MINIO_EXT_ENDPOINT)

        if self.querystring_auth:
            return url
        return self._strip_signing_parameters(url)
