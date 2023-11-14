from typing import Optional
import requests

class RequestHandler:
    
    base_url = "http://127.0.0.1:8000"
    
    @staticmethod
    def make_get_request(endpoint):
        # Implement GET request logic here
        print(f"Making GET request to {RequestHandler.base_url}")
    
        response = requests.get(f"{RequestHandler.base_url}{endpoint}")

        if response.status_code == 200:
            resposta_json = response.json()
            print(resposta_json)
            return resposta_json
            
        else:
            print('Failed to get:', response.status_code)
            return {'error': 'failed to get'}

        # # Define the login credentials
        

    @staticmethod
    def make_post_request(endpoint, data : Optional[dict[str, str]] = None):
        # Implement POST request logic here
        print(f"Making POST request to {RequestHandler.base_url} with data {data}")
        # Your actual POST request implementation
        
        # login_data = {
        #     'username': 'admin',
        #     'password': '1234'
        # }

        # Make a POST request to get the access token
        response = requests.post(f"{RequestHandler.base_url}/{endpoint}", data=data)

        if response.status_code == 200:
            token = response.json()
            access_token = token['access_token']
            # print('Access Token:', access_token)
            return token
        else:
            print('Failed to get token:', response.status_code)
            return {"error" : "failed to get token"}