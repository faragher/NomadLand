#!/bin/python3
print("#!c=0")
import time
import os
from datetime import datetime
import RNS
import sqlite3



    
def San(p):
  p=p.replace("`=","")
  p=p.replace("`","")
  return p
  
  # General Footer
def Footer():
  print(" ")
  print(" ")
  print("`Ffb0`[Home`:/page/board.mu`]`f")
  print("`Ffb0`[Notices`:/page/notices.mu`]`f")
  if sysop_address != "":
    print("`Ffb0`[SYSOP`lxmf@"+sysop_address+"`]`f")





isAuthed = False
isAdmin = False
message_board_name = "Between the Borders NomadLand Board"
sysop_address = "f5a7233c612acb393f1c273b5b0366bc"
sysop_ident =   "3de97d02f70f67612bcbfc2d32fa7da2"
board_directory = "nomadland"
board_base_url = "board.mu"
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

#boardpath = storagepath+"/boarddb"
databasepath = storagepath+"/pages.db"

#print(storagepath)

if os.path.isfile(databasepath):
    pass
else:
    print("Board is uninitialized")
    import configparser
    configfile = configparser.ConfigParser()
    confforumname = "Incorrectly Configured Forum"
    confadminhash = ""
    confsysophash = ""
    confmotd = "Please check your configuration and reinitialize the database!"
    if os.path.isfile(storagepath+"/Config.ini"):
        configfile.read(storagepath+"/Config.ini")
        confforumname = configfile['Forum']['ForumName']
        confadminhash = configfile['Forum']['ForumAdmin']
        confsysophash = configfile['Forum']['ForumSysop']
        confmotd = configfile['Forum']['MOTD']
        
    conn = sqlite3.connect(databasepath)
    cur = conn.cursor()
    query = "CREATE TABLE config (forumname TEXT, adminhash TEXT, sysophash TEXT, motd TEXT)"
    cur.execute(query)
    query = "CREATE TABLE boards (name TEXT, description TEXT, class TEXT, bigot TEXT, deleted INT)"
    cur.execute(query)
    #<-- YOU ARE HERE
    cur.execute("INSERT INTO config (forumname, adminhash, sysophash, motd) VALUES (?,?,?,?)",(confforumname,confadminhash,confsysophash,confmotd))
    conn.commit()

    print("Board Config loaded")
    if os.path.isfile(storagepath+"/Config.ini"):
      configfile.read(storagepath+"/Config.ini")
      #print("Board stuff")
      boardlist = configfile['Boards']['Names'].split(",")
      desclist = configfile['Boards']['Descriptions'].split(",")
      classlist = configfile['Boards']['Class'].split(",")
      bigotlist = configfile['Boards']['Bigot'].split(",")
      deletedlist = configfile['Boards']['Deleted'].split(",")
      for i in range(len(boardlist)):
        bName = boardlist[i]
        bDesc = desclist[i]
        bClass = classlist[i]
        bBigot = bigotlist[i]
        bDeleted = deletedlist[i]
        cur.execute("INSERT INTO boards (name, description, class, bigot, deleted) VALUES (?,?,?,?,?)",(bName,bDesc,bClass,bBigot,bDeleted))
        query = "CREATE TABLE boards"+bName.replace("'","''")+" (title TEXT, hash TEXT, creator TEXT, creatoraddress TEXT, timestamp TEXT, deleted INT)"
        cur.execute(query)
        query = "CREATE TABLE messages"+bName.replace("'","''")+" (message TEXT, topichash TEXT, creator TEXT, creatoraddress TEXT, timestamp TEXT, deleted INT)"
        cur.execute(query)
        
    conn.commit()
    
    
    print("Boards generated")
    conn.close()



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
    TargetBoard = os.environ[e]
  if e == "var_TargetTopic":
    TargetTopic = os.environ[e]
  if e == "var_TargetMessage":
    TargetMessage = int(os.environ[e])
  if e == "var_MessageIndex":
    MessageIndex = int(os.environ[e])
  if e == "field_messagepayload":
    MessagePayload = os.environ[e]
    
if ID_hex != None:
  if ID_hex == sysop_ident:
    isAdmin = True

print("`r"+datetime.now().strftime("%H:%M/%d%b%Y"))


if ID_hex == None:
  print("You are not identified. Board is Read-Only")
  print("`a")
else:
  callsign = ID_hex[-8:]
  print("Identified as "+callsign)
  if isAdmin:
    print("ADMINISTRATOR")
  print("`a")


MOTD = "This board is in active development and will break, add features, and lose data randomly. You have been warned."
print("`!`F222`Bddd")
print('-')
print('`c'+message_board_name)
print('-')
print('`a`b`f')
print("")



