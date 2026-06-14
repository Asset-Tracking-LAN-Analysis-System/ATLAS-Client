import json
import os

from .atlas_api import AtlasApi
from .helper.types import ErrorResponse


class api_handler:
    def __init__(self) -> None:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        self.host = 'localhost'
        self.port = 8000
        try:
            with open(config_path, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
            api_url = str(config.get('api_url', 'localhost'))
            if api_url.startswith('http://'):
                api_url = api_url[len('http://'):]
            elif api_url.startswith('https://'):
                api_url = api_url[len('https://'):]
            self.host = api_url.split(':')[0] if api_url else 'localhost'
            self.port = int(config.get('api_port', 8000))
        except Exception:
            pass
        self.client = AtlasApi()
        self.client.PORT = self.port

    def fetch_data(self):
        response = self.client.get_entity_list(self.host)
        if isinstance(response, ErrorResponse):
            return []
        try:
            return [
                {
                    'id': item.ID,
                    'name': item.NAME,
                }
                for item in response.DATA or []
            ]
        except Exception:
            return []

    def fetch_types(self):
        response = self.client.get_type_list(self.host)
        if isinstance(response, ErrorResponse):
            return []
        try:
            return [item.NAME for item in response.DATA or [] if item.NAME]
        except Exception:
            return []
