import requests
import binascii 
import gzip
import re
import urllib
import json
from urllib.parse import unquote_plus
import websocket
from google.protobuf import json_format

from bean.dy_pb2 import PushFrame
from bean.dy_pb2 import Response
from bean.dy_pb2 import MatchAgainstScoreMessage
from bean.dy_pb2 import LikeMessage
from bean.dy_pb2 import MemberMessage
from bean.dy_pb2 import GiftMessage
from bean.dy_pb2 import ChatMessage
from bean.dy_pb2 import SocialMessage
from bean.dy_pb2 import RoomUserSeqMessage
from bean.dy_pb2 import UpdateFanTicketMessage
from bean.dy_pb2 import CommonTextMessage
from websocket import WebSocketApp


def onOpen(ws):
    print('onOpen')
    

def onError(ws,content):
     print(content)

def onClose(ws):
     print('onClose')

def onMessage(ws: websocket.WebSocketApp, message: bytes):
    wssPackage = PushFrame()
    wssPackage.ParseFromString(message)
    logId = wssPackage.logId
    decompressed = gzip.decompress(wssPackage.payload)
    payloadPackage = Response()
    payloadPackage.ParseFromString(decompressed)
    # 发送ack包
    if payloadPackage.needAck:
        sendAck(ws, logId, payloadPackage.internalExt)
    for msg in payloadPackage.messagesList:
        # if msg.method == 'WebcastMatchAgainstScoreMessage':
        #     unPackMatchAgainstScoreMessage(msg.payload)
        #     continue

        # if msg.method == 'WebcastLikeMessage':
        #     unPackWebcastLikeMessage(msg.payload)
        #     continue

        # if msg.method == 'WebcastMemberMessage':
        #     unPackWebcastMemberMessage(msg.payload)
        #     continue
        if msg.method == 'WebcastGiftMessage':
            unPackWebcastGiftMessage(msg.payload)
            continue
        if msg.method == 'WebcastChatMessage':
            unPackWebcastChatMessage(msg.payload)
            continue

        # if msg.method == 'WebcastSocialMessage':
        #     unPackWebcastSocialMessage(msg.payload)
        #     continue

        # if msg.method == 'WebcastRoomUserSeqMessage':
        #     unPackWebcastRoomUserSeqMessage(msg.payload)
        #     continue

        # if msg.method == 'WebcastUpdateFanTicketMessage':
        #     unPackWebcastUpdateFanTicketMessage(msg.payload)
        #     continue

        # if msg.method == 'WebcastCommonTextMessage':
        #     unPackWebcastCommonTextMessage(msg.payload)
        #     continue

        # print('[onMessage] [⌛️方法' + msg.method + '等待解析～] [房间Id：' + liveRoomId + ']')


def unPackWebcastCommonTextMessage(data):
    commonTextMessage = CommonTextMessage()
    commonTextMessage.ParseFromString(data)
    data = json_format.MessageToDict(commonTextMessage, preserving_proto_field_name=True)
    log = json.dumps(data, ensure_ascii=False)
    print('[unPackWebcastCommonTextMessage] [] [房间Id：' + liveRoomId + '] ｜ ' + log)
    return data


def unPackWebcastUpdateFanTicketMessage(data):
    updateFanTicketMessage = UpdateFanTicketMessage()
    updateFanTicketMessage.ParseFromString(data)
    data = json_format.MessageToDict(updateFanTicketMessage, preserving_proto_field_name=True)
    log = json.dumps(data, ensure_ascii=False)
    print('[unPackWebcastUpdateFanTicketMessage] [] [房间Id：' + liveRoomId + '] ｜ ' + log)
    return data


def unPackWebcastRoomUserSeqMessage(data):
    roomUserSeqMessage = RoomUserSeqMessage()
    roomUserSeqMessage.ParseFromString(data)
    data = json_format.MessageToDict(roomUserSeqMessage, preserving_proto_field_name=True)
    log = json.dumps(data, ensure_ascii=False)
    print('[unPackWebcastRoomUserSeqMessage] [] [房间Id：' + liveRoomId + '] ｜ ' + log)
    return data


def unPackWebcastSocialMessage(data):
    socialMessage = SocialMessage()
    socialMessage.ParseFromString(data)
    data = json_format.MessageToDict(socialMessage, preserving_proto_field_name=True)
    log = json.dumps(data, ensure_ascii=False)
    print('[unPackWebcastSocialMessage] [➕直播间关注消息] [房间Id：' + liveRoomId + '] ｜ ' + log)
    return data


# 普通消息
def unPackWebcastChatMessage(data):
    chatMessage = ChatMessage()
    chatMessage.ParseFromString(data)
    data = json_format.MessageToDict(chatMessage, preserving_proto_field_name=True)
    # print('[unPackWebcastChatMessage] [📧直播间弹幕消息] [房间Id：' + liveRoomId + '] ｜ ' + data['content'])
    info = f"{chatMessage.user.nickName}说：{chatMessage.content}"
    print(info)
    # print('[unPackWebcastChatMessage] chatMessage ｜ ' + data['content'])
    # print('[unPackWebcastChatMessage] [📧直播间弹幕消息] [房间Id：' + liveRoomId + '] ｜ ' + json.dumps(data))
    return data


# 礼物消息
def unPackWebcastGiftMessage(data):
    giftMessage = GiftMessage()
    giftMessage.ParseFromString(data)
    data = json_format.MessageToDict(giftMessage, preserving_proto_field_name=True)
    log = json.dumps(data, ensure_ascii=False)
    # print('[unPackWebcastGiftMessage] [🎁直播间礼物消息] [房间Id：' + liveRoomId + '] ｜ log')
    info = f"*****礼物消息【{data['user']['nickName']}】{data['common']['describe']}"
    print(info)
    return data


