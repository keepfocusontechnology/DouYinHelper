import requests
import binascii 
import gzip
import re
import urllib
import json
import websocket
from google.protobuf import json_format
from bean.dy_pb2 import PushFrame,Response,ChatMessage


def onOpen(ws,content):
    print('on_open')

def onMessage(ws,content):
    
    frame = PushFrame()
    frame.ParseFromString(body_bytes)

    origin_bytes=gzip.decompress(frame.payload)

    resp = Response()
    resp.ParseFromString(origin_bytes)

    for item in resp.messagesList:
        print(item.method)
        if item.method != "WebcastChatMessage":
            continue
        msg = ChatMessage()
        msg.ParseFromString(item.payload)
        info = f"{msg.user.nickName} 说: {msg.content} "
        print(info)

def onError(ws,content):
     info = f"错误内容为: {content} "
     print(info)

def onClose(ws,content):
     print('on_cloese')


def parseLiveRoomUrl(url):
    h={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'cookie': '__ac_nonce=0638733a400869171be51',
    }
    res = requests.get(url=url,headers=h)
    global ttwid, roomStore, liveRoomId, liveRoomTitle
    data = res.cookies.get_dict()
    ttwid = data['ttwid']
    res = res.text
    res = re.search(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', res)
    res = res.group(1)
    res = urllib.parse.unquote(res, encoding='utf-8', errors='replace')
    res = json.loads(res)
    roomStore = res['app']['initialState']['roomStore']
    liveRoomId = roomStore['roomInfo']['roomId']
    liveRoomTitle = roomStore['roomInfo']['room']['title']
    wssServerStart(liveRoomId) 

def wssServerStart(roomId):
    global liveRoomId
    liveRoomId = roomId
    websocket.enableTrace(False)
    webSocketUrl = 'wss://webcast3-ws-web-lq.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.3.0&update_version_code=1.3.0&compress=gzip&internal_ext=internal_src:dim|wss_push_room_id:'+liveRoomId+'|wss_push_did:7188358506633528844|dim_log_id:20230520121945B46758C962558DB5E3C1|fetch_time:1684556385653|seq:6|wss_info:0-1684556379596-1-0|wrds_kvs:WebcastRoomRankMessage-1684555970811623853_WebcastRoomStatsMessage-1684556384766727459&cursor=d-1_u-1_h-1_t-1684556385653_r-7235114581843136473_rdc-2&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&debug=false&maxCacheMessageNumber=20&endpoint=live_pc&support_wrds=1&im_path=/webcast/im/fetch/&user_unique_id=7188358506633528844&device_platform=web&cookie_enabled=true&screen_width=1440&screen_height=900&browser_language=zh&browser_platform=MacIntel&browser_name=Mozilla&browser_version=5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/113.0.0.0%20Safari/537.36&browser_online=true&tz_name=Asia/Shanghai&identity=audience&room_id='+liveRoomId+'&heartbeatDuration=0&signature=RDggdDS41veLqFHS'
    h = {
        'cookie': 'ttwid='+ttwid,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    # 创建一个长连接
    ws = websocket.WebSocketApp(
        webSocketUrl, on_message=onMessage, on_error=onError, on_close=onClose,
        on_open=onOpen,
        header=h
    )
    ws.run_forever()



def run():
    web_url = "https://live.douyin.com/80017709309"
    parseLiveRoomUrl(web_url)

if __name__ == '__main__':
    run()




"wss://webcast3-ws-web-hl.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.3.0&update_version_code=1.3.0&compress=gzip&internal_ext=internal_src:dim|wss_push_room_id:7234986737615833913|wss_push_did:7169945237800470068|dim_log_id:2023052011085415C3A320A421EB8D690F|fetch_time:1684552134379|seq:1|wss_info:0-1684552134379-0-0|wrds_kvs:InputPanelComponentSyncData-1684539991595369155_WebcastRoomStatsMessage-1684552128687433340_WebcastRoomRankMessage-1684551672732793020&cursor=t-1684552134379_r-1_d-1_u-1_h-1&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&debug=false&maxCacheMessageNumber=20&endpoint=live_pc&support_wrds=1&im_path=/webcast/im/fetch/&user_unique_id=7169945237800470068&device_platform=web&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36&browser_online=true&tz_name=Asia/Hong_Kong&identity=audience&room_id=7234986737615833913&heartbeatDuration=0&signature=RBYe+w9+Ha4ndnz/"


"wss://webcast3-ws-web-lq.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.3.0&update_version_code=1.3.0&compress=gzip&internal_ext=internal_src:dim|wss_push_room_id:7234986737615833913|wss_push_did:7169945237800470068|dim_log_id:20230520154230C3BB361A117732F41168|fetch_time:1684568550181|seq:1|wss_info:0-1684568550181-0-0|wrds_kvs:MoreLiveSyncData-1684568524224065496_WebcastRoomStatsMessage-1684568544683579626_WebcastRoomRankMessage-1684568496793548112_InputPanelComponentSyncData-1684539991595369155&cursor=t-1684568550181_r-1_d-1_u-1_h-1&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&debug=false&maxCacheMessageNumber=20&endpoint=live_pc&support_wrds=1&im_path=/webcast/im/fetch/&user_unique_id=7169945237800470068&device_platform=web&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36&browser_online=true&tz_name=Asia/Hong_Kong&identity=audience&room_id=7234986737615833913&heartbeatDuration=0&signature=RKop3QicaXMJu/kL"



 