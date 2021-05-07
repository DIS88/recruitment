from dingtalkchatbot.chatbot import DingtalkChatbot

from django.conf import settings

def send(message, at_mobile=[]):
    
    webhook = settings.DINGTALK_WEB_HOOK
    
    xiaoding = DingtalkChatbot(webhook)
    
    xiaoding.send_text(msg=('面试通知: %s' % message), at_mobiles = at_mobile)