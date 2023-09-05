#!/usr/bin/env python3

import rospy
import openai
import json

from openai_ros.srv import ChatCompletion, ChatCompletionResponse


def handle_chat_request(req):

    openai.api_key = rospy.get_param('~key')
    model = rospy.get_param('~model')
    
    res = ChatCompletionResponse()
    messages = json.loads(req.messages)
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    
    return json.dumps(response)


def chat_service():
    rospy.init_node('chat_service')
    rospy.Service('chat_service', ChatCompletion, handle_chat_request)
    rospy.spin()


if __name__ == "__main__":
    chat_service()

