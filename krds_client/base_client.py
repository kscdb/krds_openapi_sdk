import hashlib
import hmac
import urllib

import datetime
import requests


class RequestComposer:
    def __init__(self, ak, sk, service, request_parameters, method, content_hash=False):
        self.ak = ak
        self.sk = sk
        self.service = service
        self.content_hash = content_hash
        self.header_name_authorization = 'Authorization'
        self.header_name_host = 'Host'
        self.header_name_content_sha256 = 'X-Amz-Content-Sha256'
        self.header_name_date = 'X-Amz-Date'
        self.hash_keyword = 'AWS4'
        self.hash_method = 'AWS4-HMAC-SHA256'
        self.request_parameters = request_parameters
        self.method = method

    @staticmethod
    def get_canonical_headers(headers):
        canonical = []

        for header in headers:
            c_name = header.lower().strip()
            raw_value = str(headers[header])
            if '"' in raw_value:
                c_value = raw_value.strip()
            else:
                c_value = ' '.join(raw_value.strip().split())
            canonical.append('%s:%s' % (c_name, c_value))
        return '\n'.join(sorted(canonical)) + '\n'

    @staticmethod
    def get_signed_headers(headers):
        lowercase_headers = ['%s' % n.lower().strip() for n in headers]
        lowercase_headers = sorted(lowercase_headers)
        return ';'.join(lowercase_headers)

    def get_headers(self, host, region, payload, additional_signing_headers=None):
        if additional_signing_headers is None:
            additional_signing_headers = {}
        if self.ak is None or self.sk is None:
            return None

        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope

        # ************* TASK 1: CREATE A CANONICAL REQUEST *************
        # http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

        # Step 1 is to define the verb (GET, POST, etc.)--already done.
        method = self.method

        # Step 2: Create canonical URI--the part of the URI from domain to query
        # string (use '/' if no path)
        canonical_uri = '/'

        # Step 3: Create the canonical query string. In this example, request
        # parameters are passed in the body of the request and the query string
        # is blank.
        canonical_querystring = self.request_parameters

        # Step 4: Create the canonical headers. Header names and values
        # must be trimmed and lowercase, and sorted in ASCII order.
        # Note that there is a trailing \n.
        headers_to_sign = {
            self.header_name_host: host,  # sign indispensable
            self.header_name_date: amz_date,  # sign indispensable
        }

        if self.content_hash:
            headers_to_sign[self.header_name_content_sha256] = hashlib.sha256(payload).hexdigest()
        # additional headers can be added to signing process
        for h in additional_signing_headers:
            if h not in headers_to_sign:
                headers_to_sign[h] = additional_signing_headers[h]

        canonical_headers = self.get_canonical_headers(headers_to_sign)

        # Step 5: Create the list of signed headers. This lists the headers
        # in the canonical_headers list, delimited with ";" and in alpha order.
        # Note: The request can include any headers; canonical_headers and
        # signed_headers include those that you want to be included in the
        # hash of the request. "Host" and "x-amz-date" are always required.
        # For DynamoDB, content-type and x-amz-target are also required.
        signed_headers = self.get_signed_headers(headers_to_sign)

        # Step 6: Create payload hash. In this example, the payload (body of
        # the request) contains the request parameters.
        payload_hash = hashlib.sha256(payload).hexdigest()

        # Step 7: Combine elements to create create canonical request
        canonical_request = method + '\n' + canonical_uri + '\n' + \
            canonical_querystring + '\n' + canonical_headers + '\n' + \
            signed_headers + '\n' + payload_hash

        # ************* TASK 2: CREATE THE STRING TO SIGN*************
        # Match the algorithm to the hashing algorithm you use, either SHA-1 or
        # SHA-256 (recommended)
        algorithm = self.hash_method
        credential_scope = date_stamp + '/' + region + '/' + self.service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' + amz_date + '\n' + credential_scope + '\n' + hashlib.sha256(
            canonical_request).hexdigest()

        # ************* TASK 3: CALCULATE THE SIGNATURE *************
        # Create the signing key using the function defined above.
        signing_key = self.get_signature_key(self.sk, date_stamp, region, self.service)

        # Sign the string_to_sign using the signing_key
        signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

        # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
        # Put the signature information in a header named Authorization.
        authorization_header = algorithm + ' ' + 'Credential=' + self.ak + '/' + credential_scope + ', ' \
            + 'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        # For DynamoDB, the request can include any headers, but MUST include "host", "x-amz-date",
        # "x-amz-target", "content-type", and "Authorization". Except for the authorization
        # header, the headers must be included in the canonical_headers and signed_headers values, as
        # noted earlier. Order here is not significant.
        # # Python note: The 'host' header is added automatically by the Python 'requests' library.
        headers = {}
        for h in headers_to_sign:
            headers[h] = headers_to_sign[h]
            headers[self.header_name_authorization] = authorization_header

        return headers

    # Key derivation functions. See:
    @staticmethod
    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def get_signature_key(self, key, date_stamp, region_name, service_name):
        k_date = self.sign((self.hash_keyword + key).encode('utf-8'), date_stamp)
        k_region = self.sign(k_date, region_name)
        k_service = self.sign(k_region, service_name)
        k_signing = self.sign(k_service, 'aws4_request')
        return k_signing


class BaseClient(object):
    def __init__(self, host, ak=None, sk=None, service=None, version=None, region=None):
        self.service = service
        self.host = host
        self.ak = ak
        self.sk = sk
        self.region = region
        self.version = version

    def _call(self, target, dict_request_parameters=None, headers=None):
        # using kop authentication
        if headers is None:
            headers = {}
        url = 'http://%s?' % self.host
        if isinstance(dict_request_parameters, str):
            dict_request_parameters = eval(dict_request_parameters)
        dict_request_parameters['Version'] = self.version

        request_parameters = "Action=%s&" % target + '&'.join(
            ["%s=%s" % (k, urllib.quote(str(dict_request_parameters[k]), ''))
             for k in sorted(dict_request_parameters.keys())])
        url += request_parameters

        composer = RequestComposer(ak=self.ak, sk=self.sk, service=self.service,
                                   request_parameters=request_parameters, method='GET')
        headers = composer.get_headers(host=self.host, region=self.region,
                                       payload="", additional_signing_headers=headers)
        r = requests.get(url, headers=headers)
        return r
