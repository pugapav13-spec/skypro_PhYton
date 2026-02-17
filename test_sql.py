import pytest
from sqlalchemy import Column, Integer, String
from config import SessionLocal, Base


class Subject(Base):
    __tablename__ = "subject"
    subject_id = Column(Integer, primary_key=True, index=True)
    subject_title = Column(String)


@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()


# ДОБАВЛЕНИЕ
def test_add_subject(db_session):
    new_id = 999
    new_title = "Automation Testing"
    new_subject = Subject(subject_id=new_id, subject_title=new_title)
    db_session.add(new_subject)
    db_session.commit()
    result = db_session.query(Subject).filter_by(subject_id=new_id).first()
    assert result is not None
    assert result.subject_title == new_title

    db_session.delete(result)
    db_session.commit()


# ИЗМЕНЕНИЕ
def test_update_subject(db_session):
    test_id = 1000
    subject = Subject(subject_id=test_id, subject_title="Old Title")
    db_session.add(subject)
    db_session.commit()
    subject.subject_title = "New Title"
    db_session.commit()

    updated_subject = db_session.query(Subject).filter_by(
        subject_id=test_id).first()
    assert updated_subject.subject_title == "New Title"

    db_session.delete(updated_subject)
    db_session.commit()


# УДАЛЕНИЕ
def test_delete_subject(db_session):
    test_id = 1001
    subject = Subject(subject_id=test_id, subject_title="To be deleted")
    db_session.add(subject)
    db_session.commit()

    db_session.delete(subject)
    db_session.commit()

    result = db_session.query(Subject).filter_by(subject_id=test_id).first()
    assert result is None
