from application.auth import login
import pytest
from application import create_app, db
from application.models import User, Content

#! To run pytest do: python3 -m pytest -v

@pytest.fixture (scope = 'module')
def new_user ():
    user = User ('test', 'test@test.com', '1234')
    return user

@pytest.fixture (scope = 'module')
def new_content():
    content = Content ("Attack on Titan", "2013", "Anime", "10", "Series", "1")
    return content

@pytest.fixture (scope = 'module')
def test_client (new_user):
    flask_app = create_app ()
    
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User('test1', 'test1@test1.com', '1313')
    user2 = User('test2', 'test2@test2.com', '1515')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()