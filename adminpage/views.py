# Create your views here.
from codex.baseerror import *
from codex.baseview import APIView
from wechat import models
from django.contrib import auth


class Login(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")

    def post(self):
        self.check_input("username", "password")
        username = self.input["username"]
        password = self.input["password"]
        login_user = auth.authenticate(request=self.request, username=username, password=password)
        if not login_user:
            raise ValidateError("Fail to login, either username or password is wrong!")
        auth.login(self.request, login_user)


class Logout(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Fail to logout,you must login first!")
        auth.logout(self.request)


class ActivityListShow(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("Fail to get information, you must login first!")

        activity_list = models.Activity.objects.exclude(status__lt=0)

        activity_details = []
        for activity in activity_list:
            activity_item = {
                "id": activity.id,
                "name": activity.name,
                "description": activity.description,
                "startTime": activity.start_time.timestamp(),
                "endTime": activity.end_time.timestamp(),
                "place": activity.place,
                "bookStart": activity.book_start.timestamp(),
                "bookEnd": activity.book_end.timestamp(),
                "status": activity.status
            }

            activity_details.append(activity_item)
        return activity_details


class ActivityAdd(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("You must login first")
        self.check_input("name", "key", "description", "picUrl", "startTime",
                         "endTime", "bookStart", "bookEnd", "totalTickets", "status")
        name = self.input["name"]
        key = self.input["key"]
        place = self.input["place"]
        description = self.input["description"]
        picurl = self.input["picUrl"]
        starttime = self.input["startTime"]
        endtime = self.input["endTime"]
        bookstart = self.input["bookStart"]
        bookend = self.input["bookEnd"]
        totaltickets = self.input["totalTickets"]
        status = self.input["status"]
        remaintickets = totaltickets

        newActivity = models.Activity.objects.create(name=name, key=key, place=place, description=description,
            pic_url=picurl,start_time=starttime, end_time=endtime, book_start=bookstart, book_end=bookend,
            total_tickets=totaltickets, status=status, remain_tickets=remaintickets)
        if not newActivity:
            raise InputError("Fail to add an activity")


class ActivityDelete(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("You must login first")
        self.check_input("id")
        activity_id = self.input["id"]
        if not models.Activity.objects.filter(id=activity_id).update(status=models.Activity.STATUS_DELETED):
            raise LogicError("Fail to delete, activity not found!")


