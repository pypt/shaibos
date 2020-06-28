import os

from pkg_resources import resource_filename, Requirement


def resolve_resource(path):
    # Try local path
    local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../', path)
    if os.path.exists(local_path):
        return local_path

    # Try package resource path
    package_path = resource_filename(Requirement.parse("shaibos"), path)
    if os.path.exists(package_path):
        return package_path

    return None


def default_template_path():
    return resolve_resource('shaibos/templates/basic.jinja2')


def default_journal_template_path():
    return resolve_resource('shaibos/templates/basic_journal.jinja2')
