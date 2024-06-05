import logging
import requests
import ckanext.logisymphony.utils as utils

log = logging.getLogger(__name__)


class LogiManagedDashboardAPI(object):
    """ Handles requests to the Logi Symphony Managed API
    """

    def __init__(self, logi_url, account_name, password):
        self.logi_url = logi_url
        self.account_name = account_name
        self.password = password

    def __enter__(self):
        data_dict = {
            'accountName': self.account_name,
            'password': self.password,
            'deleteOtherSessions': True
        }
        response = self.logi_request('post', 'api/logon/', data_dict)
        self.sessionId = response['sessionId']
        return self

    def __exit__(self, *args):
        data_dict = {
            'sessionId': self.sessionId
        }
        self.logi_request('post', 'api/session/delete/', data_dict)
        self.sessionId = None
        return self
        
    def logi_request(self, request_type, api_uri, data=None):
        logi_url = self.logi_url
        api_endpoint = '{0}/managed/{1}'.format(logi_url, api_uri)
        headers = {
            'Content-Type': 'application/json'
        }
        if hasattr(self, 'sessionId') and self.sessionId:
            headers['Authorization'] = 'Bearer ' + self.sessionId

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
            log.error('Error making request to Logi Symphony: {0}'.format(r.text))

    def get_logi_project_id(self):
        # Get Open Data project
        project_list = self.logi_request('get', 'api/project/', {})
        for project in project_list:
            if project.get('name') == 'Open Data':
                project_id = project.get('projectId')
                return project_id
        log.error('Open Data project not found in Logi Symphony')
        return


def get_logi_project_dashboards():
    logi_url = utils.get_logi_url()
    account_name = utils.get_logi_account_name()
    password = utils.get_logi_password()

    with LogiManagedDashboardAPI(logi_url, account_name, password) as logi_api:
        project_id = logi_api.get_logi_project_id()

        if not project_id:
            return []

        # Query project
        query_dict = {
            'pageSize': 100,
            'pageNumber': 1,
            'searchTerm': None,
            'projectId': project_id,
            'excludedIds': [],
            'filter': []
        }
        query_response = logi_api.logi_request('post', 'api/project/getallprojectitems', query_dict)
        dashboard_list = []
        for item in query_response:
            if item.get('objectType') == 'Dashboard':
                dashboard_dict = {}
                dashboard_dict['id'] = item.get('id')
                dashboard_dict['name'] = item.get('name')
                dashboard_dict['text'] = item.get('name')
                dashboard_dict['lastModifiedTime'] = item.get('lastModifiedTime')
                dashboard_list.append(dashboard_dict)
        sorted_dashboard_list = sorted(dashboard_list, key=lambda d: d['lastModifiedTime'], reverse=True)
        return sorted_dashboard_list