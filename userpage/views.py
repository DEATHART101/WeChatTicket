from codex.baseerror import *
from codex.baseview import APIView
import requests

from wechat import models
from wechat.models import *


post_url = 'https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp'

header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'learn.tsinghua.edu.cn',
    'Origin': 'http://learn.tsinghua.edu.cn',
    'Referer': 'http://learn.tsinghua.edu.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

class UserBind(APIView):

    def validate_user(self):
        """
        input: self.input['student_id'] and self.input['password']
        raise: ValidateError when validating failed
        """
        learn_session = requests.Session()

        post_data = 'userid=%s&userpass=%s&submit1=%s' % (
            self.input['student_id'],
            self.input['password'],
            r'%E7%99%BB%E5%BD%95'
        )

        reps = learn_session.post(post_url, post_data, headers = header)

        if (len(reps._content > 100)):
            raise ValidateError("StuentID or Password incorrect")

    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()

class ActivityDetail(APIView):
    def get(self):
        self.check_input('openid')
        activity = Activity.get_by_activity_id(self.input['id'])
        
        if activity.status == 1:
            item = {
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
                "remainTickets": activity.remain_tickets,
                "currentTime": timezone.now().timestamp(),
            }
            return item
        else:
            return status

class TicketDetail(APIView):
    def get(self):
        self.check_input('openid')
        ticket = Ticket.get_by_unique_id(self.input['ticket'])
        activity = ticket.activity
        item = {
            "name": activity.name,
            "place": activity.place,
            "activityKey": activity.key,
            "uniqueId": ticket.unique_id,
            "startTime": activity.start_time.timestamp(),
            "endTime": activity.end_time.timestamp(),
            "currentTime": timezone.now().timestamp(),
            "status": ticket.status,
        } 
        return ticket
