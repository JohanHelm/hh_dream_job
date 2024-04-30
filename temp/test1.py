from api_requests.api_querry import ApiClient
from utils.tokens_handler import TokensHandler
from secrets.tokens import tokens
from utils.basic_params import basic_url

api_client = ApiClient()
tokens_handler = TokensHandler(api_client)
attributes = tokens_handler.__dict__

print(attributes)

assert isinstance(attributes["api_client"], ApiClient) and attributes["tokens"] == tokens and attributes["url"] == f"{basic_url}/token"

