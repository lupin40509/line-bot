import sys
import datetime
import gspread
from  oauth2client.service_account import ServiceAccountCredentials as SAC

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('xCCQwGVRRmxjhszvdG02KkVFxC4jHA7U44ZZ4OCgzFJIpyL6g/HJ7wwuiKsLJxgigvl0Po7zwK3x1b2QCv2ozplOcEQUMNKrsDpL+BSSXmlJWkOPVFPAKyFkdXeAuYCFRfurgXPR6uAE78H//1CuLgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3ab8e92a15e1c060ac872d493fd79b5a')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉,你說什麼?'
    GDriveJSON = 'linebot.json'
    GSpreadSheet = 'Line Bot Order'

    if msg in ['hi','Hi']:
        r = '嗨'
    elif '吃飯' in msg:
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位,是嗎?'
    elif msg == '你好':
        r = '你好'
    elif '下訂' in msg:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="你想訂什麼?"))
        pass
        

        scope = ['https://docs.google.com/spreadsheets/d/18ehKGZg9RQSmAap0MyCdEL5acTa0r4fkOgLojNXsszc/edit?usp=sharing']
        key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open(GSpreadSheet).sheet1
        if msg != "":
            worksheet.append_row((datetime.datetime.now(), msg))

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__": 
    app.run()