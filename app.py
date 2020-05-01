from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('xCCQwGVRRmxjhszvdG02KkVFxC4jHA7U44ZZ4OCgzFJIpyL6g/HJ7wwuiKsLJxgigvl0Po7zwK3x1b2QCv2ozplOcEQUMNKrsDpL+BSSXmlJWkOPVFPAKyFkdXeAuYCFRfurgXPR6uAE78H//1CuLgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3ab8e92a15e1c060ac872d493fd79b5a')

# 發送訊息到 www.line-bot.com/callback
# 接收 "Line" 傳來的訊息
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__": #確保此檔案可直接執行的而不是載入
    app.run()