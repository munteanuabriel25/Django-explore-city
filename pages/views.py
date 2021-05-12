from django.shortcuts import render
from django.http import HttpResponse
from listing.models import ListingCategory
from datetime import datetime
# Create your views here.

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val :
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S' )

    if (datetime.now()-last_visit_time).seconds > 0 :
        visits+=1
        request.session['last_visit']= str(datetime.now())
    else:
        visits=1
        request.session['last_visit']= last_visit_cookie
    request.session['visits'] = visits

   


def home_view(request):
    print(request.session.values())
    categories= ListingCategory.objects.all()
    visitor_cookie_handler(request)
    context ={}
    context['visits'] = request.session['visits']
    context['categories']=categories
    return render(request, 'pages/home.html',context)