#!/usr/bin/env python3

import rospy
import openai

from std_msgs.msg import String


class Chatter:
    """
    Chat with ChatGPT on ROS topics
    """
    def __init__(self):
        # Get ROS parameters
        prompt = rospy.get_param('~prompt')
        self.model = rospy.get_param('~model')
        openai.api_key = rospy.get_param('~key')
        
        rospy.loginfo("For \'system\': %s" % (prompt))
        
        # Set initial message with a prompt
        self.messages = []
        self.messages.append({"role": "system", "content": str(prompt)})
        
        self.sub = rospy.Subscriber('request', String, self.callback)
        self.pub = rospy.Publisher('response', String, queue_size=10)
        
        rospy.spin()


    def callback(self, data):
        rospy.loginfo("request: %s", data.data)
        
        # Add user's input to the history
        self.messages.append({"role": "user", "content": str(data.data)})
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        
        content = response["choices"][0]["message"]["content"]
        role = response["choices"][0]["message"]["role"]
        token = response["usage"]["total_tokens"]
        
        # Add GPT's response to the history
        self.messages.append({"role": str(role), "content": str(content)})
        
        rospy.loginfo("%s(token:%d): %s" % (role, token, content))
        self.pub.publish(content)


if __name__ == "__main__":
    rospy.init_node('chat_rostopic', anonymous=True)
    chatter = Chatter()
    
