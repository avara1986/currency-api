# encoding: utf-8
from __future__ import absolute_import, unicode_literals, print_function

import json
import logging
from http.client import RemoteDisconnected

import requests
from requests.exceptions import ConnectionError, ConnectTimeout

logger = logging.getLogger(__name__)


class Request(object):
    headers = {'content-type': 'application/json'}
    base_url = ""

    def __init__(self, base_url, *args, **kwargs):
        if base_url:
            self.base_url = base_url

    def get_full_url(self):
        return self.base_url + self.url

    def parse_exceptions(self, exception):
        logger.exception(exception)
        response = str(exception)
        return response

    def request(self, url, method, data, files=None, headers={}):
        """

        :param str url:
        :param str method:
        :param dict data:
        :param dict headers:
        :return: str
        """
        content = "{}"
        response = False
        self.url = url
        request_params = {"url": self.get_full_url()}

        if headers:
            request_params.update({"headers": headers})

        if method == "get":
            request_params.update({"params": data})
        else:  # pragma: no cover
            if headers.get("content-type") == "application/json":
                request_params.update({"json": data})
            else:
                request_params.update({"data": data})
            if files:
                request_params.update({"files": files})
        try:
            try:
                # Si dentro de los parámetros va un BytesIO o StringIO puede petar
                logger.info("{}".format(json.dumps(request_params)))
            except TypeError:
                logger.error("Params: {}".format(request_params))
            response = getattr(requests, method)(**request_params)
            logger.debug("Response: {}".format(response))
            logger.debug("Response result: [{}] {}".format(response.status_code, json.dumps(response.text)))
            content = json.loads(response.text)
        except ConnectTimeout as exception:
            content = self.parse_exceptions(exception)
        except ConnectionError as exception:
            content = self.parse_exceptions(exception)
        except RemoteDisconnected as exception:
            content = self.parse_exceptions(exception)

        return response, content
