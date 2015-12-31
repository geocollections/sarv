import json
from django.http import HttpResponse
from sarv.utils import get_model
SarvIssue, SarvUser = get_model(["SarvIssue", "User"])

def read(request):
    msg_l = SarvIssue.objects \
        .filter(
             reported_to = request.sarvuser, 
             resolved = False
        ) \
        .order_by("-date_added") \
        .values_list(
             "title",
             "pk",
             "date_added",
             "reported_by__username",
             "description",
             "response",
             "issue_type__issue_type"
        )
    o_l=[]
    for i in msg_l:
        u_l=[]
        for j in i:
            u_l.append(str(j))
        o_l.append(u_l) 
    return HttpResponse(json.dumps(o_l),
        content_type = "application/json")

def add(request):
    s = request.GET.dict()
    to_db = {
        "resolved": False, 
        "reported_by": request.sarvuser
    }
    out = {}
    try:
        for k,v in s.items():
            to_db.update({
                k: v \
                    if not k == "reported_to" \
                    else SarvUser.objects \
                        .filter(username = v)[0]           
            })
        ni = SarvIssue(**to_db)
        ni.save()
    except Exception as e:
        out.update({"error": e})
    return HttpResponse(json.dumps(out), 
        content_type = "application/json")

def mark_resolved(request):
    s = request.GET.dict()
    if "idm" in s:
        qs = SarvIssue.objects \
            .filter(pk = s["idm"])
        qs.update(**{"resolved":True})

    return HttpResponse(json.dumps({}),
        content_type = "application/json")
