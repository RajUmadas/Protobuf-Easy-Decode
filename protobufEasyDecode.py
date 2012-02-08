#!/usr/bin/python

#This will use a lot of code from the google protobuf project
#to generate decoders for the most general of cases.

#Once I learn a bit more about the proto and the src base
#I should be able to just use the protobuf code base to 
#accomplise this task.

class ProtobufEasyDecode:
    
    WIRETYPE_VARINT = 0
    WIRETYOE_FIXED_64 = 1
    WIRETYPE_LENGTHDELIM = 2
    WIRETYPE_STARTGROUP = 3
    WIRETYPE_ENDGROUP = 4
    WIRETYPE_FIXED_32 = 5

    raw_message = ""
    decoded_message = {}

    def __init__(self,new_message):
        self.raw_message = new_message 
    
    def get_raw_message (self):
        return self.raw_message

    def decode_varint(self,buf,pos):
    #pass in buffer and starting position
    #return the int and the ending pos
        result
        shifts = 0
        while True:
            current_byte = ord(buf[pos])
            result = result | ((current_byte & 0x7f) << shifts)
            pos = pos + 1
            if not (current_byte & 0x80):
                return (result,pos)
            shifts = shifts + 7
    
    def decode_tag_header(self, tag_header):
        #returns tag_id, and tag_type
        return (tag_header >> 3, tag_header & 0x07)

    def decode_lenghtdelim (self, buf, pos)
    #pass in buffer and start pos
    #return bytes and ending pos
        length,pos = self.decode_varint(buf,pos)
        new_pos = pos + length
        return buf[pos:new_pos],new_pos


x = ProtobufEasyDecode("asdfasdfsadf")
print x
print x.get_raw_message()
