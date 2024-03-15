import ckan.plugins as p


def logisymphony_resource_embed(context, data_dict, privilege='resource_update'):
    if 'id' not in data_dict:
        data_dict['id'] = data_dict.get('resource_id')

    user = context.get('user')

    try:
        p.toolkit.check_access(privilege, context, data_dict)
    except:
        return {
            'success': False,
            'msg': p.toolkit._(
                'User {0} not authorized to update resource {1}'
                    .format(str(user), data_dict['id'])
            )
        }
    else:
        return {'success': True}

def logisymphony_sysadmin_embed(context, data_dict):
    # Only sysadmins can access this
    return {'success': False}
