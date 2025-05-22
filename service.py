import requests
import logging


class ApiClient:
    @staticmethod
    def get_user_data(user_id):
        response = requests.get(f"https://api.example.com/users/{user_id}")
        if response.status_code == 200:
            return response.json()
        raise ValueError("API request failed")


class UserService:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_username(self, user_id):
        user_data = self.api_client.get_user_data(user_id)
        logging.info(f"user_data: {user_data}")
        return user_data["name"].upper()
