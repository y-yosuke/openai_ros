#!/usr/bin/env python3
import rospy
from openai_ros.srv import GptService, GptServiceResponse
import openai

def handle_gpt_request(req):
#    openai.api_key = 'your-api-key'
    openai.api_key = rospy.get_param('~key')
    
    response = openai.ChatCompletion.create(
#        model="gpt-4.0-turbo",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "{} '{}'".format(req.prompt, req.input)}
        ]
    )

    return GptServiceResponse(response['choices'][0]['message']['content'])

def gpt_service():
    rospy.init_node('gpt_service')
    s = rospy.Service('gpt_service', GptService, handle_gpt_request)
#    print("Ready to handle GPT-4 requests.")
    print("Ready to handle GPT-3.5 requests.")
    rospy.spin()

if __name__ == "__main__":
    gpt_service()

