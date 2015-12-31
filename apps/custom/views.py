from django.shortcuts import render_to_response
from django.template import RequestContext

def get_model (modelname, db_id):
    from sarv.utils import get_model
    m = get_model(modelname)
    if hasattr(m, "session_db"):
        m.session_db=db_id
    return m

def testpage(request):
    out={"test": "qwerty",
        "sarvuser": request.sarvuser
    }
    return render_to_response("testpage.html",out, 
        context_instance = RequestContext(request))

def doi(request):
    out={'test':'qwerty','sarvuser':request.sarvuser}
    return render_to_response('testpage.html',out, 
        context_instance = RequestContext(request))


def relocate_location(request):
    get=request.GET.dict()
    out={'get':get}
    db_id=request.session['database_id']
    m=get_model('Location', db_id)
        
    #update
    if 'location_old' in get \
    and 'location_new' in get:
        ol=get['location_old']
        nl=get['location_new']
        #mn=m.objects.filter(location=nl)
        ol_d={'storage':int(ol)} \
                if ol.isdigit() \
                else {'location':ol}
        nl_d={'storage':int(nl)} \
                if nl.isdigit() \
                else {'location':nl}
        def upd(name):
            try:
                mo=get_model(name, db_id)
                dbn= mo._meta.db_table \
                    if not hasattr(mo._meta, 'verbose_name') \
                    else mo._meta.verbose_name
                mv= mo\
                    .objects \
                    .filter(**ol_d)#location=ol)
                if 'confirmed' in get:
                    nc= mo \
                        .objects \
                        .filter(**ol_d).count() #location=ol).count()
                    mv.update(**nl_d) #{'location':nl})
                    if not 'moved' in out:
                        out.update({'moved':[]})
                    out['moved'].append([
                        dbn, nc
                        ])
                else:
                    mvn=get_model(name,db_id) \
                        .objects \
                        .filter(**nl_d) #location=nl)
                    if not 'move' in out:
                        out.update({'move':[]})
                    out['move'].append([
                        dbn,
                        mv.count(), 
                        mvn.count()])
            except Exception as e:
                print(name+': '+e)
        upd('Specimen')
        upd('Sample')
        upd('Analysis')
        upd('Preparation')
        #upd('SamplePaleontology') # todo: check if model is missing
    qs=m.objects.all().values_list('location',flat=True) 
    out.update({
                'locations': list([j for j in qs if j])
    })
    return render_to_response(
            'relocate_location.html', out,
            context_instance=RequestContext(request))

