import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from json import load

class Watson_API_Session:

    def __init__(self, API_KEY, DRAFT_ID):
        self.DRAFT_ID = DRAFT_ID
        
        self.ASSISTANT = AssistantV2(
            version='2021-06-14',
            authenticator=IAMAuthenticator(API_KEY)
        )
        self.ASSISTANT.set_service_url("https://api.au-syd.assistant.watson.cloud.ibm.com/instances/69f6c87a-3aad-4ab8-b7a8-3092edcb433c")

        self.RESPONSE_IN = None
        self.RESPONSE_MSG = None
        self.RESPONSE_OUT = None
        self.MSG = None

    def create_session(self):
        self.RESPONSE_IN = self.ASSISTANT.create_session(
            assistant_id=self.DRAFT_ID
        ).get_result()

        print("============SESSION CREATED============")
    
    def delete_session(self):
        self.RESPONSE_OUT = self.ASSISTANT.delete_session(
            assistant_id=self.DRAFT_ID,
            session_id=self.RESPONSE_IN["session_id"]
        ).get_result()

        print("============SESSION DELETED============")
    
    def hdd(self):

        print("size: " + str(len(self.RESPONSE_MSG["output"]["generic"]))) 
        print(self.RESPONSE_MSG)

    def handle_msg(self):
        
        try:
            response_type = self.RESPONSE_MSG["output"]["generic"][0]["response_type"]

            if response_type == "option":
                labels = self.RESPONSE_MSG["output"]["generic"][0]["options"]
                
                print("-----------labels----------")
                for label in labels:
                    print(label["label"])

                print("Choose label:")
                x = input()
               
                self.send_msg(x)
                self.handle_msg() 
        except:
            print("Empty")
        
        if len(self.RESPONSE_MSG["output"]["generic"]) > 0: 
            self.MSG = self.RESPONSE_MSG["output"]["generic"][0]["text"]

        print("==============MSG HENDLED=============")
    
    def send_msg(self, msg):
        self.RESPONSE_MSG = self.ASSISTANT.message(
            assistant_id=self.DRAFT_ID,
            session_id=self.RESPONSE_IN["session_id"],
            input={
                'message_type': 'text',
                'text': msg
            }
        ).get_result()

        print("============MESSEGE SENT==============")
    
    def get_msg(self):
        print("===============MSG GOT================")
        return self.MSG

#=======================================================================================

def load_lines_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    line1 = lines[0].strip()
    line2 = lines[1].strip()

    return line1, line2



def main():
    
    API_KEY, DRAFT_ID = load_lines_from_file('private.txt')
    BOT = Watson_API_Session(API_KEY, DRAFT_ID)
    
    BOT.create_session()

    print("type QUIT to end chat sesssion")

    while 1 :    
        print("Ask question")
        
        x = input()
        if x == "QUIT":
            break
        
        BOT.send_msg(x)
        BOT.handle_msg()
        #BOT.hdd()
        print(BOT.get_msg())
    
    BOT.delete_session()

main()
