# Coolsms Python SDK

Send Message & Message Management using Python and REST API.

## Version

v2.0.1

## License

BSD License

## Installation

- Package install url ( source code & examples ) : http://www.coolsms.co.kr/download/545387

- Github : https://github.com/coolsms/python-sdk

## Usage 

### Send Message
```python
	from sdk.api.message import Message
	from sdk.exceptions import CoolsmsException

	# set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    ## 4 params(to, from, type, text) are mandatory. must be filled
    params = dict()
    params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
    params['to'] = '01000000000' # Recipients Number '01000000000,01000000001'
    params['from'] = '01000000000' # Sender number
    params['text'] = 'Test Message' # Message

	cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)
```

### Message History
```python
	from sdk.api.message import Message
	from sdk.exceptions import CoolsmsException

	# set api key, api secret
    api_key = "#ENTER_YOUR_OWN#"
    api_secret = "#ENTER_YOUR_OWN#"

    cool = Message(api_key, api_secret)
    try:
        i = 0
        response = cool.sent()
        for data in response['data']:
            i += 1
            print("Message No.%s" % i)
            print("Type : %s" % data['type'])
            print("Accepted_time : %s" % data['accepted_time'])
            print("Recipient_number : %s" % data['recipient_number'])
            print("Group_id : %s" % data['group_id'])
            print("Message_id : %s" % data['message_id'])
            print("Status : %s" % data['status'])
            print("Result_code : %s" % data['result_code'])
            print("Result_message : %s" % data['result_message'])
            print("Sent_time : %s" % data['sent_time'])
            print("Text : %s" % data['text'])
            print("Carrier : %s" % data['carrier'])
            print("Scheduled_time : %s" % data['scheduled_time'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)
```

If you want more examples. Visit to 'http://www.coolsms.co.kr/Python_SDK_Example'.

## Information

Look at the 'http://www.coolsms.co.kr/Python_SDK_Start_here'
