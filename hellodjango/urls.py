from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

from django.contrib import admin

from users_.views import welcome, profile, register, new_test, delete_test, admin_test, ajax_new_question, ajax_delete_question, admin_question, ajax_new_answer, ajax_delete_answer, user_test, ajax_send_result

from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hellodjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', welcome),
    url(r'^register/', register),
    url(r'^profile/ajax_new_test', new_test),
    url(r'^profile/ajax_delete_test', delete_test),
    url(r'^profile/admin/(?P<test_id>\d{1,50})/$', admin_test),
    url(r'^profile/admin/(?P<test_id>\d{1,50})/ajax_new_question', ajax_new_question),
    url(r'^profile/admin/(?P<test_id>\d{1,50})/ajax_delete_question', ajax_delete_question),
    url(r'^profile/admin/(?P<test_id>\d{1,50})/(?P<question_id>\d{1,50})/$', admin_question),
    url(r'^profile/admin/(?P<test_id>\d{1,50})/(?P<question_id>\d{1,50})/ajax_new_answer', ajax_new_answer),
    url(r'^profile/admin/(?P<test_id>\d{1,50})/(?P<question_id>\d{1,50})/ajax_delete_answer', ajax_delete_answer),

    url(r'^profile/user/(?P<test_id>\d{1,50})/$', user_test),
    url(r'^profile/user/(?P<test_id>\d{1,50})/ajax_send_result', ajax_send_result),
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'login/$', login, kwargs={'template_name': 'login.html'}, name='login'),
    url(r'logout/$', logout, kwargs={'next_page': '/login'}, name='logout'),
    url(r'^profile/$', profile, name='profile'),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)