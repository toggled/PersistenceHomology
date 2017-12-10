__author__ = 'Naheed'

import uuid
import hashlib


# def getId():
#     """
#     :returns unique integer id each time called
#     """
#     return uuid.uuid1()


def getId(key):
    """
    :returns
    """
    return hashlib.sha1(key).hexdigest()
