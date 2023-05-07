from kavenegar import *


def send_otp_code(phone_number, code):
     print('{} send to: {}'.format(code, phone_number))
     pass
     # try:
     #      api = KavenegarAPI('466643684A5762693536474E51644953386B68496356794C712F6253664B7635514752305A7859514A78413D')
     #      params = {
     #           'receptor': phone_number,
     #           'template': 'Verify-1',
     #           'token': code,
     #           'type': 'sms',#sms vs call
     #      }   
     #      response = api.verify_lookup(params)
     #      # print(response)
     # except APIException as e: 
     #      print(e)
     # except HTTPException as e: 
     #      print(e)