# -*- coding: utf-8 -*-
# @Time    : 18-11-27 上午11:07
# @Author  : Felix Wang

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import random

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import parseaddr, formataddr
from email.header import Header
import smtplib
from hashlib import md5


class CheckCode:
    def __init__(self, font_file, font_size=36, width=240, height=60, char_length=4, start_color_num=0,
                 end_color_num=255, is_simple=True, is_oncache=False):
        self.is_oncache = is_oncache
        self.is_simple = is_simple
        self.font_file = font_file
        self.font_size = font_size
        self.width = width
        self.height = height
        self.char_length = char_length
        self.start_num = start_color_num
        self.end_num = end_color_num
        # 定义使用Image类实例化一个长为120px,宽为30px,基于RGB的(255,255,255)颜色的图片
        self.image = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        # 创建Font对象:
        self.font = ImageFont.truetype(self.font_file, self.font_size)
        # 创建Draw对象:
        self.draw = ImageDraw.Draw(self.image)
        # 双下划綫的变量在类中不能直接访问起到保护的作用
        self.__code_text = []

    def get_random_code(self, time=1):
        """
        :param is_simple: 是否包含中文繁体字，默认不包含，True表示不包含
        :param time: 返回多少个
        :return: 返回一个随机字符列表
        """
        is_simple = self.is_simple
        codes = []
        for i in range(time):
            num = chr(random.randint(0x30, 0x39))  # 随机生成数字
            lowercase = chr(random.randint(0x61, 0x74))  # 随机生成小写字母
            capcase = chr(random.randint(0x41, 0x5a))  # 随机生成大写字母

            # Unicode编码的汉字，带繁体字 ，共2万多字
            zh = chr(random.randint(0x4e00, 0x9fbf))

            # gbk编码的简单汉字，无繁体字
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
            val = f'{head:x}{body:x}'
            ch = bytes.fromhex(val).decode('gb2312')

            if is_simple:
                # code = random.choice([ch, num, lowercase, capcase])
                code = random.choice([ch, num, lowercase, capcase])
            else:
                code = random.choice([zh, num, lowercase, capcase])
            codes.append(code)
        return codes

    # 随机颜色:
    def rndColor(self, start, end, randomflag=True):
        """
        :param start:
        :param end:
        :param randomflag: 是否返回随机参数，
        :return:
        """
        return (random.randint(start, end), random.randint(start, end),
                random.randint(start, end))

    def rotate(self):
        self.image.rotate(random.randint(0, 90), expand=0)

    # 随机点
    def randPoint(self):
        return (random.randint(0, self.width), random.randint(0, self.height))

    # 随机线
    def randLine(self, num):
        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
            draw.line([self.randPoint(), self.randPoint()], self.rndColor(0, 255))
        del draw

    # 获取验证码
    def get_codes(self):
        return self.__code_text

    def draw_pic(self):
        # 填充每个像素:
        # 单一背景
        color = self.rndColor(170, 255)  # 可以把背景调浅色
        for x in range(self.width):
            for y in range(self.height):
                self.draw.point((x, y), fill=color)

        # 输出文字:
        codes = self.get_random_code(time=self.char_length)
        self.__code_text = []
        for ii in range(self.char_length):
            code = self.get_random_code()[0]
            self.__code_text.append(code)
            self.draw.text([random.randint(int((self.width / 2 - self.font_size / 2) / self.char_length * 2 * ii),
                                           int((self.width / 2 - self.font_size / 2) / self.char_length * 2 * (
                                                   ii + 1))), random.randint(0, self.height / 4)],
                           code, font=self.font, fill=self.rndColor(0, 120))  # 把字体调深色
        # self.rotate()

        # 画出随机线
        self.randLine(10)

        # 模糊:
        # self.image = self.image.filter(ImageFilter.BLUR)
        if self.is_oncache:  # 保存在缓存
            f = BytesIO()
            self.image.save(f, 'jpeg')
            return f.getvalue()
        else:
            # 保存
            self.image.save('{}.jpg'.format(''.join(self.get_codes())), 'jpeg')


