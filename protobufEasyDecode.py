#!/usr/bin/python

#This will use a lot of code from the google protobuf project
#to generate decoders for the most general of cases.

#Once I learn a bit more about the proto and the src base
#I should be able to just use the protobuf code base to 
#accomplise this task.

class ProtobufEasyDecode:
    raw_message = ""

    def __init__(self,new_message):
        self.raw_message = new_message 
    
    def get_raw_message (self):
        return self.raw_message

x = ProtobufEasyDecode("asdfasdfsadf")
print x
print x.get_raw_message()
