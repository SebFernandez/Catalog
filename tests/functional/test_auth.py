'''
This file will test GETs and POSTs on the blueprint with name AUTH
'''

def test_login_page_get (test_client):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    '''
    
    response = test_client.get ('/auth/login')
    assert response.status_code == 200
    
def test_login_logout_page_post (test_client, init_database):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted (POST) with a valid user
    THEN check the response is valid
    '''
    response = test_client.post ('/auth/login',
                                 data=dict(email='test1@test.com', password='1313'),
                                 follow_redirects=True)
    assert response.status_code == 200

#! Problem with @login_required
'''
def test_logout_page_get (test_client):
    ''''''
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    ''''''
    
    response = test_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
'''

'''
#!Needs to have flash message.    
def test_login_page_post (test_client, init_database):
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted (POST) with a wrong user
    THEN check the response is valid
    
    response = test_client.post ('/auth/login',
                                 data=dict(email='tst1@test.com', password='1312'),
                                 follow_redirects=True)
    assert response.status_code == 200
''' 
    
def test_sign_in_page_get (test_client):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/sign-in' page is requested (GET)
    THEN check the response is valid
    '''
    
    response = test_client.get ('/auth/sign-in')
    assert response.status_code == 200
    
def test_sign_in_page_post (test_client, init_database):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/sign-in' page is posted (POST)
    THEN check the response is valid
    '''
    
    response = test_client.post ('/auth/sign-in',
                                 data=dict(username='test3',email='test3@test.com', password='1234'),
                                 follow_redirects=True)
    
    assert response.status_code == 200
    