# 自动发邮件
class AutoSendEmail:
    def __init__(self, sender, password, title, from_who, recever, smtp_server="smtp.qq.com", port=465):
        """
        :param sender: 邮件发送者
        :param password: 密码
        :param title: 邮件发送主题
        :param from_who: 邮件来自谁
        :param recever: 邮件接收者，可以是多个
        :param smtp_server: 邮件服务器，默认qq邮箱服务器
        :param port: 服务器端口qq邮箱默认端口为465
        """
        self.smtp_server = smtp_server  # 使用qq转发需要用到，可以在QQ邮箱设置中查看并开通此转发功能
        self.smtp_port = port  # smtp默认的端口是465
        # 接受者可以是多个，放在列表中
        self.recever = recever
        self.sender = sender
        self.password = password  # 该密码是配置qq邮箱的SMTP功能的授权码
        self.msg = MIMEMultipart()
        self.msg['Subject'] = title  # 邮件标题
        self.msg['From'] = self._format_addr(u'{} <{}>'.format(from_who, self.sender))

    # 添加文字信息
    def addTextMsg(self, text):
        text_plain = MIMEText(text, 'plain', 'utf-8')
        self.msg.attach(text_plain)

    # 添加图片
    def addImageMsg(self, imgPath):
        extend = imgPath.split('.')[-1]
        with open(imgPath, 'rb')as f:
            sendimagefile = f.read()
            filename = md5(sendimagefile).hexdigest() + '.' + extend
        image = MIMEImage(sendimagefile)
        image.add_header('Content-ID', '<image1>')
        image["Content-Disposition"] = u'attachment; filename={}'.format(filename)
        self.msg.attach(image)

    # 添加附件
    def addFile(self, filePath):
        extend = filePath.split('.')[-1]
        with open(filePath, 'rb')as f:
            sendfile = f.read()
            filename = md5(sendfile).hexdigest() + '.' + extend
        # 构造附件
        text_att = MIMEText(sendfile, 'base64', 'utf-8')
        text_att["Content-Type"] = 'application/octet-stream'
        text_att["Content-Disposition"] = u'attachment; filename="{}"'.format(filename)
        self.msg.attach(text_att)

    # 添加html格式
    def addHtml(self, html):
        # 构造html
        # 发送正文中的图片:由于包含未被许可的信息，网易邮箱定义为垃圾邮件，报554 DT:SPM ：<p><img src="cid:image1"></p>
        text_html = MIMEText(html, 'html', 'utf-8')
        self.msg.attach(text_html)

    # 格式化邮件地址
    def _format_addr(self, s):
        name, address = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), address))

    # 发送邮件
    def sendEmail(self):
        server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)  # 链接服务器
        server.set_debuglevel(1)  # 打印出和SMTP服务器交互的信息
        server.login(self.sender, self.password)  # 登录
        server.sendmail(self.sender, self.recever, self.msg.as_string())  # 发送邮件
        server.quit()  # 退出
        print('邮件发送成功')


if __name__ == '__main__':
    smtp_server = "smtp.qq.com"  # smtp服务地址
    port = 465  # 端口号
    recever = ['1403179190@qq.com']  # 接收人列表可以是多个
    sender = "1403179190@qq.com"  # 发送人邮箱
    password = ""  # 如果是qq邮箱的话该密码是配置qq邮箱的SMTP功能的授权码
    title = '验证码'
    from_who = 'felixCRM'  # 发送人姓名

    # 实例化对象
    autoEmail = AutoSendEmail(sender=sender, recever=recever, password=password, title=title, from_who=from_who,
                              smtp_server=smtp_server, port=port)

    html = """
        <html>  
          <head></head>  
          <body>  
            <p>Hi!<br>  
               欢迎注册felixCRM系统！
               <br>  
               Here is the <a href="http://www.baidu.com">link</a> you wanted.<br> 
            </p> 
            <img src="http://img.zcool.cn/community/01f09e577b85450000012e7e182cf0.jpg@1280w_1l_2o_100sh.jpg"></img>
          </body>  
        </html>  
        """
    # 以html的形式发送文字，推荐这个，因为可以添加图片等
    autoEmail.addHtml(html)
    # 发送邮件
    try:
        autoEmail.sendEmail()
    except Exception as e:
        print(e)
        print('邮件发送失败')

if __name__ == '__main__':

    # 这里的字体采用能识别中文的字体
    # font_file = '‪C:\Windows\Fonts\simhei.ttf' # windows使用这个
    font_file = '/home/felix/.local/share/fonts/SIMHEI.TTF'
    checkcode = CheckCode(font_file=font_file, is_simple=True, char_length=random.randint(3, 5))

    # 生成多张验证码
    for i in range(1):
        checkcode.draw_pic()
        # 生成的验证码的内容
        codes = checkcode.get_codes()
        print(i, codes)
