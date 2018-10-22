# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from WeChatTicket import settings
from wechat.models import Activity

__author__ = "Epsirom"


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')


class HelpOrSubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('帮助', 'help') or self.is_event('scan', 'subscribe') or \
               self.is_event_click(self.view.event_keys['help'])

    def handle(self):
        return self.reply_single_news({
            'Title': self.get_message('help_title'),
            'Description': self.get_message('help_description'),
            'Url': self.url_help(),
        })


class UnbindOrUnsubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('解绑') or self.is_event('unsubscribe')

    def handle(self):
        self.user.student_id = ''
        self.user.save()
        return self.reply_text(self.get_message('unbind_account'))


class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_text('绑定') or self.is_event_click(self.view.event_keys['account_bind'])

    def handle(self):
        return self.reply_text(self.get_message('bind_account'))


class BookEmptyHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['book_empty'])

    def handle(self):
        return self.reply_text(self.get_message('book_empty'))


class BookWhatHandle(WeChatHandler):

    def check(self):
        return self.is_text('抢什么') or self.is_event_click(self.view.event_keys['book_what'])

    def handle(self):
        activities = Activity.objects.filter(status=Activity.STATUS_PUBLISHED)
        acticles = []
        if not activities:
            return self.reply_text("目前不能进行抢票")
        if activities.exits():
            for activity in activities:
                acticles.append({'Title': activity.name,
                'Description': activity.description,
                'Time': "抢票时间：" + activity.start_time + "-" + activity.end_time,
                'url': settings.url("/u/activity/", {"id": activity.id}),
                'PicUrl': activity.pic_url})
            return self.reply_news(acticles)