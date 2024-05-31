from flask import Blueprint
from flask.views import MethodView

import ckan.model as model
import ckanext.logisymphony.utils as utils
from ckan.plugins.toolkit import (
    ObjectNotFound, NotAuthorized, get_action,
    check_access, abort, render, c, g, _
)

logisymphony = Blueprint(u'logisymphony', __name__)


class LogiSymphonyView(MethodView):

    @staticmethod
    def resource_embed(id, resource_id):
        # resource_edit_base template uses these
        try:
            pkg_dict = get_action(u'package_show')(None, {u'id': id})
            resource = get_action(u'resource_show')(None, {u'id': resource_id})
        except (ObjectNotFound, NotAuthorized):
            return abort(404, _("Resource not found"))

        try:
            context = {
                u'model': model,
                u'user': g.user,
                u'auth_user_obj': g.userobj
            }
            check_access('logisymphony_resource_embed', context, {u'id': resource_id})
        except NotAuthorized:
            abort(404, _(u'Resource not found'))

        data_dict = {
            'pkg_dict': pkg_dict,
            'resource': resource
        }

        # global variables for backward compatibility
        c.pkg_dict = data_dict[u'pkg_dict']
        c.resource = data_dict[u'resource']

        return render(u'logisymphony/resource_embed.html', data_dict)


    def sysadmin_embed():
        try:
            context = {
                u'model': model,
                u'user': g.user,
                u'auth_user_obj': g.userobj
            }
            check_access('logisymphony_sysadmin_embed', context, {})
        except NotAuthorized:
            abort(404, _(u'Resource not found'))

        return render(u'logisymphony/sysadmin_embed.html')


    def get_logi_dashboards():
        try:
            context = {
                u'model': model,
                u'user': g.user,
                u'auth_user_obj': g.userobj
            }
            check_access('logisymphony_sysadmin_embed', context, {})
        except NotAuthorized:
            abort(404, _(u'Resource not found'))

        dashboard_list = utils.get_logi_project_dashboards()
        data = {
            'results': dashboard_list
        }
        return data


logisymphony.add_url_rule(
    u'/dataset/<id>/reporting/<resource_id>',
    view_func=LogiSymphonyView.resource_embed
)
logisymphony.add_url_rule(
    u'/reporting',
    view_func=LogiSymphonyView.sysadmin_embed
)
logisymphony.add_url_rule(
    u'/get_logi_dashboards',
    view_func=LogiSymphonyView.get_logi_dashboards,
    methods=[u'GET']
)
