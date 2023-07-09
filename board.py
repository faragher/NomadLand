#!/bin/python3
print("#!c=0")
import time
import os
import RNS.vendor.umsgpack as msgpack
from datetime import datetime
import pickle


class MessageBoard:
  def __init__(self, Name):
    self.name = Name
    self.members = False
    self.private = False
    self.topics = []
    self.bigot = []
    self.description = "Undefined Board"

  def add(self, Topic):
    self.topics.append(Topic)

class Topic:
  def __init__(self,User,Title):
    buffer = Title.replace("`=","")
    buffer = "`="+buffer+"`="
    self.title = Title
    self.messages = []
    self.last_time = "No Data"
    self.deleted = False
    self.creator = User[-8:]
    self.creatoraddress = User

  def add(self,Message):
    self.messages.append(Message)
    self.last_time = datetime.now().strftime("%H%M/%d%b%Y")

class Message:
  def __init__(self, User, Payload):
    self.user = User
    self.callsign = User[-8:]
    self.time = datetime.now().strftime("<%H%M/%d%b%Y>")
    self.deleted = False
    buffer = Payload.replace("`=","")
    buffer = "`="+buffer+"`="
    self.text = buffer

#Debug Dummy Database
DebugAddy = "f5a7233c612acb393f1c273b5b0366bc"
#DDD = []
#DD = MessageBoard("Debug Board")
#DD.add(Topic(DebugAddy,"DebugTopic"))
#DD.topics[0].creator = DebugAddy
#DD.topics[0].add(Message(DebugAddy,"Debug Message"))
#DD.add(Topic(DebugAddy,"DeletedTopic"))
#for M in range(20):
#  DD.topics[0].add(Message(DebugAddy,"Message "+str(M)))
#DD.topics[0].messages[5].deleted = True
#DD.topics[1].add(Message(DebugAddy,"Deleted Message"))
#DD.topics[1].deleted = True
#DDD.append(DD)
#DE = MessageBoard("Members Only Board")
#DE.members = True
#DDD.append(DE)
#DF = MessageBoard("Private Board")
#DF.private = True
#DF.bigot.append("a22c2e8486a168a3b762d5a4b76a454f")
#DDD.append(DF)

#End Debug


isAuthed = False
#message_board_peer = 'please_replace'
message_board_name = "Between the Borders NomadLand Board"
sysop_address = "f5a7233c612acb393f1c273b5b0366bc"
board_directory = "nomadland"
board_base_url = "board2.mu"
env_string = []
userdir = os.path.expanduser("~")
callsign = "Unidentified"
interest = None
TargetBoard = -1
TargetTopic = -1
MessageIndex = 0
MessageEndIndex = 0
MessagePerPage = 10

if os.path.isdir("/etc/"+board_directory) and os.path.isfile("/etc/"+board_directory+"/config"):
    configdir = "/etc/"+board_directory
else:
    configdir = userdir+"/."+board_directory

storagepath  = configdir+"/storage"
if not os.path.isdir(storagepath):
    os.makedirs(storagepath)

boardpath = storagepath+"/boarddb"
if os.path.isfile(boardpath):
    f = open(boardpath, "rb")
#    board_contents = msgpack.unpack(f)
    BoardDB = pickle.load(f)
    f.close()
#    board_contents.reverse()
#     pass
else:
    print("Board is uninitialized")
    print("Generating default boards")
    # Change these for custom initialization
    BoardDB = []
    DD = MessageBoard("General")
    DD.description = "Publicly viewable message board for general discussion and information."
    BoardDB.append(DD)
    DE = MessageBoard("Greatroom")
    DE.description = "A general gathering space and discussion area that requies users be authenticated prior to viewing."
    DE.members = True
    BoardDB.append(DE)
    DF = MessageBoard("Operations")
    DF.description="Private: For message board operations"
    DF.private = True
    DF.bigot.append("a22c2e8486a168a3b762d5a4b76a454f")
    DF.bigot.append("f5a7233c612acb393f1c273b5b0366bc")
    BoardDB.append(DF)
    f = open(boardpath, "wb")
    f.write(pickle.dumps(BoardDB))
    f.close()



