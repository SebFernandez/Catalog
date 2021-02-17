from flask import Blueprint, url_for, render_template, request, redirect, session
from flask_login import login_required, current_user
from application.models import Content
from operator import add, itemgetter

from . import db
import requests

main = Blueprint('main', __name__)

'''

# TODO
    - Add users.
    - Unit test.
    - Clean Code.

'''

add_list = []
srch_list = []
delete_list = []
edit_list = []
definitive_edit_list = []
user_search = ""
dlist = []


def delete_items():
    if delete_list:
        for i in delete_list:

            #! Returns models object. movie.id -> ID, movie.name -> name, movie.password -> password.
            content = Content.query.filter_by(name=i).first()

            if (content):
                db.session.delete(content)
                db.session.commit()

        delete_list.clear()


def delete_full_db():
    Content.query.delete()
    db.session.commit()


@main.route('/', methods=["GET", "POST"])
def index():
    edit_list.clear()
    definitive_edit_list.clear()
    
    if request.method == "POST":
        titles = request.form.getlist ("active-item")
        
        if request.form.get ("delete") == 'delete':            
            
            for i in titles:
                delete_list.append(i)
                
            delete_items ()
            return redirect (url_for ('main.index'))
        
        elif request.form.get ("edit") == 'edit':
            
            for i in titles:
                
                edit_list.append(i)
            
            return redirect (url_for ('main.edit'))

    return render_template("index.html", user=current_user, edit=False)

#! This path will perform searches.
@main.route('/search', methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        user_search = request.form.get("name").replace(' ', '+')
        srch_list.append(user_search)

        return redirect(url_for('main.search_results', name=user_search))
    
    return render_template ("search.html", user=current_user)

#! This path will add search results to DB
@main.route ('/search/results', methods = ["GET", "POST"])
@login_required
def search_results():
    d = {}
    
    if request.method == "GET" and srch_list:
        dlist.clear()
            
        URL = 'https://www.omdbapi.com/?s=' + srch_list [0] + '&apikey=678cd26e'
            
        srch_list.clear()
                
        q = requests.get(url=URL)
        r = q.json()
                
        if q.status_code == 200:
            if r['Response'] == 'True':
                for i in r['Search']:
                    d = {
                        'Title' : i.get ('Title'),
                        'Year' : i.get ('Year'),
                        'Type': i.get ('Type').capitalize(),
                    }
                                
                    dlist.append (d)

                res_list = sorted (dlist, key=itemgetter ('Title'), reverse=False)
                    
                return render_template ("search.html", user=current_user, table=True, list = res_list)                
    elif request.method == "POST":
        add_list = request.form.getlist ('active-item')
            
        for i in add_list:
            if Content.query.filter_by(name=i).count() < 1:
                    
                URL = 'https://www.omdbapi.com/?t=' + i + '&apikey=678cd26e'
            
                q = requests.get(url=URL)
                r = q.json()
                    
                if q.status_code == 200:
                    if r['Response'] == 'True':
                        d = {
                            'Title': r['Title'],
                            'Year' : r['Year'],
                            'Genre': r['Genre'],
                            'Rating' : float (r['imdbRating']),
                            'Type': r['Type'].capitalize()
                        }
                
                    new_content = Content (name=d['Title'], year=d['Year'], genre=d['Genre'], rating = d['Rating'], content_type= d['Type'], user_id = current_user.id)
                    
                    db.session.add (new_content)
                    db.session.commit ()
            
        add_list.clear ()
    
    return redirect (url_for("main.index"))               

@main.route ('/edit', methods = ["GET", "POST"])
@login_required
def edit ():
    edit_dict = {}
    
    if request.method == "GET":
        if edit_list:                
            for i in edit_list:
                title = Content.query.filter_by(name=i).first()
                    
                edit_dict = {
                    'Title': title.name,
                    'Year': title.year,
                    'Genre': title.genre,
                    'Rating': title.rating,
                    'User-Rating': title.user_rating,
                    'Type': title.content_type
                }
                
                definitive_edit_list.append(edit_dict)
                
            return render_template ("index.html", user = current_user, edit = True, content = definitive_edit_list)
                    
    elif request.method == "POST":
        if request.form.getlist ('your-rating'):
            user_rating = request.form.getlist ('your-rating')
                
            for u in user_rating:
                for i in edit_list:
                    title = Content.query.filter_by(name=i).first()
                    
                    if u:
                        title.user_rating = u
                        db.session.commit ()

    return redirect (url_for ('main.index'))