# xx成员进入直播间消息
def unPackWebcastMemberMessage(data):
    memberMessage = MemberMessage()
    memberMessage.ParseFromString(data)
    data = json_format.MessageToDict(memberMessage, preserving_proto_field_name=True)
    log = json.dumps(data, ensure_ascii=False)
    print('[unPackWebcastMemberMessage] [🚹🚺直播间成员加入消息] [房间Id：' + liveRoomId + '] ｜ ' + log)
    return data


# 点赞
def unPackWebcastLikeMessage(data):
    likeMessage = LikeMessage()
    likeMessage.ParseFromString(data)
    data = json_format.MessageToDict(likeMessage, preserving_proto_field_name=True)
    log = json.dumps(data, ensure_ascii=False)
    print('[unPackWebcastLikeMessage] [👍直播间点赞消息] [房间Id：' + liveRoomId + '] ｜ ' + log)
    return data


# 解析WebcastMatchAgainstScoreMessage消息包体
def unPackMatchAgainstScoreMessage(data):
    matchAgainstScoreMessage = MatchAgainstScoreMessage()
    matchAgainstScoreMessage.ParseFromString(data)
    data = json_format.MessageToDict(matchAgainstScoreMessage, preserving_proto_field_name=True)
    log = json.dumps(data, ensure_ascii=False)
    print('[unPackMatchAgainstScoreMessage] [🤷不知道是啥的消息] [房间Id：' + liveRoomId + '] ｜ ' + log)
    return data


# 发送Ack请求
def sendAck(ws, logId, internalExt):
    obj = PushFrame()
    obj.payloadType = 'ack'
    obj.logId = logId
    obj.payloadType = internalExt
    data = obj.SerializeToString()
    ws.send(data, websocket.ABNF.OPCODE_BINARY)
    # print('[sendAck] [🌟发送Ack] [房间Id：' + liveRoomId + '] ====> 房间🏖标题【' + liveRoomTitle + '】')



def fetch_live_room_info(url):
    res = requests.get(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        },
        cookies={
            "__ac_nonce": "063abcffa00ed8507d599"  # 可以是任意值
        }
    )
    data_string = re.findall(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', res.text)[0]
    data_dict = json.loads(unquote_plus(data_string))

    room_id = data_dict['app']['initialState']['roomStore']['roomInfo']['roomId']
    room_title = data_dict['app']['initialState']['roomStore']['roomInfo']["room"]['title']
    room_user_count = data_dict['app']['initialState']['roomStore']['roomInfo']["room"]['user_count_str']

    wss_url = f"wss://webcast3-ws-web-hl.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.3.0&update_version_code=1.3.0&compress=gzip&internal_ext=internal_src:dim|wss_push_room_id:{room_id}|wss_push_did:7169945237800470068|dim_log_id:202305211845404BC31A40C91C83B5E682|fetch_time:1684665940167|seq:1|wss_info:0-1684665940167-0-0|wrds_kvs:WebcastRoomStatsMessage-1684665936654448799_WebcastRoomRankMessage-1684665564689274908&cursor=t-1684665940167_r-1_d-1_u-1_h-1&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&debug=false&maxCacheMessageNumber=20&endpoint=live_pc&support_wrds=1&im_path=/webcast/im/fetch/&user_unique_id=7169945237800470068&device_platform=web&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/113.0.0.0%20Safari/537.36&browser_online=true&tz_name=Asia/Hong_Kong&identity=audience&room_id={room_id}&heartbeatDuration=0&signature=WhzeuN2igfWGPvwb"

    # wss_url = f"wss://webcast3-ws-web-lq.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.3.0&update_version_code=1.3.0&compress=gzip&internal_ext=internal_src:dim|wss_push_room_id:{room_id}|wss_push_did:7188358506633528844|dim_log_id:20230520121945B46758C962558DB5E3C1|fetch_time:1684556385653|seq:6|wss_info:0-1684556379596-1-0|wrds_kvs:WebcastRoomRankMessage-1684555970811623853_WebcastRoomStatsMessage-1684556384766727459&cursor=d-1_u-1_h-1_t-1684556385653_r-7235114581843136473_rdc-2&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&debug=false&maxCacheMessageNumber=20&endpoint=live_pc&support_wrds=1&im_path=/webcast/im/fetch/&user_unique_id=7188358506633528844&device_platform=web&cookie_enabled=true&screen_width=1440&screen_height=900&browser_language=zh&browser_platform=MacIntel&browser_name=Mozilla&browser_version=5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/113.0.0.0%20Safari/537.36&browser_online=true&tz_name=Asia/Shanghai&identity=audience&room_id={room_id}&heartbeatDuration=0&signature=WhzeuN2igfWGPvwb"

    global liveRoomId,liveRoomTitle
    
    liveRoomId = room_id
    liveRoomTitle = room_title
    ttwid = res.cookies.get_dict()['ttwid']
    return room_id, room_title, room_user_count, wss_url, ttwid


def run():
    web_url = "https://live.douyin.com/324034686283"
    room_id, room_title, room_user_count, wss_url, ttwid = fetch_live_room_info(web_url)

    print(room_id, room_title, room_user_count, wss_url, ttwid)

    ws = WebSocketApp(
        url=wss_url,
        header={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        },
        cookie=f"ttwid={ttwid}",
        on_open=onOpen,
        on_message=onMessage,
        on_error=onError,
        on_close=onClose,
    )
    ws.run_forever()

if __name__ == '__main__':
    run()




 