ID_hex = None
for e in os.environ:
#  print(e+", "+os.environ[e])
  if e == "remote_identity":
    ID_hex = os.environ[e]
    isAuthed = True
  if e == "var_interest":
    interest = os.environ[e]
    if interest == "None":
      interes = None
  if e == "var_TargetBoard":
#    print("Found var_TargetBoard "+os.environ[e])
    TargetBoard = int(os.environ[e])
#    print("Set TargetBoard "+str(TargetBoard))
  if e == "var_TargetTopic":
    TargetTopic = int(os.environ[e])
  if e == "var_MessageIndex":
    MessageIndex = int(os.environ[e])
  if e == "field_messagepayload":
    MessagePayload = os.environ[e]

print("`r"+datetime.now().strftime("%H:%M/%d%b%Y"))


if ID_hex == None:
  print("You are not identified. Board is Read-Only")
  print("`a")
else:
  callsign = ID_hex[-8:]
  print("Identified as "+callsign)
  print("`a")


MOTD = "This board is in active development and will break, add features, and lose data randomly. You have been warned."
print("`!`F222`Bddd")
print('-')
print('`c'+message_board_name)
print('-')
print('`a`b`f')
print("")

#print("`b`[Evil Broken Test Link`:/page/board2.mu`TargetBoard=3|interest=Topics]")


#print("To add a message to the board just converse with the NomadNet Message Board at `[lxmf@{}]".format(message_board_peer))
#time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
#print("Last Updated: {}".format(time_string))

#debug

# Display boards
if interest==None or interest == "None":
  print("MOTD: "+MOTD)
  print("``")
  print(" ")
  print("    Be sure to read the notices.")
  i=-1
  for BDB in BoardDB:
    isBoardAuthed=True
    i=i+1
    if(BDB.members and not isAuthed):
      isBoardAuthed = False
    if(BDB.private):
      if(isAuthed):
        Token = ID_hex
      else:
        Token = "Invalid"
      if(not Token in BDB.bigot):
        isBoardAuthed = False
    if isBoardAuthed:
      print(" ")
      print("``")
      print("`Ffb0`["+BDB.name+"`:/page/"+board_base_url+"`TargetBoard="+str(i)+"|interest=Topics]`f")
      print("``    "+BDB.description)
      print("``")

# Display Topics
if interest == "Topics":
  if TargetBoard < 0 or TargetBoard > len(BoardDB)-1:
    print("`Ff00Error: Attempted to view topics without a valid board`f")
  else:
    isBoardAuthed=True
    if(BoardDB[TargetBoard].members and not isAuthed):
      isBoardAuthed = False
    if(BoardDB[TargetBoard].private):
      if(isAuthed):
        Token = ID_hex
      else:
        Token = "Invalid"
      if(not Token in BoardDB[TargetBoard].bigot):
        isBoardAuthed = False
    if isBoardAuthed:
      i = -1
      for TP in BoardDB[TargetBoard].topics:
        i = i+1
        if not TP.deleted:
#          print(TP.title+" -- "+TP.creator)
          print("`Ffb0`b`["+TP.title+"`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+str(i)+"|interest=Messages] -- `["+TP.creator+"`lxmf@"+TP.creatoraddress+"`f`]")
          print("  Last activity: "+TP.last_time)
#          print("-")
#          for M in TP.messages:
#            print('`=')
#            print(M.text)
#            print('`=')
#            print("`r"+M.user+M.time)
#            print("`a")
#            print("-")
    else:
      print("`Ff00You are not authorized to view this board`f")
    if isAuthed:
      print("Add Topic")
      print("`B333`<30|messagepayload`>")
      print("``")
      print("Maximum length 60 chars")
      print("`r`Ffb0`[POST`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|messagepayload|interest=NewTopic]`f")
    print("``")
    print(" ")
    print("-")
    print("`Ffb0`[<<Board`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|interest=None]`f")


