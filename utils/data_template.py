import json
import logging
import os
import re


logger = logging.getLogger(__name__)


class DataTemplate():
    def __init__(self, template_name: str):
        self.template = self._read_template(template_name)

    def get_field_attr(self, field_name: str, attr: str) -> str:
        for field in self.template['fields']:
            if field['name'] == field_name:
                return field.get(attr, None)
        return None

    def _read_template(self, template_name: str) -> dict:
        filename = 'data_templates/' + self._to_snake_case(template_name) + '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except OSError as e:
            logger.critical('Failed to open data template {}'.format(filename))
            return None

    def _to_snake_case(self, string: str) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()
