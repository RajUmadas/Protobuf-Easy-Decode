#!/usr/bin/python

import binascii
import sys
import struct

TYPE_VARINT = 0
TYPE_64 = 1
TYPE_LENGTHDELIM = 2
TYPE_STARTGROUP = 3
TYPE_ENDGROUP = 4
TYPE_32 = 5


def getVarintPos(stream):
    result = 0
    shifts = 0
    pos = 1
    for i in stream:
        result = result | ((ord(i)&0x7f) << shifts)
        if not (ord(i)&0x80):
            return result,pos
        shifts = shifts+7
        pos = pos+1

def getLengthdelimPos(stream):
    length,pos = getVarintPos(stream)
    stream = stream[pos:]
    string = stream[0:length]
    return string,pos+length

def getTagType(i):
    return (i>>3,i&0x07)

def getTypeName(i):
    if i == TYPE_VARINT:
        return "varint"
    elif i == TYPE_64:
        return "64 bit"
    elif i == TYPE_LENGTHDELIM:
        return "length delim"
    elif i == TYPE_32:
        return "32 bit"
    else:
        return "WTF"

def genDecodeProtoBuff(protoBin):
    allsGood = True
    theProtos =  {}
    while allsGood:
        if len(protoBin) == 0:
            return theProtos
        currentTagInt,pos = getVarintPos(protoBin)
        protoBin = protoBin[pos:]
        currentTag,currentType = getTagType(currentTagInt)
        if currentType == TYPE_LENGTHDELIM:
            data,pos = getLengthdelimPos(protoBin)
            protoBin = protoBin[pos:]
            
            theProtos[currentTag]=(currentType,data,genDecodeProtoBuff(data))
        elif currentType == TYPE_VARINT:
            data,pos = getVarintPos(protoBin)
            protoBin = protoBin[pos:]
            theProtos[currentTag]=(currentType,data,0)
        else:
            allsGood = False
    return theProtos

protoBin = binascii.unhexlify(sys.argv[1])    
print genDecodeProtoBuff(protoBin) 
