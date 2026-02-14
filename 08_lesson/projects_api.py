import requests


class ProjectsPage:
    def __init__(self, base_url, token):
        self.base_url = base_url.strip("/")
        self.url = f"{self.base_url}/projects"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def create(self, title: str):
        return requests.post(self.url, json={"title": title},
                             headers=self.headers)

    def get_by_id(self, project_id: str):
        return requests.get(f"{self.url}/{project_id}", headers=self.headers)

    def update(self, project_id: str, title: str = None,
               deleted: bool = False):
        payload = {"deleted": deleted}
        if title:
            payload["title"] = title
        return requests.put(f"{self.url}/{project_id}", json=payload,
                            headers=self.headers)
