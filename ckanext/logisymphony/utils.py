import requests
from ckantoolkit import config


def get_logi_url():
    return config.get('ckanext.logisymphony.url', '')

def get_logi_account_name():
    return config.get('ckanext.logisymphony.account_name', '')

def get_logi_password():
    return config.get('ckanext.logisymphony.password', '')


def logi_request(request_type, api_uri, data=None, sessionId=None):
    logi_url = get_logi_url()
    api_endpoint = '{0}/managed/{1}'.format(logi_url, api_uri)
    headers = {
        'Content-Type': 'application/json'
    }
    if sessionId:
        headers['Authorization'] = 'Bearer ' + sessionId

    if request_type == 'post':
        r = requests.post(
            api_endpoint,
            json=data,
            headers=headers
        )
    elif request_type == 'put':
        r = requests.put(
            api_endpoint,
            json=data,
            headers=headers
        )
    elif request_type == 'get':
        r = requests.get(
            api_endpoint,
            headers=headers
        )

    try:
        return r.json()
    except:
        print(api_endpoint)
        print(r.status_code)
        print(r.text)


def get_logi_session():
    # Get Logi session
    account_name = get_logi_account_name()
    password = get_logi_password()
    data_dict = {
        'accountName': account_name,
        'password': password,
        'deleteOtherSessions': True
    }
    response = logi_request('post', 'api/logon/', data_dict)
    print(response)
    return response['sessionId']


def get_logi_project_id(sessionId):
    # Get Open Data project
    project_list = logi_request('get', 'api/project/', {}, sessionId)
    for project in project_list:
        if project.get('name') == 'Open Data':
            project_id = project.get('projectId')
            return project_id
    print('Open Data project not found')
    return


def get_logi_project_dashboards():
    sessionId = get_logi_session()
    project_id = get_logi_project_id(sessionId)

    # Query project
    query_dict = {
        'pageSize': 100,
        'pageNumber': 1,
        'searchTerm': None,
        'projectId': project_id,
        'excludedIds': [],
        'filter': []
    }
    query_response = logi_request('post', 'api/project/getallprojectitems', query_dict, sessionId)
    dashboard_list = []
    for item in query_response:
        if item.get('objectType') == 'Dashboard':
            dashboard_dict = {}
            dashboard_dict['id'] = item.get('id')
            dashboard_dict['name'] = item.get('name')
            dashboard_dict['text'] = item.get('name')
            dashboard_dict['lastModifiedTime'] = item.get('lastModifiedTime')
            dashboard_list.append(dashboard_dict)
    return dashboard_list
