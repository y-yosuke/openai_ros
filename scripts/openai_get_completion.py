#!/usr/bin/env python3

import sys
import rospy

from openai_ros.srv import Completion, CompletionResponse


def get_response_client(prompt):
  request = '{prompt: ' + str(prompt) +'}'
  rospy.wait_for_service('get_response')
  try:
    get_response = rospy.ServiceProxy('get_response', Completion)
    response = get_response(request, 0)
    return response
  except rospy.ServiceException as e:
    print ("Service call failed: %s"%e)


if __name__ == "__main__":
  if len(sys.argv) == 2:
    prompt = str(sys.argv[1])
  else:
    prompt = "Write a poem about OpenAI"
  
  print("Prompt: %s\n" % (prompt))
  
  response = get_response_client(prompt)
  
  print("Response: \n%s\n" % (response))
  print("Text: %s\n" % (response.text))
