import requests
import json
from datetime import datetime, timedelta

class BackendTokenHandler:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, base_url=None, token_endpoint=None, refresh_token_endpoint=None):
        if not hasattr(self, 'initialized'):
            self.base_url = base_url
            self.token_endpoint = token_endpoint
            self.refresh_token_endpoint = refresh_token_endpoint
            self.access_token = None
            self.refresh_token = None
            self.tipo = None
            self.initialized = True

    def initialize_with_credentials(self, username, passwd):
        self._get_new_token(username, passwd)

    def close(self):
        self.access_token = None
        self.refresh_token = None
        self.tipo = None

    def _get_new_token(self, username, passwd):
        token_response = requests.post(
            f"{self.base_url}/{self.token_endpoint}",
            data={
                "username": username, "password": passwd
            },
        )

        if token_response.status_code == 200:
            token_data = token_response.json()
            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")
        else:
            raise ValueError(f"Failed to obtain token: {token_response.status_code}")
    
    def refresh_access_token(self):
        token_response = requests.post(
            f"{self.base_url}/{self.refresh_token_endpoint}",
            data={
                "refresh_token": self.refresh_token
            },
        )
        if token_response.status_code == 200:
            token_data = token_response.json()
            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")
        else:
            raise ValueError(f"Failed to obtain token: {token_response.status_code}")

    def get_token(self):
        if self.access_token is None:
            self._get_new_token()
        return self.access_token

    
    def make_authenticated_request(self, method, endpoint, data=None):
        headers = {"Authorization": f"Bearer {self.get_token()}"}
        url = f"{self.base_url}{endpoint}"

        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=json.dumps(data))
        elif method == "PATCH":
            print("patch")
            print(data)
            # 'Content-Type: application/json'
            # novo_headers = {"Authorization": f"Bearer {self.get_token()}"}
            response = requests.patch(url, headers=headers, data=json.dumps(data))
        else:
            raise ValueError("Invalid HTTP method. Supported methods: GET, POST")

        if response.status_code == 401:
            # If the token has expired, try to refresh it and retry the request
            self.refresh_access_token()
            headers["Authorization"] = f"Bearer {self.access_token}"

            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, data=data)
            elif method == "PATCH":
                response = requests.patch(url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Request failed: {response.status_code}")
        
    def get_tipo(self):
        if self.tipo is None:
            me_response = self.make_authenticated_request("GET", "/usuarios/me")

            self.tipo = me_response.get("tipo")
            
            return self.tipo
        else:
            return self.tipo