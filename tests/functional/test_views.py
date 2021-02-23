'''
This file will test GETs and POSTs on the blueprint with name VIEWS
'''

import pytest

def test_home_page (test_client):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    '''
    
    response = test_client.get ('/')    
    assert response.status_code == 200
    
    '''
    GIVEN a Flask application configrured for testing
    WHEN the '/' page is posted (POST)
    THEN check that a '405' status code is returned
    '''
    response = test_client.post ('/')
    assert response.status_code == 200

@pytest.mark.parametrize ('user_search', ["star wars", "friends"])
def test_search (test_client, user_search):
    '''
    GIVEN a Flask application configrured for testing
    WHEN the '/search' page is requested (GET)
    THEN check that a '200' status code is returned
    '''
    
    response = test_client.get ('/search')
    assert response.status_code == 200
    
    '''
    GIVEN a Flask application configrured for testing
    WHEN the '/search' page is posted (POST)
    THEN check that a '200' status code is returned
    '''
    
    response = test_client.post ('/search',
                               data=dict(name=user_search),
                               follow_redirects=True)
    assert response.status_code == 200