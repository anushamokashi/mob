def parseEventsIntoMap(lines):
    event_dest={}
    statement_List =[]
    key =""
    event_obj = ""
    print "WITH IN parseEventsIntoMap"
    print "^^lines^^"
    print lines
    print "-----"
    
    if lines:
		splited_lines = string.split(lines, '\n')
		#splited_lines = string.split(lines, '\r')
		print "SPLITED_LINES N^^"
		print splited_lines
		print "-----"
		for line in splited_lines:
			statement_List =[]
			if line:
				if line[0]=='{':
					key = str(line)
					print "KEY"
					print key
					print "-----"
					
					if not event_dest.has_key(str(key)):
						event_dest[key] = statement_List
					else:
						if key:
							statement_List = event_dest.get(key)
						if not statement_List:
							statement_List.append(str(line))
						else:
							statement_List.append(str(line))
		event_obj = adjustEvents(event_dest) 
		print "EVENT_OBJ" 
		print event_obj
		print "-----"              
    return event_obj

def adjustEvents(event_dest):
    adjustedEventdest = {}
    subEventdest = {}
    tempdest = {}
    
    for eventKey,eventVal in event_dest.iteritems():
        eventSign = [] 
        eventSign = getEventAndArguments(eventKey)
        print "EVENTSIGN"
        print eventSign
        print "-----"
        print eventSign.__len__()
        if eventSign.__len__() > 1:
                eventName = str(eventSign[0].lower())
                arg1 = eventSign[1].lower()
                print '###'
		print "ARG1"
		print arg1
		print '-----'
                if not adjustedEventdest.has_key(eventName):
                        subEventdest = {}
                        if arg1:
                                subEventdest[arg1]= eventVal
                        else:
                                subEventdest["COMPEVENT"]= eventVal
                        adjustedEventdest[eventName]=subEventdest
                else:
                        tempdest =  adjustedEventdest.get(eventName)
                        tempdest[arg1]=eventVal
        elif eventSign.__len__() == 1:
                eventName = str(eventSign[0].lower())
                arg1 = "COMPEVENT"
                subEventdest = {}
                subEventdest[arg1]= eventVal
                adjustedEventdest[eventName] = subEventdest
                #print adjustedEventdest
    return adjustedEventdest

def getEventAndArguments(strLine):

        firstWord = ""
        restOfString = ""

        rpStrLine = strLine.replace("{", "").replace("}", "")

        temp = rpStrLine.split(" ")
       
        firstWord = temp[0]

        
        for index in range(len(temp)):
            if index != 0:
                restOfString += temp[index]
                restOfString += " "
        

        if len(restOfString) == 0:
            re = []
            re.append(firstWord)
            return re;
        else:
           alter = restOfString;
           re = []
           re.append(firstWord.strip())
           re.append(alter.strip())
           return re;