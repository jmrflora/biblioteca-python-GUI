import requests
from datetime import datetime, timedelta

class BackendTokenHandler:
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.base_url = "http://127.0.0.1:8000"
            self.token_endpoint = None
            self.refresh_token_endpoint = None
            self.access_token = None
            self.refresh_token = None
            self.initialized = True

    def initialize_with_credentials(self, token_endpoint, refresh_token_endpoint, username, passwd):
        self.token_endpoint = token_endpoint
        self.refresh_token_endpoint = refresh_token_endpoint
        self._get_new_token(username, passwd)
        
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
            response = requests.post(url, headers=headers, data=data)
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

        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Request failed: {response.status_code}")