# Display Messages
if interest == "Messages":
  if TargetBoard < 0 or TargetBoard > len(BoardDB)-1:
    print("Error: Attempted to view topics without a valid board")
  elif TargetTopic < 0 or TargetTopic > len(BoardDB[TargetBoard].topics):
    print("Error: Attempted to view a non-existent topic")
  else:
    isBoardAuthed=True
    if(BoardDB[TargetBoard].members and not isAuthed):
      isBoardAuthed = False
    if(BoardDB[TargetBoard].private):
      if(isAuthed):
        Token = ID_hex
      else:
        Token = "Invalid"
      if(not Token in BoardDB[TargetBoard].bigot):
        isBoardAuthed = False
    if isBoardAuthed:
      TP = BoardDB[TargetBoard].topics[TargetTopic]
      print(TP.title)
      print("-")
      currentindex = MessageIndex
      displayedmessages = 0
      doMessages = True
      if len(TP.messages)>0:
        while doMessages and currentindex >= 0:
#        for M in TP.messages:
#          print('`=')
          M = TP.messages[currentindex]
          if not M.deleted:
            print(M.text)
#            print('`=')
            print("`r`["+M.callsign+"`lxmf@"+M.user+"`]"+M.time)
            print("`a")
            print("-")
            displayedmessages = displayedmessages+1
          currentindex = currentindex+1
          if currentindex == len(TP.messages):
            doMessages = False
            MessageEndIndex = currentindex
          if displayedmessages > 9:
            doMessages = False
            MessageEndIndex = currentindex
          if currentindex > 1000:
            doMessages = False
            print("Error, exceeded 1,000 messages in thread. Infinite loop? Terminating.")
#      print("`rNext>>")
      #DebugIf
      if isAuthed:
        print("Post Reply")
        print("`B333`<30|messagepayload`>")
        print("``")
        print("Maximum length, 25 lines (750 chars)")
        print("`r`Ffb0`[POST`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+str(TargetTopic)+"|messagepayload|interest=Posting]`f")
        print(" ")
        print("``")


      #endif
      if MessageEndIndex < len(TP.messages):
        print("`r`Ffb0`[NEXT>>`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+str(TargetTopic)+"|MessageIndex="+str(MessageEndIndex)+"|interest=Messages]`f")
      print("``")
      print("`[`Ffb0<<"+BoardDB[TargetBoard].name+"`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+str(TargetTopic)+"|interest=Topics]`f")
      print("`[`Ffb0<<Board`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|interest=None]`f")

    else:
      print("`Ff00You are not authorized to view this board`f")

if interest == "Posting":
  if not isAuthed:
    print("`Ff00You are not authorized to post.`f")
  else:
    if len(MessagePayload) > 750:
      MessagePayload = MessagePayload[:750]+"`Ff00<Message Truncated>`f"
    print(MessagePayload)
    BoardDB[TargetBoard].topics[TargetTopic].add(Message(ID_hex,MessagePayload))
    f = open(boardpath, "wb")
    f.write(pickle.dumps(BoardDB))
    f.close()
    print("`Ffb0`c`[<<GO>>`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+str(TargetTopic)+"|interest=Messages]`f")
    print("``")

if interest == "NewTopic":
  if not isAuthed:
    print("`Ff00You are not authorized to post.`f")
  else:
    if len(MessagePayload) > 60:
      MessagePayload = MessagePayload[:60]+"`Ff00<Message Truncated>`f"
    print(MessagePayload)
    BoardDB[TargetBoard].add(Topic(ID_hex,MessagePayload))
    f = open(boardpath, "wb")
    f.write(pickle.dumps(BoardDB))
    f.close()
    print("`Ffb0`c`[<<GO>>`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"interest=Topics]`f")
    print("``")


# General Footer
print(" ")
print(" ")
print("`Ffb0`[Notices`:/page/notices.mu`]`f")
if sysop_address != "":
	print("`Ffb0`[SYSOP`lxmf@"+sysop_address+"`]`f")


#end debug


