'''
This file will test Models.py.
'''

from application.models import Content, User

def test_new_content (new_content):
    '''
    GIVEN a new content 
    WHEN user has performed a search and added to DB
    THEN check name, year, genre, rating, content type
    '''
    
    assert new_content.name == 'Attack on Titan'
    assert new_content.year == '2013'
    assert new_content.genre == 'Anime'
    assert new_content.rating == '10'
    assert new_content.content_type == 'Series'
    assert new_content.user_id == 1    
    
    assert isinstance (new_content.name, str) == True
    assert isinstance (new_content.year, str) == True
    assert isinstance (new_content.genre, str) == True
    assert isinstance (new_content.rating, str) == True
    assert isinstance (new_content.content_type, str) == True
    assert isinstance (new_content.user_id, int) == True
    
def test_new_user (new_user):
    '''
    Given a User model
    When a new User is created
    THEN check username, email and password
    '''
    
    assert new_user.username == 'test'
    assert new_user.email == 'test@test.com'
    assert new_user.password == '1234'
    
    assert isinstance (new_user.username, str) == True
    assert isinstance (new_user.email, str) == True
    assert isinstance (new_user.password, str) == True