# Display boards
if interest==None or interest == "None":
  print("MOTD: "+MOTD)
  print("``")
  print(" ")
  print("    Be sure to read the notices.")
  i=-1
  conn = sqlite3.connect(databasepath)
  cur = conn.cursor()
  query = "SELECT name, description, class, bigot, deleted FROM boards"
  cur.execute(query)
  result = cur.fetchall()

  for b in result:
    bName = b[0].replace("'","''")
    bDesc = b[1].replace("'","''")
    bClass = b[2]
    bBigot = b[3].split("|")
    bDeleted = b[4]
    isBoardAuthed=True
    i=i+1
    if(bClass == "Members" and not isAuthed):
      isBoardAuthed = False
    if(bClass == "Private"):
      if(isAuthed):
        Token = ID_hex
      else:
        Token = "Invalid"
      if(not Token in bBigot):
        isBoardAuthed = False
    if bDeleted:
      isBoardAuthed = False
    if isBoardAuthed:
      print(" ")
      print("``")
      print("`Ffb0`["+bName+"`:/page/"+board_base_url+"`TargetBoard="+str(b[0])+"|interest=Topics]`f")
      print("``    "+bDesc)
      print("``")

# Display Topics
if interest == "Topics":
  conn = sqlite3.connect(databasepath)
  cur = conn.cursor()
  query = "SELECT title, hash, creator, creatoraddress, timestamp, deleted FROM boards"+TargetBoard+" WHERE deleted = '0' ORDER BY timestamp DESC"
  cur.execute(query)
  results = cur.fetchall()
  query = "SELECT class, bigot FROM boards WHERE name ='"+TargetBoard+"'"
  cur.execute(query)
  boarddata = cur.fetchone()
  if len(results) == 0:
    print("`Ff00Error: Board is empty!`f")
  isBoardAuthed=True
  if(boarddata[0] == "Members" and not isAuthed):
    isBoardAuthed = False
  if(boarddata[0] == "Private"):
    if(isAuthed):
      Token = ID_hex
    else:
      Token = "Invalid"
    if(not Token in boarddata[1].split("|")):
      isBoardAuthed = False
    if isAdmin:
      isBoardAuthed = True
  if isBoardAuthed:
      for R in results:
            print("``")
            print("`Ffb0`b`["+San(R[0])+"`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+R[1]+"|interest=Messages]`f -- `["+R[3][-8:]+"`lxmf@"+R[3]+"`]")
            print("  Last activity: "+datetime.fromtimestamp(float(R[4])).strftime("%H%M/%d%b%Y"))
            print(" ")
            if isAdmin:
              print("`Ff00`[DELETE`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+R[1]+"|interest=DeleteTopic]`f")

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
  conn = sqlite3.connect(databasepath)
  cur = conn.cursor()
  query = "SELECT class, bigot FROM boards WHERE name ='"+TargetBoard+"'"
  cur.execute(query)
  boarddata = cur.fetchone()
  query = "SELECT title FROM boards"+TargetBoard+" WHERE hash = '"+TargetTopic+"'"
  cur.execute(query)
  topicdata = cur.fetchone()
  #message TEXT, topichash TEXT, creator TEXT, creatoraddress TEXT, timestamp TEXT, deleted INT
  query = "SELECT COUNT(*) FROM messages"+TargetBoard+" WHERE topichash ='"+TargetTopic+"' and deleted = '0'"
  cur.execute(query)
  messagecount = cur.fetchall()[0][0]
  
  query = "SELECT message, creator, creatoraddress, timestamp FROM messages"+TargetBoard+" WHERE topichash ='"+TargetTopic+"' and deleted = '0' ORDER BY timestamp ASC LIMIT 10 OFFSET "+str(MessageIndex)
  cur.execute(query)
  results = cur.fetchall()
  if len(results) == 0:
    print("`Ff00Error: Topic is empty!`f")
  isBoardAuthed=True
  if(boarddata[0] == "Members" and not isAuthed):
    isBoardAuthed = False
  if(boarddata[0] == "Private"):
    if(isAuthed):
      Token = ID_hex
    else:
      Token = "Invalid"
    if(not Token in boarddata[1].split("|")):
      isBoardAuthed = False
    if isAdmin:
      isBoardAuthed = True
  if isBoardAuthed:
    print("``")
    print(San(topicdata[0]))
    print("-")
    #currentindex = MessageIndex
    #displayedmessages = 0
    #doMessages = True
    #if len(TP.messages)>0:
    #  while doMessages and currentindex >= 0:
    for M in results:
      print(San(M[0])) 
      print("`r`["+M[2][-8:]+"`lxmf@"+M[2]+"`]"+datetime.fromtimestamp(float(M[3])).strftime("<%H%M/%d%b%Y>"))
      print("`a")
      if isAdmin:
        print("`Ff00`[DELETE`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+str(TargetTopic)+"|TargetMessage="+str(currentindex)+"|interest=DeleteMessage]`f")
      print("-")
    if isAuthed:
      print("Post Reply")
      print("`B333`<30|messagepayload`>")
      print("``")
      print("Maximum length, 25 lines (750 chars)")
      print("`r`Ffb0`[POST`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+str(TargetTopic)+"|messagepayload|interest=Posting]`f")
      print(" ")
      print("``")


      #endif
    if (MessageIndex + 10 < messagecount):
      print("`r`Ffb0`[NEXT>>`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+str(TargetTopic)+"|MessageIndex="+str(MessageIndex+10)+"|interest=Messages]`f")
    if (MessageIndex > 0):
      print("`a`Ffb0`[<<BACK`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+str(TargetTopic)+"|MessageIndex="+str(MessageIndex-10)+"|interest=Messages]`f")

    print("``")
    print("`[`Ffb0<<"+topicdata[0]+"`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+str(TargetTopic)+"|interest=Topics]`f")
    print("`[`Ffb0<<Board`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|interest=None]`f")

  else:
    print("`Ff00You are not authorized to view this board`f")

if interest == "Posting":
  if not isAuthed:
    print("`Ff00You are not authorized to post.`f")
  else:
    if len(MessagePayload) > 750:
      MessagePayload = MessagePayload[:750]+"`Ff00<Message Truncated>`f"
    conn = sqlite3.connect(databasepath)
    cur = conn.cursor()
    print(San(MessagePayload))
    MessagePayload = MessagePayload.replace("'","''")
    identity_hash = bytes.fromhex(ID_hex)
    ID = RNS.Destination.hash_from_name_and_identity("lxmf.delivery",identity_hash)
    LXMF_hex = RNS.prettyhexrep(ID)
    LXMF_hex = LXMF_hex.replace("<","")
    LXMF_hex = LXMF_hex.replace(">","")
    query = "INSERT INTO messages"+TargetBoard.replace("'","''")+" (message, topichash, creator, creatoraddress, timestamp, deleted) values ('"+MessagePayload+"','"+TargetTopic+"','"+ID_hex+"','"+LXMF_hex+"','"+str(datetime.now().timestamp())+"',0)"
    cur.execute(query)
    conn.commit()
    print("`Ffb0`c`[<<GO>>`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"|TargetTopic="+str(TargetTopic)+"|interest=Messages]`f")
    print("``")
    conn.commit()

if interest == "NewTopic":
  if not isAuthed:
    print("`Ff00You are not authorized to post.`f")
  else:
    if len(MessagePayload) > 60:
      MessagePayload = MessagePayload[:60]+"`Ff00<Message Truncated>`f"
    print(MessagePayload)
    MessagePayload = San(MessagePayload)
    conn = sqlite3.connect(databasepath)
    cur = conn.cursor()
    identity_hash = bytes.fromhex(ID_hex)
    TopicHash = RNS.prettyhexrep(RNS.Cryptography.sha256((ID_hex+str(datetime.now())+MessagePayload).encode("UTF-8")))	
#    print(TopicHash)
    ID = RNS.Destination.hash_from_name_and_identity("lxmf.delivery",identity_hash)
    LXMF_hex = RNS.prettyhexrep(ID)
    LXMF_hex = LXMF_hex.replace("<","")
    LXMF_hex = LXMF_hex.replace(">","")
    query = "INSERT INTO boards"+TargetBoard.replace("'","''")+" (title, hash, creator, creatoraddress, timestamp, deleted) VALUES ('"+MessagePayload+"','"+str(TopicHash)+"','"+ID_hex+"','"+LXMF_hex+"','"+str(datetime.now().timestamp())+"','0')"
    print(query)
    cur.execute(query)
    #f = open(boardpath, "wb")
    #f.write(pickle.dumps(BoardDB))
    #f.close()
    print("`Ffb0`c`[<<GO>>`:/page/"+board_base_url+"`TargetBoard="+str(TargetBoard)+"interest=Topics]`f")
    print("``")
    conn.commit()
    
if interest == "DeleteTopic":
  if isAdmin:
    BoardDB[TargetBoard].topics[TargetTopic].deleted=True
    #f = open(boardpath, "wb")
    #f.write(pickle.dumps(BoardDB))
    #f.close()
    print("Done")
  else:
    print("Unauthorized")
    
if interest == "DeleteMessage":
  if isAdmin:
    BoardDB[TargetBoard].topics[TargetTopic].messages[TargetMessage].deleted=True
    #f = open(boardpath, "wb")
    #f.write(pickle.dumps(BoardDB))
    #f.close()
    print("Done")
  else:
    print("Unauthorized")


Footer()


#end debug


