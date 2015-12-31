import json
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from sarv.settings import PROJECT_ADMINS
from django.contrib.auth.models import User
from sarv.middleware import get_database

from sarv.utils import get_model
Database, SarvIssue, Session, SarvUser = get_model(["Database", "SarvIssue", "SarvSession", "User"])

def index(request):
    user = request.sarvuser
    if user is None: 
        return HttpResponse("")
    
    database = user.db
    request.session["database"] = user.db
    
    user_o = SarvUser.objects.get(username=user)

    # Get all messages to user    
    msg_n=SarvIssue.objects \
            .filter(reported_to=user_o,
                    resolved=False) \
            .count()

    return render_to_response("index.html", {
        "sarvuser": request.sarvuser,
        "sarvuser_id": request.session["sarvuser_id"],
        "database": database,
        "acl": request.session["acl"] if "acl" in request.session else None,
        "users": SarvUser.objects.all().order_by("username").values_list("username", flat=True),
        "msg_n": msg_n
    }, 
    context_instance = RequestContext(request))

"""
Login/logout
"""
def login(request):
    if not request.is_secure():
        return HttpResponse("Seda lehte saab näha ainult üle https protokolli.")
    name = request.__class__.__name__
    if name == "WSGIRequest":
        env = request.environ
    elif name == "ModPythonRequest":
        env = request._req.subprocess_env
    else:
        return HttpResponse("Antud serveri konfiguratsiooniga ei õnnestu seda lehte kasutada.")
    
    verified = env.get("SSL_CLIENT_VERIFY", None)
    if verified is None \
    or verified != "SUCCESS":
        return HttpResponse("Vale PIN") # seda ei tohiks juhtuda, kui on SSLClientVerify require
    
    personal_code = env.get("SSL_CLIENT_S_DN_CN", "").split(",")[2]
    sarvuser = None
    try:
        sarvuser = SarvUser.objects.get(isikukood = personal_code)
        if "username" in request.GET.dict() \
        and sarvuser.pk in PROJECT_ADMINS:
            try:
                sarvuser = SarvUser.objects \
                    .get(username = request.GET.dict()["username"])
            except SarvUser.DoesNotExist:
                return HttpResponse("Kasutajat ei eksisteeri")
    except SarvUser.DoesNotExist:
        return HttpResponse("Ei ole lubatud seda lehte vaadata %s" % get_database())

    request.session["sarvuser_id"] = sarvuser.id
    request.session["database"] = sarvuser.db
    request.session["sarvuser"] = sarvuser.username
    request.session["database_id"] = sarvuser.database_id
    request.session["agent_id"] = sarvuser.id
   
    try:
        Session.objects.filter(user=sarvuser.username,active=1) \
            .update(active=0,session_end=datetime.now())
    except Exception as e:
        print(e)
    try:
        from django.db.models import Q
        Session.objects.filter((Q(user=sarvuser.username) & Q(active=1)))
        Session.objects.create(
                user=sarvuser.username,
                active=1,
                session_start=datetime.now(),
                database_id=sarvuser.database_id,
                )
    except Exception as e:
        print (e)

    """
    Set user rights per page session variables
    """
    from apps.acl.views import Acl as vAcl
    urights = vAcl().get_all_user_rights(request)

    if len(urights) > 0:
        request.session["acl"] = urights

    return HttpResponseRedirect("/")

"""
Alternative login with password/username which additionally activates sarvuser session variables
"""
def login_with_password (request):        
    username = request.POST['username']
    password = request.POST['password']
    redirect_path = request.META['HTTP_REFERER']

    #Test validity of given login information
    from django.contrib.auth import authenticate, login 
    user = authenticate(username = username, password = password)
    
    if user is not None and user.is_active:
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)
    else:
        return HttpResponseRedirect(redirect_path+'?e=login')
            
    request.__class__.user = user

    #Set sarvuser session variables
    sarvuser = None
    try:
        sarvuser = SarvUser.objects.using('sarv').get(username=username)
    except SarvUser.DoesNotExist:
        return HttpResponse("Ei ole lubatud seda lehte vaadata %s" % get_database())    
    request.session['sarvuser_id'] = sarvuser.id
    request.session['database'] = sarvuser.db

    #Set user rights per page session variables
    from apps.acl.views import Acl as vAcl
    request.session['acl'] = vAcl().get_all_user_rights(request)

    return HttpResponseRedirect(redirect_path.replace("?e=login", ""))

def mark_user_logged_out(username):
    try:
        Session.objects \
            .filter(user = username, active = 1) \
            .update(active = 0, session_end = datetime.now())
    except Exception as e:
        print (e)

def logout(request):
    if hasattr(request, "session") \
    and "sarvuser" in request.session:
        mark_user_logged_out(request.session["sarvuser"])
    try: del request.session["sarvuser_id"]
    except KeyError: pass
    try: del request.session["database"]
    except KeyError: pass
    try: del request.session["acl"]
    except KeyError: pass
    
    from django.contrib.auth import logout
    logout(request)

    return render_to_response("logout.html", {
        "MEDIA_URL": settings.MEDIA_URL,
        "PUBLIC_STATIC_URL": settings.PUBLIC_STATIC_URL,
    })
