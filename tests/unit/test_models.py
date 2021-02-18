from application.models import User

def test_new_user (new_user):
    
    '''
    Given a User model
    When a new User is created
    THEN check username, email and password
    '''
    
    assert new_user.username == 'test'
    assert new_user.email == 'test@test.com'
    assert new_user.password == '1234'