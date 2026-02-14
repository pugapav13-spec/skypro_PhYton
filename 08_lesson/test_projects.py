# POST

def test_create_project_positive(projects_page):
    title = "New Project"
    response = projects_page.create(title)
    assert response.status_code == 201

    data = response.json()
    assert "id" in data, "Сервер не вернул ID"
    project_id = data["id"]

    get_response = projects_page.get_by_id(project_id)
    assert get_response.json()["title"] == title

    projects_page.update(project_id, deleted=True)


def test_create_project_negative(projects_page):
    response = projects_page.create("")
    assert response.status_code == 400
    assert "error" in response.json()


# GET

def test_get_project_positive(projects_page, temp_project):
    response = projects_page.get_by_id(temp_project)
    assert response.status_code == 200
    assert response.json()["id"] == temp_project


def test_get_project_negative(projects_page):
    response = projects_page.get_by_id("non-existent-id-123")
    assert response.status_code == 404
    assert "error" in response.json()


# [PUT]

def test_update_project_positive(projects_page, temp_project):
    new_title = "Updated Title"
    response = projects_page.update(temp_project, title=new_title)
    assert response.status_code == 200

    get_resp = projects_page.get_by_id(temp_project)
    assert get_resp.json()["title"] == new_title


def test_update_project_negative(projects_page):
    response = projects_page.update("invalid-id-format", title="New")
    assert response.status_code == 404
    assert "error" in response.json()
