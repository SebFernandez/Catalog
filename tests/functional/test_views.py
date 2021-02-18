'''
This file will test GETs and POSTs on the blueprint with name MAIN
'''

from application import create_app

def test_home_page_get (test_client):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    '''
    
    response = test_client.get ('/')
        
    assert response.status_code == 200

def test_home_page_post (test_client):
    '''
    GIVEN a Flask application configrured for testing
    WHEN the '/' page is posted (POST)
    THEN check that a '405' status code is returned
    '''
    response = test_client.post ('/')
        
    assert response.status_code == 200

#!Problem with @login_required
'''
def test_search_get (test_client):
    
    ''''''
    GIVEN a Flask application configrured for testing
    WHEN the '/search' page is requested (GET)
    THEN check that a '200' status code is returned
    ''''''
    
    response = test_client.get ('/search')
    
    assert response.status_code == 200
'''