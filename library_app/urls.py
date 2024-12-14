from django.urls import re_path as url
from django.conf.urls import include 
from django.conf import settings


from .views.login import LoginViewSet
from .views.logout import LogoutView
from .views.users import ImpersonateView

""" User login/ add/ logout profile urls"""
urlpatterns = [
    url(r'^login/$', LoginViewSet.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
]



""" User impersonate"""
urlpatterns += [
    url(r'^users/(?P<id>.+)/$', ImpersonateView.as_view({'get': 'retrieve',})),
    url(r'^users/$', ImpersonateView.as_view({'post':'create',})),
    
]

from .views.books import BooksView
urlpatterns += [
    url(r'^books/(?P<id>.+)/$', BooksView.as_view({'get': 'retrieve', 'put':'update'})),
    url(r'^books/$', BooksView.as_view({'get':'list','post':'create'}))
]
        
from .views.borrow_requests import BorrowRequestsView
urlpatterns += [
    url(r'^borrow-request/(?P<id>.+)/$', BorrowRequestsView.as_view({'get': 'retrieve', 'put':'update'})),
    url(r'^borrow-request/$', BorrowRequestsView.as_view({'get':'list','post':'create'})),
    url(r'^get-borrow-history/$', BorrowRequestsView.as_view({'get':'get_borrow_history',})),

]

# from .views.student import StudentView

# ''' Student '''
# urlpatterns += [
#     re_path(r'^student/$', StudentView.as_view({'get': 'list', 'post': 'create', 'delete': 'bulk_delete'})),
#     re_path(r'^student/(?P<id>.+)/$', StudentView.as_view({'get': 'retrieve', 'delete': 'delete', 'put': 'partial_update'})),
# ]
