import logging

import hammock


logger = logging.getLogger(__name__)


class APIClient(object):

    def __init__(self, api_url, api_key, username, password, company_id, version='1.1.1'):
        """
        Stores the API key and sets up the root API URL with basic auth
        for future Hammock calls
        """
        self.api_key = api_key
        self.company_id = company_id
        self.api = hammock.Hammock(
            '%s/api/%s' % (api_url, version),
            auth=(username, password))

    def __call__(self, verb, service, method, identifier=None, **kwargs):
        """
        Constructs an API call for the parameters passed, in the format:
            VERB /service/method/<identifier>?[kwargs]

        Returns the JSON response.
        """
        # add the service name to the request
        request = getattr(self.api, service)

        # add the method name to the request
        request = getattr(request, method)

        # optionally add the identifier to the request
        if identifier:
            request = getattr(request, identifier)

        # initialise the request headers
        headers = {'Accept': 'application/json'}

        # initialise the request parameters - always add the API key and company id
        params = {'APIKey': self.api_key, 'CompanyId': self.company_id}

        # initialise the POST data
        data = {}

        # update either the request parameters or POST payload with
        # kwargs depending on the request verb
        if verb.upper() == 'POST':
            data.update(kwargs)
        else:
            params.update(kwargs)

        # send the request
        response = getattr(request, verb.upper())(
            params=params, json=data, headers=headers)

        return response.json()
