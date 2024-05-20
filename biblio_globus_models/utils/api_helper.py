import requests
from biblio_globus_models.utils.logging_and_attaching_api import response_logging, response_attaching


def api_request(base_api_url, endpoint, method, data=None, params=None, allow_redirects=None):
    url = f"{base_api_url}{endpoint}"
    response = requests.request(method, url, data=data, params=params, allow_redirects=allow_redirects)
    response_logging(response)
    response_attaching(response)
    return response
