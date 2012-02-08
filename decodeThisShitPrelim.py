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

def genDecodeProtoBuff(protoBin, indentLevel = 0):
    allsGood = True
    while allsGood:
        if len(protoBin) == 0:
            return 1
        currentTagInt,pos = getVarintPos(protoBin)
        protoBin = protoBin[pos:]
        currentTag,currentType = getTagType(currentTagInt)
        if currentType == TYPE_LENGTHDELIM:
            data,pos = getLengthdelimPos(protoBin)
            protoBin = protoBin[pos:]
            print "    " * indentLevel + "Current Tag: " + str(currentTag)
            print "    " * indentLevel + "Current Type: " + getTypeName(currentType)
            print "    " * indentLevel + "Current Data: " + data
            print "    " * indentLevel + "Current Data Hex: " + binascii.hexlify(data)
            print "    " * indentLevel + "*******Digging In**********"
            genDecodeProtoBuff(data, indentLevel + 1)
            print "    " * indentLevel + "***************************"
        elif currentType == TYPE_VARINT:
            data,pos = getVarintPos(protoBin)
            protoBin = protoBin[pos:]
            print "    " * indentLevel + "Current Tag: " + str(currentTag)
            print "    " * indentLevel + "Current Type: " + getTypeName(currentType)
            print "    " * indentLevel + "Current Data: " + str(data)
        else:
            print "    " * indentLevel + "OMFG:" + str(currentType) + " " + getTypeName(currentType)
            allsGood = False


protoBin = binascii.unhexlify(sys.argv[1])


    
genDecodeProtoBuff(protoBin) 
