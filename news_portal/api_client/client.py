import requests


class NewsAPIClient:
    def __init__(self, base_url, token=None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if token:
            self.session.headers.update({'Authorization': f'Token {token}'})

    def register(self, username, email, password):
        return self.session.post(f"{self.base_url}/api/users/", json={
            'username': username, 'email': email, 'password': password
        }).json()

    def login(self, username, password):
        # Для токеновой аутентификации
        resp = self.session.post(f"{self.base_url}/api/token/", json={
            'username': username, 'password': password
        })
        if resp.status_code == 200:
            self.session.headers.update({'Authorization': f"Token {resp.json()['token']}"})
        return resp.json()

    def create_news(self, title, content, summary=""):
        return self.session.post(f"{self.base_url}/api/news/", json={
            'title': title, 'content': content, 'summary': summary
        }).json()

    def get_news(self, news_id=None):
        url = f"{self.base_url}/api/news/{news_id}/" if news_id else f"{self.base_url}/api/news/"
        return self.session.get(url).json()

    def update_news(self, news_id, **kwargs):
        return self.session.patch(f"{self.base_url}/api/news/{news_id}/", json=kwargs).json()

    def delete_news(self, news_id):
        return self.session.delete(f"{self.base_url}/api/news/{news_id}/").status_code


class APIError:
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response