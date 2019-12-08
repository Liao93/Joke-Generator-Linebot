from transitions.extensions import GraphMachine

from utils import send_text_message, send_img_message

import random

class TocMachine(GraphMachine):
      
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.maxnum = 6
        self.joke_num = 0
        self.thing = ""
        self.people = ""
        self.benefit = ""
        self.victim = ""
        self.spot = ""
        self.stage = 0

    def is_going_to_state1(self, event):
        text = event.message.text
        return (text == "哈囉"  or text.lower() == "hello") and self.stage == 0

    def on_enter_state1(self, event):
        print("I'm entering state1")
        self.stage = 1

        reply_token = event.reply_token
        send_text_message(reply_token, "是在哈囉" + "\n" + "請選擇笑話編號(1~6), 或「隨機」")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")
		
    def is_going_to_img(self, event):
        text = event.message.text
        return text.lower() == "fsm"

    def on_enter_img(self, event):
        print("I'm entering img state")
        url='https://i.imgur.com/yWmXNlI.png'
        reply_token = event.reply_token
        send_img_message(reply_token, url)
        self.go_back()

    def on_exit_img(self):
        print("Leaving img state")
        
    def is_going_to_random(self, event):
        text = event.message.text
        return text == "隨機" and self.stage == 1
    
    def on_enter_random(self, event):
        print("I'm entering random")
        self.stage = 2
        self.joke_num = random.randint(1, self.maxnum)

        reply_token = event.reply_token
        send_text_message(reply_token, "諷刺的事是？")
        self.go_back()

    def on_exit_random(self):
        print("Leaving random")
    
    def is_going_to_joke1_1(self, event):
        if (self.stage == 1):
            self.joke_num = int(event.message.text)
        return self.joke_num >= 1 and self.joke_num <= self.maxnum and self.stage == 1
    
    def on_enter_joke1_1(self, event):
        print("I'm entering joke1_1")
        self.stage = 2

        reply_token = event.reply_token
        send_text_message(reply_token, "諷刺的事是？")
        self.go_back()

    def on_exit_joke1_1(self):
        print("Leaving joke1_1")
        
    def is_going_to_joke1_t(self, event):
        text = event.message.text
        if (self.stage == 2):
            self.thing = text
        return self.thing != "" and self.stage == 2 and text != "退出"
    
    def on_enter_joke1_t(self, event):
        print("I'm entering joke1_t")
        self.stage = 3

        reply_token = event.reply_token
        send_text_message(reply_token, "提出者是？")
        self.go_back()

    def on_exit_joke1_t(self):
        print("Leaving joke1_t")
        
    def is_going_to_joke1_p(self, event):
        text = event.message.text
        if (self.stage == 3):
            self.people = text
        return self.people != "" and self.stage == 3 and text != "退出"
    
    def on_enter_joke1_p(self, event):
        print("I'm entering joke1_p")
        self.stage = 4

        reply_token = event.reply_token
        send_text_message(reply_token, "提出者聲稱這件事有何幫助？")
        self.go_back()

    def on_exit_joke1_p(self):
        print("Leaving joke1_p")
        
    def is_going_to_joke1_b(self, event):
        text = event.message.text
        if (self.stage == 4):
            self.benefit = text
        return self.benefit != "" and self.stage == 4 and text != "退出"
    
    def on_enter_joke1_b(self, event):
        print("I'm entering joke1_b")
        self.stage = 5

        reply_token = event.reply_token
        send_text_message(reply_token, "此事針對的是？")
        self.go_back()

    def on_exit_joke1_b(self):
        print("Leaving joke1_b")
        
    def is_going_to_joke1_v(self, event):
        text = event.message.text
        if (self.stage == 5):
            self.victim = text
        return self.victim != "" and self.stage == 5 and text != "退出"
    
    def on_enter_joke1_v(self, event):
        print("I'm entering joke1_v")
        self.stage = 6

        reply_token = event.reply_token
        send_text_message(reply_token, "此事的作用範圍？")
        self.go_back()

    def on_exit_joke1_v(self):
        print("Leaving joke1_v")
        
    def is_going_to_joke1_s(self, event):
        text = event.message.text
        if (self.stage == 6):
            self.spot = text
        return self.spot != "" and self.stage == 6 and text != "退出"
    
    def on_enter_joke1_s(self, event):
        print("I'm entering joke1_s")

        reply_token = event.reply_token
        if (self.joke_num == 1):
            send_text_message(reply_token, self.people + "：由於實施了" + self.thing + ", 所有" + self.victim + "的美好前景已經出現在地平線了。\n" + "一個" + self.victim + "問道：什麼是地平線？\n" + "另一個" + self.victim + "回答：就是那條看得到但永遠到不了的線。")
        elif (self.joke_num == 2):
            send_text_message(reply_token, self.people + "在" + self.spot + "隨機問了一個" + self.victim + "：請問你對" + self.thing + "有什麼意見？\n" + "那位" + self.victim + "回答：我有一些意見，但我不同意我的意見。")
        elif (self.joke_num == 3):
            send_text_message(reply_token, "那些有心人士是怎麼抹黑" + self.thing + "的？\n" + "他們把" + self.people + "說的話覆述了一遍。")
        elif (self.joke_num == 4):
            send_text_message(reply_token, "一位" + self.victim + "的鸚鵡飛走了。這是隻會學人說話的鸚鵡，要是遇到" + self.people + "就完了。\n於是那位" + self.victim + "發了條聲明：本人遺失鸚鵡一隻。另外，本人不同意牠對於" + self.thing + "的看法。")
        elif (self.joke_num == 5):
            send_text_message(reply_token, self.thing + "的前途是什麼？\n" + "可能的情況有兩種：現實的可能是火星人會統治地球幫我們打理一切，科幻的可能是我們成功地" + self.benefit + "。")
        else:
            send_text_message(reply_token, "法官在法庭上審問一名" + self.victim + "：你那時在醫院為什麼要拔掉他的呼吸維持器？\n那名" + self.victim + "答道：他說他相信" + self.thing + "能成功" + self.benefit + "。")
        self.go_back()

    def on_exit_joke1_s(self):
        print("Leaving joke1_s")
        self.joke_num = 0
        self.thing = ""
        self.people = ""
        self.benefit = ""
        self.victim = ""
        self.spot = ""
        self.stage = 0
        
    def is_going_to_reset(self, event):
        text = event.message.text
        return text == "退出"
    
    def on_enter_reset(self, event):
        print("I'm entering reset")
        self.joke_num = 0
        self.thing = ""
        self.people = ""
        self.benefit = ""
        self.victim = ""
        self.spot = ""
        self.stage = 0
        
        reply_token = event.reply_token
        send_text_message(reply_token, "重新啟動\n請使用關鍵字再次喚醒機器")
        self.go_back()

    def on_exit_reset(self):
        print("Leaving reset")
        