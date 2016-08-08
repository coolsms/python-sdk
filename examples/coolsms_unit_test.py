# -*- coding: utf8 -*-
# vi:set sw=4 ts=4 expandtab:

import sys
import unittest
sys.path.insert(0, "../")

from sdk.api.message import Message
from sdk.api.group_message import GroupMessage
from sdk.api.sender_id import SenderID
from sdk.api.image import Image
from sdk.coolsms import Coolsms 
from sdk.exceptions import CoolsmsException

import sys,json

def makeSuite(testcase,tests):
    return unittest.TestSuite(map(testcase,tests)) #testcase를 이용해서 testsuite생성

## @class CoolsmsUnitTest 
#  @brief Coolsms Python SDK Unit Test
class CoolsmsUnitTest(unittest.TestCase):

    api_key = "NCS57A43A134D2B9"
    api_secret = "9BF07E949C74516A70D7C6A4D6B2B0D3"

    def setUp(self):
        pass

    ## @brief python sdk 'message' resource test
    def test_message(self):
        cool = Message(self.api_key, self.api_secret)

        ## send 
        params = {
            'type':'sms',
            'to':'01000000000',
            'from':'01000000000',
            'text':'Test Message'
        }
        try:
            cool.send(params)
        except CoolsmsException as e:
            # 402는 잔액부족이기 때문에 테스트 실패사유가 안됨
            if e.code == 402:
                pass
            
        ## status : response 가 None값이 아니라면 성공
        response = cool.status()
        self.assertIsNotNone(response[0]['registdate'])

        ## sent
        try:
            cool.sent()
        except CoolsmsException as e:
            # 404는 메시지 내역이 없는 것이기 때문에 테스트 실패사유가 안됨
            if e.code == 404:
                pass

        ## balane
        response = cool.balance()
        self.assertIsNotNone(response['deferred_payment'])

        ## cancel
        params = {
            'message_id':'TESTMESSAGEID',
        }
        self.assertIsNotNone(cool.cancel(params))

    ## @brief python sdk 'group_message' resource test
    def test_group_message(self):
        cool = GroupMessage(self.api_key, self.api_secret)

        ## create group
        response = cool.create_group()
        group_id = response['group_id']
        self.assertIsNotNone(group_id)

        ## group list
        response = cool.get_group_list()
        self.assertIsNotNone(response['list'][0])

        ## add messages
        params = {
            'group_id':group_id,
            'to':'01000000000',
            'from':'01000000000',
            'text':'TestGroupMessage'
        }
        response = cool.add_messages(params)
        self.assertIsNotNone(response['error_count'])
        
        ## add messages json
        params = [ 
            {"from":"01000000000", "to":"01000000001", "text":"TestGroupMessage"}, 
            {"from":"01000000000", "to":"01000000002", "text":"TestGroupMessage"} 
        ]
        messages = json.dumps(params)
        response = cool.add_messages_json(group_id, messages)
        self.assertIsNotNone(response[0]['error_count'])

        ## get message list
        params = {'group_id':group_id}
        try:
            cool.get_message_list(params)
        except CoolsmsException as e:
            # 404는 메시지 내역이 없는 것이기 때문에 테스트 실패사유가 안됨
            if e.code == 404:
                pass

        ## delete messages
        message_id = 'TESTMESSAGEID'
        response = cool.delete_messages(group_id, message_id)
        self.assertIsNotNone(response['error_count'])

        ## send 
        try:
            cool.send(group_id)
        except CoolsmsException as e:
            # 402는 잔액부족이기 때문에 테스트 실패사유가 안됨
            if e.code == 402:
                pass

    ## @brief python sdk 'image' resource test
    def test_image(self):
        cool = Image(self.api_key, self.api_secret)
        image = 'image/test.jpg'

        ## upload image
        response = cool.upload_image(image)
        image_id = response['image_id'] 
        
        ## get image list
        response = cool.get_image_list()
        self.assertIsNotNone(response['total_count'])

        ## get image info
        response = cool.get_image_info(image_id)
        self.assertIsNotNone(response['file_name'])
        
        ## delete images
        response = cool.delete_images(image_id)
        self.assertIsNotNone(response['success_count'])

    ## @brief python sdk 'sender_id' resource test
    def test_sender_id(self):
        cool = SenderID(self.api_key, self.api_secret)

        ## register
        phone = "01000000000"
        response = cool.register(phone)
        self.assertIsNotNone(response['handle_key'])
        handle_key = response['handle_key']

        ## verify
        try:
            cool.verify(handle_key)
        except CoolsmsException as e:
            # 401은 대기중 상태로 테스트 실패사유가 안됨
            if e.code == 401:
                pass

        ## delete
        response = cool.delete(handle_key)
        self.assertIsNone(response)

        ## get list
        self.assertIsNotNone(cool.get_list())

        ## set_default
        self.assertIsNone(cool.set_default(handle_key))

        ## get_default
        try:
            cool.get_default()
        except CoolsmsException as e:
            # 404는 default sender id가 없는 것이므로 테스트 실패사유가 안됨
            if e.code == 404:
                pass


if __name__ == "__main__":
    suite = makeSuite(CoolsmsUnitTest,['test_message', 'test_group_message', 'test_image', 'test_sender_id'])
    unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit()
