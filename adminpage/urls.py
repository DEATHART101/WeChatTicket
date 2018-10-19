# -*- coding: utf-8 -*-
#

from django.conf.urls import url

from adminpage.views import *

__author__ = "Epsirom"


urlpatterns = [
    url(r'^activity/menu/?$', Upgrade_menu.as_view()),
]
