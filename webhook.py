#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import os 
app = Flask(__name__)
ACCESS_TOKEN = 'EAAHCL6rXeeYBAPjWbXz7qpKwD0hjgdB0bgZCPJcZB0F5vIycpgaXd01VpNkBN5SqIGbX2waaHaoT1oX8R3LqW5GXLXyYvZCjZCtK3bYdk9fYZBfYa17zijtj9ZBMlbE08nM83G3ldlkrb8ZB9bmlqYpwyQM4ZAKGUAA6NRV6o6biJceulU0JRjPI'   #ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = 'TESTINGTOKEN'   #VERIFY_TOKEN = os.environ['VERIFY_TOKEN'] 
bot = Bot(ACCESS_TOKEN)
      

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/fb", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       # config for faceboob webhook
       for event in output['entry']:
           # check if the webhook data is a facebook message
            if 'messaging' in event:
                messaging = event['messaging']
                print('message is:', messaging)
                for message in messaging:
                    if message.get('message'):
                        #Facebook Messenger ID for user so we know where to send response back to
                        recipient_id = message['sender']['id']
                        if message['message'].get('text'):
                            response_sent_text = get_message(message['message'].get('text'))
                            send_message(recipient_id, response_sent_text)
                        #if user sends us a GIF, photo,video, or any other non-text item
                        if message['message'].get('attachments'):
                            response_sent_nontext = get_message()
                            send_message(recipient_id, response_sent_nontext)
            # if not facebook message print out
            else:
                print('output data:', output)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    print(token_sent)
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message(sender_msg):
    print('sender msg',sender_msg)
    response_str =''
    #p = Payload.__init__('')
    #r= Response.__init__('',p)
    if (sender_msg.find('menu') != -1):
        response_str= 'Menu hôm nay gồm có: Bánh thuyền, Bánh hạnh nhân ... Bạn chọn bánh gì?'
        #print ('réponse', r)
    else:
        response_str= 'Bạn gửi tin là:' + sender_msg
    #sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    #return random.choice(sample_responses)
    #response_str = 
    return response_str

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()