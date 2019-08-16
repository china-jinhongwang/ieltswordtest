# _*_coding : UTF-8_*_
# 开发团队：NONE
# 开发人员：41570
# 开发时间：2019/8/15 20:36
# 文件名称：IeltsWordTest.PY
# 开发工具：PyCharm

import wx
import random
import numpy as np
import os
import time


class IeltsTest(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="ielts test App", size=(500, 450), pos=(100, 100))
        self.Center()
        self.p = 5
        self.c = 0
        self.count = 0
        self.err_dict = {}
        self.ielts_dict = self.get_ielts_dict()
        self.panel = wx.Panel(self)
        self.bt_new_window = wx.Button(self.panel, label="查看并保存错误单词表", id=14)
        self.Bind(wx.EVT_BUTTON, self.OnNewWindow, id=14)
        self.bt_submit = wx.Button(self.panel, label="提交", id=13)
        self.Bind(wx.EVT_BUTTON, self.judge, id=13)
        self.bt_score = wx.Button(self.panel, label="查看成绩", id=12)
        self.Bind(wx.EVT_BUTTON, self.get_score, id=12)
        self.stxt1 = wx.StaticText(self.panel, label='请输入您的姓名：', style=wx.ALIGN_RIGHT)
        self.stxt2 = wx.StaticText(self.panel, label='请输入样本数量(建议值200)：', style=wx.ALIGN_RIGHT)
        self.bt_next = wx.Button(self.panel, label="下一个", id=10)
        self.Bind(wx.EVT_BUTTON, self.go_test, id=10)
        self.bt_start = wx.Button(parent=self.panel, label="开始测试", id=11)
        self.Bind(wx.EVT_BUTTON, self.start_test, id=11)
        self.getfilename = wx.TextCtrl(parent=self.panel, id=100, style=wx.TE_LEFT)
        self.getnumber = wx.TextCtrl(parent=self.panel, id=100, style=wx.TE_LEFT)
        self.word = wx.StaticText(self.panel, label="单词", style=wx.ALIGN_LEFT)
        font_title= wx.Font(14, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD)
        self.word.SetFont(font_title)
        self.rbA = wx.RadioButton(self.panel, 1, label='Value A', style=wx.RB_GROUP)
        self.rbB = wx.RadioButton(self.panel, 2, label='Value B')
        self.rbC = wx.RadioButton(self.panel, 3, label='Value C')
        self.rbD = wx.RadioButton(self.panel, 4, label='Value D')
        font_chioce = wx.Font(14, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.rbA.SetFont(font_chioce)
        self.rbB.SetFont(font_chioce)
        self.rbC.SetFont(font_chioce)
        self.rbD.SetFont(font_chioce)
        self.rbA.SetValue(False)
        self.rbB.SetValue(False)
        self.rbC.SetValue(False)
        self.rbD.SetValue(False)
        self.result = wx.StaticText(self.panel, label="选择后点击提交按钮", style=wx.ALIGN_LEFT)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioGroup)
        hbox3 = wx.BoxSizer()
        hbox3.Add(self.bt_submit, -1, flag=wx.ALL | wx.EXPAND, border=5)
        hbox3.Add(self.bt_next, -1, flag=wx.ALL | wx.EXPAND, border=5)
        hbox3.Add(self.bt_score, -1, flag=wx.ALL | wx.EXPAND, border=5)
        hbox3.Add(self.bt_new_window, -1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox_rb = wx.BoxSizer(wx.VERTICAL)
        vbox_rb.Add(self.word, -1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox_rb.Add(self.rbA, -1, flag=wx.ALL | wx.EXPAND, border=0)
        vbox_rb.Add(self.rbB, -1, flag=wx.ALL | wx.EXPAND, border=0)
        vbox_rb.Add(self.rbC, -1, flag=wx.ALL | wx.EXPAND, border=0)
        vbox_rb.Add(self.rbD, -1, flag=wx.ALL | wx.EXPAND, border=0)
        vbox_rb.Add(self.result, -1, flag=wx.ALL | wx.EXPAND, border=5)
        vbox_rb.Add(hbox3, -1, flag=wx.ALL | wx.EXPAND, border=5)
        hbox1 = wx.BoxSizer()
        hbox1.Add(self.stxt1, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        hbox1.Add(self.getfilename, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        hbox2 = wx.BoxSizer()
        hbox2.Add(self.stxt2, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        hbox2.Add(self.getnumber, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        vbox.Add(hbox1, proportion=1, flag=wx.ALL | wx.EXPAND, border=0)
        vbox.Add(hbox2, proportion=1, flag=wx.ALL | wx.EXPAND, border=0)
        vbox.Add(self.bt_start, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        vbox.Add(vbox_rb, proportion=6, flag=wx.ALL | wx.EXPAND, border=10)
        self.panel.SetSizer(vbox)

    def OnNewWindow(self, event):
        err_words = str(self.err_dict)
        wx.MessageBox(err_words, "Message", wx.OK | wx.ICON_INFORMATION)
        dict_tmp = {}
        filename = "{}'s_error_dict.txt".format(self.name)
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("")

        with open(filename, 'r', encoding="utf-8") as f:
            for line in f:
                ls = line.split(">")
                dict_tmp[ls[0]] = ls[1].strip("\n")
            print("dict_tmp", dict_tmp)
            dict_tmp = dict(dict_tmp, **self.err_dict)

        with open(filename, 'w') as f:
            f.write("")

        with open(filename, "a", encoding="utf-8") as f:
            for item in dict_tmp:
                f.writelines(item + ">" + dict_tmp[item] + "\n")

    def OnRadioGroup(self, event):
        self.p = event.GetId()

    def get_score(self, event):
        n = eval(self.getnumber.GetValue())
        self.end_time = time.time()
        minutes = int((self.end_time - self.start_time)//60)
        seconds = int((self.end_time - self.start_time)%60)
        font = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.LIGHT)
        self.result.SetFont(font)
        self.result.SetForegroundColour((255, 0, 0))
        self.result.SetLabelText("本次测验用时{}分{}秒，正确率为：{}/{}={:.2f}%".format(minutes,\
                                        seconds, self.count, n, 100 * self.count / n))

    def judge(self, event):
        if self.p == 0:
            self.result.SetLabelText("请重新选择")
        else:
            if self.dict_item[self.p].split("$")[1] != self.ielts_dict[self.sample_list[self.c]].split("$")[1]:
                self.err_dict[self.sample_list[self.c]] = self.ielts_dict[self.sample_list[self.c]]
                font = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.LIGHT)
                self.result.SetFont(font)
                self.result.SetForegroundColour((255, 0, 0))
                self.result.SetLabelText("正确答案为：{}、{}".format(self.sample_list[self.c], \
                                                 self.ielts_dict[self.sample_list[self.c]].split("$")[1]))
            else:
                font = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.LIGHT)
                self.result.SetFont(font)
                self.result.SetForegroundColour((0, 0, 255))
                self.result.SetLabelText("恭喜你，答对了！！！")
                self.count += 1
            self.c += 1
            self.p = 0

    def get_ielts_dict(self, filename="ielts_dict_rv.txt"):
        ielts_dict = {}
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                ls = line.split(">")
                ielts_dict[ls[0]] = ls[1].strip("\n")
        return ielts_dict

    def start_test(self, event):
        self.start_time = time.time()
        self.name = self.getfilename.GetValue()
        n = eval(self.getnumber.GetValue())
        font = wx.Font(16, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        self.result.SetFont(font)
        self.result.SetForegroundColour((0, 0, 0))
        font = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.LIGHT)
        self.result.SetFont(font)
        self.result.SetForegroundColour((0, 0, 0))
        self.result.SetLabelText("选择后点击提交按钮")
        self.sample_list = random.sample(list(self.ielts_dict), n)
        self.dict_item = {}
        try:
            pro = self.ielts_dict[self.sample_list[self.c]].split("$")[0]
            self.word.SetLabelText("第{}/{}个单词>> {} {}".format(self.c+1, n, self.sample_list[self.c], pro))
            a_list = np.arange(1, 5)
            np.random.shuffle(a_list)
            ch_key_list = random.sample(self.ielts_dict.keys(), 4)
            if not (self.sample_list[self.c] in ch_key_list):
                ch_key_list[0] = self.sample_list[self.c]
            for i in range(4):
                value = self.ielts_dict[ch_key_list[i]]
                self.dict_item[a_list[i]] = value
            cnt_tmp = 0
            for item in sorted(self.dict_item):
                cnt_tmp += 1
                if cnt_tmp == 1:
                    self.rbA.SetLabelText("  {}、{}".format(item, self.dict_item[item].split('$')[1]))
                elif cnt_tmp == 2:
                    self.rbB.SetLabelText("  {}、{}".format(item, self.dict_item[item].split('$')[1]))
                elif cnt_tmp == 3:
                    self.rbC.SetLabelText("  {}、{}".format(item, self.dict_item[item].split('$')[1]))
                elif cnt_tmp == 4:
                    self.rbD.SetLabelText("  {}、{}".format(item, self.dict_item[item].split('$')[1]))
        except:
            pass

    def go_test(self, event):
        if self.p != 0:
            pass
        else:
            self.rbA.SetValue(False)
            self.rbB.SetValue(False)
            self.rbC.SetValue(False)
            self.rbD.SetValue(False)
            self.dict_item = {}
            font = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.LIGHT)
            self.result.SetFont(font)
            self.result.SetForegroundColour((0, 0, 0))
            self.result.SetLabelText("选择后点击提交按钮")
            try:
                n = eval(self.getnumber.GetValue())
                pro = self.ielts_dict[self.sample_list[self.c]].split("$")[0]
                self.word.SetLabelText("第{}/{}个单词>> {} {}".format(self.c+1, n, self.sample_list[self.c], pro))
                a_list = np.arange(1, 5)
                np.random.shuffle(a_list)
                ch_key_list = random.sample(self.ielts_dict.keys(), 4)
                if not (self.sample_list[self.c] in ch_key_list):
                    ch_key_list[0] = self.sample_list[self.c]
                for i in range(4):
                    value = self.ielts_dict[ch_key_list[i]]
                    self.dict_item[a_list[i]] = value
                cnt_tmp = 0
                for item in sorted(self.dict_item):
                    cnt_tmp += 1
                    if cnt_tmp == 1:
                        self.rbA.SetLabelText("  {}、{}".format(item, self.dict_item[item].split('$')[1]))
                    elif cnt_tmp == 2:
                        self.rbB.SetLabelText("  {}、{}".format(item, self.dict_item[item].split('$')[1]))
                    elif cnt_tmp == 3:
                        self.rbC.SetLabelText("  {}、{}".format(item, self.dict_item[item].split('$')[1]))
                    elif cnt_tmp == 4:
                        self.rbD.SetLabelText("  {}、{}".format(item, self.dict_item[item].split('$')[1]))
            except:
                pass


class MyApp(wx.App):
    def OnInit(self):
        myframe = IeltsTest()
        myframe.Show()
        return True

    def OnExit(self):
        return 0


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()