from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(
        r'^$',
        TeamListView.as_view(),
        name='list'
    ),
    url(
        r'^members/', include([
            url(
                r'^(?P<pk>[0-9]+)/remove/$',
                TeamMemberRemoveView.as_view(),
                name='teammember_remove',
            ),
            url(
                r'^(?P<pk>[0-9]+)/approve/$',
                TeamMemberApproveView.as_view(),
                name='teammember_approve',
            ),
        ]),
    ),
    url(
        r'^(?P<team_slug>[-_\w+]+)/', include([
            url(
                r'^$',
                TeamDetailView.as_view(),
                name='detail'
            ),
            url(
                r'^join/$',
                TeamJoinView.as_view(),
                name='join'
            ),
            url(
                r'^leave/$',
                TeamLeaveView.as_view(),
                name='leave'
            ),
            url(
                r'^manage/$',
                TeamManageView.as_view(),
                name='manage'
            ),
            url(
                r'^tasks/', include([
                    url(
                        r'^create/$',
                        TaskCreateView.as_view(),
                        name='task_create',
                    ),
                    url(
                        r'^(?P<slug>[-_\w+]+)/', include([
                            url(
                                r'^$',
                                TaskDetailView.as_view(),
                                name='task_detail',
                            ),
                            url(
                                r'^update/$',
                                TaskUpdateView.as_view(),
                                name='task_update',
                            ),
                        ]),
                    ),

                ]),
            ),
        ]),
    ),
]

