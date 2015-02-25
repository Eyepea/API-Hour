from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'benchmarks.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^index$', 'agents.views.index', name='index'),
    url(r'^agents$', 'agents.views.agents', name='agents'),
    url(r'^agents_with_orm$', 'agents.views.agents_with_orm', name='agents_with_orm'),
    # url(r'^admin/', include(admin.site.urls)),
)
