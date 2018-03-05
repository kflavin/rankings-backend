from flask import request, current_app, url_for, jsonify, abort
from . import status

@status.route('/', methods=['GET'])
def status():
    """
    Query parameters:
        count: return "count" per page
        empty_only: if true return only companies with an empty industry or sector field.  else return all companies.
    Returns:
        json response
    """

    return jsonify({"status": "Good"})
