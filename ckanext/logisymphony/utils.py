import requests
from ckantoolkit import config


def get_logi_url():
    return config.get('ckanext.logisymphony.url', '')

def get_logi_account_name():
    return config.get('ckanext.logisymphony.account_name', '')

def get_logi_password():
    return config.get('ckanext.logisymphony.password', '')
