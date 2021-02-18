from application.models import Content

def test_new_content (new_content):
    
    '''
    GIVEN a new content
    WHEN user has performed a search
    THEN check name, year, genre, rating, content type
    '''
    
    assert new_content.name == 'Attack on Titan'
    assert new_content.year == '2013'
    assert new_content.genre == 'Anime'
    assert new_content.rating == '10'
    assert new_content.content_type == 'Series'
    assert new_content.user_id == '1'