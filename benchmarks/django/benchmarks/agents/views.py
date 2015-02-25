# from django.http import JsonResponse
from django.db import connections
from .utils import JsonResponse

from .models import AgentFeatures

def index(request):
    return JsonResponse({'hello': 'world'})

def agents(request):
    cur = connections['dict_cursor'].cursor()
    cur.execute("SELECT af.number AS number, als.extension AS extension, als.context AS context, als.state_interface AS state_interface, 'offline' AS status, '-1' AS extension_status, '0' AS paused FROM public.agentfeatures af LEFT JOIN public.agent_login_status als ON (af.id = als.agent_id)")
    return JsonResponse(cur.fetchall(), safe=False)

def agents_with_orm(request):
    return JsonResponse(list(AgentFeatures.objects.all().values()), safe=False)