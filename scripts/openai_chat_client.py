#!/usr/bin/env python3

import sys, json
import rospy

from openai_ros.srv import ChatCompletion, ChatCompletionResponse


def chat_client(prompt="You are a helpful assistant."):
    
    messages = []
    messages.append({"role": "system", "content": str(prompt)})
    
    rospy.wait_for_service('chat_service')
    
    try:
        chat_service_client = rospy.ServiceProxy('chat_service', ChatCompletion)
    except rospy.ServiceException as e:
        print ("Service call failed: %s" % e)

    while not rospy.is_shutdown():
        
        # Get input from the user
        user_input = input("You: ")
        if user_input == "quit":
            exit()
        
        # Add user's input to the history
        messages.append({"role": "user", "content": user_input})
        
        msg_string = json.dumps(messages)
        
        # Call the service
        try:
            res_msg = chat_service_client(msg_string)
        except rospy.ServiceException as e:
            print ("Service call failed: %s" % e)
        
        response = json.loads(res_msg.response)
        
        content = response["choices"][0]["message"]["content"]
        role = response["choices"][0]["message"]["role"]
        token = response["usage"]["total_tokens"]
        
        print("\n%s(token:%d): %s\n" % (role, token, content))
        
        # Add GPT's response to the history
        messages.append({"role": str(role), "content": str(content)})


if __name__ == "__main__":
    if len(sys.argv) == 2:
        prompt = str(sys.argv[1])
    else:
        prompt = "You are a helpful assistant."
    
    print("Type \'quit\' to quit.\n")
    print("For \'system\': %s\n" % (prompt))
    rospy.init_node('chat_client')
    
    chat_client(prompt=prompt)

