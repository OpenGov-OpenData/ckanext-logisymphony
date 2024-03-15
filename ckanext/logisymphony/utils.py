from ckantoolkit import config

def get_logi_url():
    return config.get('ckanext.logisymphony.url', '')
