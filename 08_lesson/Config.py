class config:
    def __init__(self):
        self.api_key = "api_key"
        self.user_id = "user_id"
        self.base_url = "https://ru.yougile.com/api-v2"
        self.project_id = None

    def post_body(self):
        return {
            "title": "test",
            "users": {
                self.user_id: "admin"
            }
        }

    def post_body_negative(self):
        return {
            "title": "test",
            "users": {
                "123": "admin"
            }
        }

    def put_body(self):
        return {
            "title": "test"
        }

    def headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def put_url(self):
        if self.project_id:
            return f"{self.base_url}/projects/{self.project_id}"
        return None

    def put_url_negative(self):
        if self.project_id:
            return f"{self.base_url}/projects/"
        return None

    def get_url(self):
        if self.project_id:
            return f"{self.base_url}/projects/{self.project_id}"
        return None

    def post_url(self):
        return f"{self.base_url}/projects"


config = config()
