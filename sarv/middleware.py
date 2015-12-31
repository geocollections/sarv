# -*- coding: utf-8 -*-
import json
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response

class IDAuthSessionMiddleware(object):
    def process_request(self, request):        
        if request.path in ("/login","/loginpsw","/logout","/b"):
            return None
        loginurl = "https://%s/login" % request.get_host()
        msg = 'Sisselogimiseks minge <a href="%s">siia</a>' % loginurl
        try:
            user_id = request.session['sarvuser_id']
        except KeyError:
            if request.is_ajax():
                response = {"type": "event", "name": "sessionexpiry", "url": "%s" % loginurl}
                return HttpResponse(json.dumps(response), 
                    mimetype = "application/javascript")
            else:
                return render_to_response("login.html", {
                    'MEDIA_URL': settings.MEDIA_URL, 
                    'loginurl': loginurl,
                    'login_as': True if request.path.replace('/','') == 'login_as' else False,
                    'PUBLIC_STATIC_URL': settings.PUBLIC_STATIC_URL
                })

        from sarv.utils import get_model
        SarvUser = get_model("User")
        try:
            sarvuser = SarvUser.objects.get(pk=user_id)
        except:
            return HttpResponse(msg)
        
        request.__class__.user = AnonymousUser()
        request.__class__.sarvuser = sarvuser
        
        return None
     
from django.db import connection
class ProfilingMiddleware(object):
    def process_response(self, request, response):
        for q in sorted(connection.queries, key=lambda q: q['time']):
            print (q['time'])
            print (q)
        print (sum([float(q['time']) for q in connection.queries]), len(connection.queries))
        return response
        
import threading
_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'sarvuser', None)

class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        _thread_locals.sarvuser = getattr(request, 'sarvuser', None)
        

# TODO: What's the difference between using threading directly and using currentThread?     
#from django.utils.thread_support import currentThread
_database = {}

def get_default_database():
    return 'users'

def set_database(db):
    """
    Sets the currently "active" database.
    """
    _database[_thread_locals] = db

def get_database():
    """
    Gets the currently "active" database.
    """
    return _database.get(_thread_locals, get_default_database())

class DatabaseMiddleware:
    """
    Gets the currently selected database from the 
    user session and stores it as a thread variable. 
    """
    def process_request(self, request):
        database = request.session.get('database', None)
        if database:
            set_database(database)
        return None

def get_user_status(user, sarvuser):
    """
    Checks user privileges in User against sarvuser 
    """
    if user is None: #Get user privileges
        return sarvuser.priv
    elif user.is_staff == 0 \
    and sarvuser.priv == 4: #When user is created, it's privileges are based on sarvuser privileges
        user.is_staff=1 
        user.is_superuser=1
        user.save()
        
class LocalHash(object):    
    """
    Temporary solution for bridging Django with PHP.
    User session is transported between two environments through a url hash '_h'
    """
    hash = ''
            
    def set_hash(self, username):
        from sarv.models import UserSessionHash
        user_hash, created = UserSessionHash.objects.using('sarv').get_or_create(username=username)
                
        hash_exists = True
        while hash_exists is True:
            rnd_hash = self.generate_hash()
            hash_exists = UserSessionHash.objects.filter(hash=rnd_hash).using('sarv').exists()
            
        user_hash.hash = rnd_hash
        user_hash.save(using='sarv')
        
        return rnd_hash
        
    def test_hash(self, request):
        self.hash = request.GET.get('_h', False)
        from sarv.models import UserSessionHash
        user_hash = UserSessionHash.objects.using('sarv').get(hash=self.hash)
        if user_hash:
            return user_hash
        else:
            return False
        
    def generate_hash(self):
        import random, string
        rnd_hash = ''
        for i in range(15):
            rnd_hash += random.choice(string.lowercase + string.uppercase + string.digits)   
        return rnd_hash

