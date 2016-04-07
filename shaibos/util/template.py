import os

from pkg_resources import resource_filename, Requirement


def default_template_path():
    template_path = 'shaibos/templates/basic.jinja2'

    # Try local path
    local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../', template_path)
    if os.path.exists(local_path):
        return local_path

    # Try package resource path
    package_path = resource_filename(Requirement.parse("shaibos"), template_path)
    if os.path.exists(package_path):
        return package_path

    return None
