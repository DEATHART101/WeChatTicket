from codex.baseerror import *
from codex.baseview import APIView
from django.contrib import auth
from wechat import models
from wechat.models import *
from wechat.views import *
from WeChatTicket import settings
import urllib.parse
import uuid

class Upgrade_menu(APIView):
     def get(self):
        new_menu=[]
        act_all=Activity.objects.all()
        cur_t=int(time.time())
        index=1
        for item in act_all:
            act_start=time.mktime(item.book_start.timetuple())
            act_end = time.mktime(item.book_end.timetuple())
            if act_start<cur_t and cur_t<act_end:
                new_item={}
                new_item['id']=item.id
                new_item['name']=item.name
                new_item['menuindex']=index
                new_menu.append(new_item)
                index +=1
        return new_menu
     def post(self):
        self.check_input('id')
        act_id=self.input
        act_all=[]
        for i in act_id:
            act=Activity.objects.get(id=i)
            act_all.append(act)
        CustomWeChatView.update_menu(act_all)
        return None 

class AdminLogin(APIView):

    def get(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("请登录")
        else:
            return 0

    def post(self):

        self.check_input("username", "password")
        user = auth.authenticate(request=self.request, username=self.input["username"], password=self.input["password"])
        if not user:
            raise ValidateError("用户名或密码错误，登录失败")
        else:
            if user.is_active:
                auth.login(self.request, user)
            return 0


class AdminLogout(APIView):

    def post(self):
        try:
            if self.request.user.is_authenticated():
                auth.logout(self.request)
                return 0
            else:
                raise ValidateError("已登出")
        except:
            raise ValidateError("登出失败")


class ActivityList(APIView):

    def get(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("请先登录")

        activity_list = models.Activity.objects.exclude(status__lt=0)
        activity_details = []
        try:
            for activity in activity_list:
                item = {
                    "id": activity.id,
                    "name": activity.name,
                    "description": activity.description,
                    "startTime": activity.start_time.timestamp(),
                    "endTime": activity.end_time.timestamp(),
                    "place": activity.place,
                    "bookStart": activity.book_start.timestamp(),
                    "bookEnd": activity.book_end.timestamp(),
                    "currentTime": timezone.now().timestamp(),
                    "status": activity.status
                }
                activity_details.append(item)
        except:
            raise LogicError("活动列表获取失败")
        return activity_details


class ActivityDelete(APIView):

    def post(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("请先登录")
        self.check_input("id")
        activity_id = self.input["id"]
        try:
            models.Activity.objects.filter(id=activity_id).update(status=models.Activity.STATUS_DELETED)
        except:
            raise LogicError("活动删除失败")
        return 0


class ActivityCreate(APIView):

    def post(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("请先登录")
        self.check_input("name", "key", "place", "description", "picUrl", "startTime",
                         "endTime", "bookStart", "bookEnd", "totalTickets", "status")
        try:
            name = self.input["name"]
            key = self.input["key"]
            place = self.input["place"]
            description = self.input["description"]
            picUrl = self.input["picUrl"]
            startTime = self.input["startTime"]
            endTime = self.input["endTime"]
            bookStart = self.input["bookStart"]
            bookEnd = self.input["bookEnd"]
            totalTickets = self.input["totalTickets"]
            status = self.input["status"]
            remainTickets = totalTickets

            models.Activity.objects.create(
            name=name, key=key, place=place, description=description, pic_url=picUrl,
            start_time=startTime, end_time=endTime, book_start=bookStart, book_end=bookEnd,
            total_tickets=totalTickets, status=status, remain_tickets=remainTickets)

        except:
            raise LogicError("创建活动失败")


class ActivityImageUpload(APIView):

    def post(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("请先登录")
        self.check_input("image")
        try:
            image = self.input["image"][0]
            name = str(uuid.uuid1()) + image.name
            path = 'uimg/' + name
            filename = './static/uimg/' + name
            file = open(filename, 'wb')
            file.write(image.read())
            file.close()
            url = urllib.parse.urljoin(settings.CONFIGS["SITE_DOMAIN"], path)
        except:
            raise ValidateError("上传图片失败")
        return url


class ActivityDetails(APIView):

    def get(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("请先登录")

        self.check_input("id")
        activity_id = self.input["id"]
        try:
            activity = models.Activity.objects.get(id=activity_id)
            usedTickets = len(models.Ticket.objects.filter(status=models.Ticket.STATUS_USED, activity=activity))
            activity_details = {
                "name": activity.name,
                "key": activity.key,
                "description": activity.description,
                "startTime": activity.start_time.timestamp(),
                "endTime": activity.end_time.timestamp(),
                "place": activity.place,
                "bookStart": activity.book_start.timestamp(),
                "bookEnd": activity.book_end.timestamp(),
                "totalTickets": activity.total_tickets,
                "picUrl": activity.pic_url,
                "bookedTickets": activity.total_tickets - activity.remain_tickets,
                "usedTickets": usedTickets,
                "currentTime": timezone.now().timestamp(),
                "status": activity.status
            }
        except:
            raise LogicError("获取详情失败")
        return activity_details

    def post(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("You have not rights to get activity list, please login!")

        self.check_input("id", "name", "place", "description", "picUrl", "startTime",
                         "endTime", "bookStart", "bookEnd", "totalTickets", "status")
        activity_id = self.input["id"]
        status = self.input["status"]
        try:
            activity = models.Activity.objects.get(id=activity_id)
            if activity.status != models.Activity.STATUS_PUBLISHED:
                activity.name = self.input["name"]
                activity.place = self.input["place"]
                activity.book_start = self.input["bookStart"]
                activity.status = status
            elif status == 1:
                activity.status = status

            if activity.end_time > timezone.now():
                activity.start_time = self.input["startTime"]
                activity.end_time = self.input["endTime"]
                activity.save()
                activity = models.Activity.objects.get(id=activity_id)

            if activity.start_time > timezone.now():
                activity.book_end = self.input["bookEnd"]

            if activity.book_start > timezone.now():
                activity.total_tickets = self.input["totalTickets"]

            activity.description = self.input["description"]
            activity.pic_url = self.input["picUrl"]
            activity.save()
        except:
            raise LogicError("详情修改失败")
        return 0


class ActivityCheckIn(APIView):

    def post(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("Please login!")

        self.check_input("actId")
        if "ticket" in self.input:
            self.check_input("ticket")
        elif "studentId" in self.input:
            self.check_input("studentId")

        studentId = self.input["studentId"]
        unique_id = self.input["ticket"]

        if studentId == None and unique_id == None:
            raise ValidateError("info loss")

        try:
            if studentId != None:
                ticket = Ticket.objects.get(student_id=self.input["studentId"], activity_id=self.input['actId'])
            else:
                ticket = Ticket.objects.get(unique_id=self.input["ticket"], activity_id=self.input['actId'])
        except:
            raise ValidateError("检票失败")
        if ticket.status == Ticket.STATUS_USED:
            raise ValidateError("该票已检过")
        if ticket.status == Ticket.STATUS_CANCELLED:
            raise ValidateError("该票已被取消")
        ticket.status = Ticket.STATUS_USED
        ticket.save()
        ticket_info = {
            "ticket": ticket.unique_id,
            "studentId": ticket.student_id
        }
        return ticket_info