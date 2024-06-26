import requests
import json

"""
#코드 발급 주소
#친구에게 보내기
https://kauth.kakao.com/oauth/authorize?client_id=0bc6ae8b19a4d0bc6920200d89f2dcf3&redirect_uri=https://naver.com/oauth&response_type=code&scope=talk_message,friends

#발급받은 코드
#친구에게 보내기
xnbb2xQ0c5wABmwl7VTrklpCHzTyt9IPLQN11WCa0l_vW1aTFTgElAAAAAQKKwzUAAABkAaPtyVb9Pmr5eg_ZA
"""
"""
#인증토큰 발급 코드

url = 'https://kauth.kakao.com/oauth/token'
client_id = '0bc6ae8b19a4d0bc6920200d89f2dcf3'
redirect_uri = 'https://naver.com/oauth'
code = 'xnbb2xQ0c5wABmwl7VTrklpCHzTyt9IPLQN11WCa0l_vW1aTFTgElAAAAAQKKwzUAAABkAaPtyVb9Pmr5eg_ZA'
     
data = {
    'grant_type':'authorization_code',
    'client_id':client_id,
    'redirect_uri':redirect_uri,
    'code': code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

#발행된 토큰 저장
with open("/home/student/Desktop/project/Project/token_freind.json","w") as kakao:
    json.dump(tokens, kakao)


with open("/home/student/Desktop/project/Project/token_freind.json","r") as kakao:
        tokens = json.load(kakao)
    
friend_url="https://kapi.kakao.com/v1/api/talk/friends"

headers={
    "Authorization" : "Bearer " + tokens["access_token"]
    #"Authorization" : "Bearer " + "Pb6x8Urpjwnlh6LlS92vVisrTm_O6w_xAAAAAQo9c04AAAGP4PP0821lzvpaqIEo"
}

print(tokens["access_token"])

result = json.loads(requests.get(friend_url, headers=headers).text)
friends_list = result.get("elements")
print(friends_list[0].get("profile_nickname"))
friend_id = friends_list[0].get("uuid")
print(friend_id)
"""
 
def SEND_MESSAGE_TO_FRIEND(objects, num):
    #친구목록 불러오기
    #발행한 토큰 불러오기

    with open("/home/student/Desktop/project/Project/token_freind.json","r") as kakao:
        tokens = json.load(kakao)
    
    #friend_url="https://kapi.kakao.com/v1/api/talk/friends"

    headers={
        "Authorization" : "Bearer " + tokens["access_token"]
    }
    """
    result = json.loads(requests.get(friend_url, headers=headers).text)
    friends_list = result.get("elements")
    #print(friends_list[0].get("profile_nickname"))
    friend_id = friends_list[0].get("uuid")
    #print(friend_id)
    """

    send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

    data={
        #'receiver_uuids': '["{}"]'.format(friend_id),
        'receiver_uuids': '["pZyqk6eSp5OmiriNuIy0h7GDu5emlq6aqpqizw"]',
        "template_object": json.dumps({
            "object_type":"feed",
            'content' : {
            'description' : f'🔎청소 중 {','.join(list(objects))}이 감지되었습니다.🔎\n\
https://storage.googleapis.com/detected_ob/Detected{num}\n\
위 링크를 통해 위치를 확인하세요. :)',
            'image_url' : f'https://storage.googleapis.com/detected_ob/Detected{num}',
            'link' : {
                'web_url': f'https://storage.googleapis.com/detected_ob/Detected{num}',
                    'mobile_web_url': f'https://storage.googleapis.com/detected_ob/Detected{num}'
                }
            }
        })
    }
    response = requests.post(send_url, headers=headers, data=data)
    response.status_code
    print("send done!")
SEND_MESSAGE_TO_FRIEND(("ring"),0)