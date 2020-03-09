#!/usr/bin/python3
import json
import logging
import os
import uuid
from datetime import datetime
from pdb import set_trace
from pprint import pprint

import flask
import jsonschema
import requests as HTTP_REQUESTS

import flask_fat

Journal = self = flask_fat.Journal(__file__)

""" ------------------------------- ROUTES ------------------------------- """

@Journal.BP.route('/%s/add_event' % (Journal.name), methods=['POST'])
def add_subscribe():
    """
        Subscribe to an Add event.
    """
    response = {}
    status = 'nothing'
    code = 200
    body = flask.request.get_json()

    callback_endpoint = body.get('callback', None)
    endpoint_alias = body.get('alias', None)
    if not endpoint_alias:
        endpoint_alias = callback_endpoint

    if callback_endpoint is None:
        response['error'] = 'No callback in body!\n%s' % body
        status = 'error'
        code = 400
    else:
        if endpoint_alias in Journal.mainapp.add_callback:
            status = 'Endpoint alias "%s" already in the list.' % endpoint_alias
            code = 403
        elif callback_endpoint in Journal.mainapp.add_callback.values():
            status = 'Endpoint "%s" already in the list.' % callback_endpoint
            code = 403
        else:
            status = 'Callback endpoint %s added' % callback_endpoint
            if endpoint_alias != callback_endpoint:
                status = '%s with the alias name "%s"' % (status, endpoint_alias)

            Journal.mainapp.add_callback[endpoint_alias] = callback_endpoint

    response['status'] = status

    return flask.make_response(flask.jsonify(response), code)
