from flask import Blueprint, url_for, render_template, request, redirect, session
from application.models import Content
from application.extensions import db
from operator import add, itemgetter
import requests

main = Blueprint('main', __name__)

'''

#TODO
    - Mark many items to add them in group, also to delete them.
    - Unit test.
    
'''

add_list = []
srch_list = []
delete_list = []
user_search = ""
dlist = []

def delete_items ():
    if delete_list:
        for i in delete_list:
            
            #! Returns models object. movie.id -> ID, movie.name -> name, movie.password -> password.
            content = Content.query.filter_by(name=i).first()
            
            if (content):
                db.session.delete (content)
                db.session.commit ()
        
        delete_list.clear()
    
def delete_full_db ():
    Content.query.delete()
    db.session.commit ()

@main.route ('/', methods = ["GET", "POST"])
def index ():
    if request.method == "GET":
        if 'loged' not in session:
            
            delete_full_db ()
            
            return render_template ("index.html", session=False)
        else:
            information = Content.query.all()
            
            return render_template ("index.html", session=True, edit = False, information=information)
    if request.method == "POST":
        if request.form.get ("delete") == 'delete':
            
            titles = request.form.getlist ("active-item")
            
            for i in titles:
                delete_list.append(i)
                
            delete_items ()
            
            return redirect (url_for ('main.index'))
        
        elif request.form.get ("edit") == 'edit':
            title = request.form.get ("name")
            
            return redirect (url_for ('main.edit', content_name = title))

#! This path will perform searches.
@main.route ('/search', methods = ["GET", "POST"])
def search ():
    if 'loged' in session:
        if request.method == "POST":
            user_search = request.form.get ("name").replace (' ', '+')
            
            srch_list.append(user_search)
            
            return redirect (url_for('main.search_results', name = user_search))
                 
        return render_template ("search.html", session = True, table = False)
    
    else:
        return redirect (url_for ('main.index'))


#! This path will add search results to DB
@main.route ('/search/results', methods = ["GET", "POST"])
def search_results():
    d = {}
    
    if 'loged' in session:
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
                    
                    return render_template ("search.html", session = True, table=True, list = res_list)                
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
                
                    new_content = Content (name=d['Title'], year=d['Year'], genre=d['Genre'], rating = d['Rating'], content_type= d['Type'])
                    
                    db.session.add (new_content)
                    db.session.commit ()
            
            add_list.clear ()
    
    return redirect (url_for("main.index"))               

'''
@main.route ('/search', methods = ["GET", "POST"])
def search ():
    if 'loged' in session:
        if request.method == "POST":
            user_search = request.form.get ("name").replace (' ', '+')
            
            return redirect (url_for('main.search_results', name = user_search))
    
        return render_template ("search.html", session = True)
    
    return redirect (url_for ('main.index'))

@main.route ('/search/<name>',  methods = ["GET", "POST"])
def search_results(name):
    if 'loged' in session:
        d = {}
        
        if request.method == "GET":
            URL = 'https://www.omdbapi.com/?s=' + name + '&apikey=678cd26e'
            
            q = requests.get(url=URL)
            r = q.json()
                
            dlist = []
                
            if q.status_code == 200:
                if r['Response'] == 'True':
                    for i in r['Search']:
                        d = {
                            'Title' : i.get ('Title'),
                            'Year' : i.get ('Year'),
                            'Type': i.get ('Type').capitalize(),
                        }
                            
                        dlist.append (d)
                    
                    #! Param 'key' needs the key to sort.            
                    rlist = sorted (dlist, key=itemgetter ('Title'), reverse=False)
                    
                    return render_template ("search.html", session = True, table=True, list = rlist)
            
            return redirect(url_for('main.search'))
        
        elif request.method == "POST":
            title = request.form.get ("title")
            
            if not bool(Content.query.filter_by(name=title).first()):
                
                URL = 'https://www.omdbapi.com/?t=' + title + '&apikey=678cd26e'
                
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
            
                new_content = Content (name=d['Title'], year=d['Year'], genre=d['Genre'], rating = d['Rating'], content_type= d['Type'])
                
                db.session.add (new_content)
                db.session.commit ()
            
    return redirect (url_for("main.index"))
'''

@main.route ('/edit/<content_name>', methods = ["GET", "POST"])
def edit (content_name):
    if 'loged' in session:
        content = Content.query.filter_by(name=content_name).first()
        
        if request.method == "GET":
            return render_template ("index.html", session = True, edit = True, content = content)
        
        elif request.method == "POST":
            if request.form.get ('your-rating'):
                content.user_rating = request.form.get ('your-rating')
            
                db.session.commit ()
    
    return redirect (url_for ('main.index'))
   
@main.route ('/login')
def login ():
    session['loged'] = True
    
    return redirect (url_for ('main.index'))

@main.route ('/logout')
def logout ():
    session.pop ('loged', None)
    
    return redirect (url_for ('main.index'))