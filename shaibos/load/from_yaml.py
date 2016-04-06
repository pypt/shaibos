import yaml as yaml_loader

from shaibos.invoice import from_list_enumerate


def load_invoices_from_yaml(yaml_path):
    yaml_file = open(yaml_path, 'r')
    yaml_invoices = yaml_loader.load(yaml_file)
    return from_list_enumerate(yaml_invoices['invoices'])
