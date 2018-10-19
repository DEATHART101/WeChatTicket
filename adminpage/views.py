from django.shortcuts import render
import time
from codex.baseview import APIView
from wechat.models import Activity
from wechat.views import CustomWeChatView
# Create your views here.
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