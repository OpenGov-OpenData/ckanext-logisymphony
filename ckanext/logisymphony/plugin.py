from six import text_type

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.logisymphony.auth as auth
import ckanext.logisymphony.utils as utils
import ckanext.logisymphony.blueprint as view

ignore_empty = toolkit.get_validator('ignore_empty')


class LogisymphonyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_resource('assets', 'logisymphony')
        toolkit.add_public_directory(config_, 'public')

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_logi_url': utils.get_logi_url
        }

    # IAuthFunctions
    def get_auth_functions(self):
        return {
            'logisymphony_resource_embed': auth.logisymphony_resource_embed,
            'logisymphony_sysadmin_embed': auth.logisymphony_sysadmin_embed
        }

    # IBlueprint
    def get_blueprint(self):
        u'''Return a Flask Blueprint object to be registered by the app.'''
        return view.logisymphony


class LogisymphonyViewPlugin(plugins.SingletonPlugin):
    '''This plugin makes views of Logi Symphony dashboards'''
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IResourceView, inherit=True)

    # IConfigurer
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')

    # IResourceView
    def info(self):
        return {
            'name': 'logisymphony_view',
            'title': 'Logi Symphony',
            'default_title': 'Dashboard',
            'icon': 'pie-chart',
            'always_available': False,
            'iframed': True,
            'preview_enabled': False,
            'schema': {
                'dashboard_id': [ignore_empty, text_type]
            },
        }

    def can_view(self, data_dict):
        resource = data_dict['resource']
        return resource.get(u'datastore_active')

    def view_template(self, context, data_dict):
        return 'logisymphony/logisymphony_view.html'

    def form_template(self, context, data_dict):
        return 'logisymphony/logisymphony_form.html'
