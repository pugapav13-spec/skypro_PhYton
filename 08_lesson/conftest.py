import pytest
from projects_api import ProjectsPage


@pytest.fixture(scope="session")
def projects_page():
    token = "IsG-1B2xwPXyBbHUwlcyHUUF45AYPFIaYimpaASCOA6f2HDJ-bNs9jFchUkhApeV"
    base_url = "https://ru.yougile.com/api-v2"
    return ProjectsPage(base_url, token)


@pytest.fixture
def temp_project(projects_page):
    response = projects_page.create("X Project")
    project_id = response.json()["id"]

    yield project_id

    projects_page.update(project_id, deleted=True)
