import yaml as yaml_loader

from shaibos.invoice import from_list_enumerate


def load_invoices_from_yaml_string(yaml_string):
    yaml_invoices = yaml_loader.safe_load(yaml_string)
    return from_list_enumerate(yaml_invoices['invoices'])


def load_invoices_from_yaml_file(yaml_path):
    yaml_string = open(yaml_path, 'r').read()
    return load_invoices_from_yaml_string(yaml_string=yaml_string)
