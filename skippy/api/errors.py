import requests


ConnectionErrors = (requests.ConnectionError, requests.Timeout)


__all__ = ["ConnectionErrors"]
