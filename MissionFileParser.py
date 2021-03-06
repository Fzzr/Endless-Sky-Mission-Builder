''' MissionFileParser.py
# Copyright (c) 2019 by Andrew Sneed
#
# Endless Sky Mission Builder is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# Endless Sky Mission Builder is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.

This takes the data read in from a mission file and stores it in each mission object

'''
#TODO: Add data validation, there are currently no checks to make sure it's not all junk data
import re, shlex

class MissionFileParser(object):
    def __init__(self, esmb):
        self.esmb     = esmb
        self.missions = esmb.missionList

        self.graveKeyPattern = re.compile(r'^ *(.*) (`.*`) *')
        self.logMessagePattern = re.compile(r'^ *')
    #end init

    def run(self):
        print("\nParsing Mission file...")

        for mission in self.missions:
            print("\tParsing mission: \"%s\"" % mission.missionName)
            lines = enumerate(mission.missionLines)
            for i, line in lines:
                line = line.rstrip()
                #print(i, line)
                tokens = self.tokenize(line)
                #print(tokens)

                # determine which attribute we've got
                if "mission" in tokens[0]:
                    continue
                elif "name" in tokens[0]:
                    print("\t\tFound mission display name: \"%s\"" % tokens[1])
                    mission.components.missionDisplayName = tokens[1]
                elif "description" in tokens[0]:
                    print("\t\tFound description: %s" % tokens[1])
                    mission.components.description = tokens[1]
                elif "blocked" in tokens[0]:
                    print("\t\tFound blocked: %s" % tokens[1])
                    mission.components.blocked = tokens[1]
                elif "deadline" in tokens[0]:
                    print("\t\tFound deadline")
                    mission.components.deadline.isDeadline = True
                    self.storeComponentData(mission.components.deadline.deadline, tokens[1:])
                elif "cargo" in tokens[0]:
                    print("\t\tFound cargo: %s" % tokens[1:])
                    mission.components.cargo.isCargo = True
                    self.storeComponentData(mission.components.cargo.cargoType, tokens[1:])
                elif "passengers" in tokens[0]:
                    print("\t\tFound passengers: %s" % tokens[1:])
                    mission.components.passengers.isPassengers = True
                    self.storeComponentData(mission.components.passengers.passengers, tokens[1:])
                elif "illegal" in tokens[0]:
                    print("\t\tFound illegal modifier: %s" % tokens[1:])
                    mission.components.illegal.isIllegal = True
                    self.storeComponentData(mission.components.illegal.illegal, tokens[1:])
                elif "stealth" in tokens[0]:
                    print("\t\tFound stealth modifier")
                    mission.components.isStealth = True
                elif "invisible" in tokens[0]:
                    print("\t\tFound invisible modifier")
                    mission.components.isInvisible = True
                elif tokens[0] in ["priority", "minor"]:
                    print("\t\tFound priority level")
                    mission.components.priorityLevel = tokens[0]
                elif tokens[0] in ["job", "landing", "assisting", "boarding"]:
                    print("\t\tFound where shown")
                    mission.components.whereShown = tokens[0]
                elif "repeat" in tokens[0]:
                    print("\t\tFound repeat")
                    mission.components.isRepeat = True
                    if len(tokens) > 1:
                        print("\t\t\tFound repeat optional data: %s" % tokens[1])
                        mission.components.repeat = tokens[1]
                elif "clearance" in tokens[0]:
                    print("\t\tFound clearance: %s" % tokens[1])
                    mission.components.clearance.isClearance = True
                    mission.components.clearance.clearance   = tokens[1]
                elif "infiltrating" in tokens[0]:
                    print("\t\tFound infiltrating")
                    mission.components.isInfiltrating = True
                elif "waypoint" in tokens[0]:
                    print("\t\tFound waypoint: %s" % tokens[1])
                    mission.components.waypoint = tokens[1]
                elif "stopover" in tokens[0]:
                    print("\t\tFound stopover: %s" % tokens[1])
                    mission.components.stopover.isStopover = True
                    mission.components.stopover.stopover   = tokens[1]
                elif "source" in tokens[0]:
                    print("\t\tFound source: %s" % tokens[1])
                    mission.components.source.isSource = True
                    mission.components.source.source   = tokens[1]
                elif "destination" in tokens[0]:
                    print("\t\tFound destination: %s" % tokens[1])
                    mission.components.destination.isDestination = True
                    mission.components.destination.destination   = tokens[1]
                elif "on" in tokens:
                    print("\t\tFound Trigger: on %s" % tokens[1])
                    trigger             = mission.addTrigger()
                    trigger.isActive    = True
                    trigger.triggerType = tokens[1]

                    cur = self.getIndentLevel(mission.missionLines[i])
                    nxt = self.getIndentLevel((mission.missionLines[i+1]))
                    while True:
                        if nxt <= cur:
                            break
                        i, line = lines.__next__()
                        line = line.rstrip()
                        tokens = self.tokenize(line)
                        #print(i, tokens)

                        # dialog
                        if "dialog" in tokens[0]:
                            print("\t\t\tFound Dialog: %s" % tokens[1])
                            trigger.dialog = tokens[1]
                        elif "outfit" in tokens[0]:
                            print("\t\t\tFound Outfit: %s" % tokens)
                            self.storeComponentData(trigger.outfit, tokens[1:])
                        elif "require" in tokens[0]:
                            print("\t\t\tFound Require: %s" % tokens)
                            self.storeComponentData(trigger.require, tokens[1:])
                        elif "payment" in tokens[0]:
                            print("\t\t\tFound Outfit: %s" % tokens)
                            trigger.isPayment = True
                            self.storeComponentData(trigger.payment, tokens[1:])
                        elif "event" in tokens[0]:
                            print("\t\t\tFound Event: %s" % tokens)
                            self.storeComponentData(trigger.event, tokens[1:])
                        elif "fail" in tokens[0]:
                            print("\t\t\tFound Event: %s" % tokens[1])
                            trigger.isFail = True
                            trigger.fail   = tokens[1]
                        elif "log" in tokens[0] and tokens[0] == "log":
                            print("\t\t\tFound Log: %s" % tokens)
                            newLog            = trigger.addLog()
                            newLog.isActive   = True
                            newLog.formatType = "<message>"
                            newLog.log[0]     = tokens[1]
                        elif "log" in tokens[0]:
                            print("\t\t\tFound Log: %s" % tokens)
                            newLog            = trigger.addLog()
                            newLog.isActive   = True
                            newLog.formatType = "<type> <name> <message>"

                            tokens2 = shlex.split(tokens[0])
                            tokens2.append(tokens[1])
                            self.storeComponentData(newLog.log, tokens2[1:])
                        elif tokens[1] in ["=", "+=", "-="]:
                            print("\t\t\tFound TriggerCondition: %s" % tokens)
                            newTC               = trigger.addTC()
                            newTC.isActive      = True
                            newTC.conditionType = 0
                            self.storeComponentData(newTC.condition, tokens)
                        elif tokens[1] in ["++", "--"]:
                            print("\t\t\tFound TriggerCondition: %s" % tokens)
                            newTC               = trigger.addTC()
                            newTC.isActive      = True
                            newTC.conditionType = 1
                            self.storeComponentData(newTC.condition, tokens)
                        elif tokens[0] in ["set", "clear"]:
                            print("\t\t\tFound TriggerCondition: %s" % tokens)
                            newTC               = trigger.addTC()
                            newTC.isActive      = True
                            newTC.conditionType = 2
                            self.storeComponentData(newTC.condition, tokens)
                        else:
                            print("Trigger component no found: ", i, line)
                        #end if else

                        try:
                            nxt = self.getIndentLevel(mission.missionLines[i+1])
                        except IndexError:
                            break

                    #end while
                else:
                    print("ERROR: No tokens found on line %d: %s" % (i, line))
                #end if/else
                for trigger in mission.components.triggerList:
                    trigger.printTrigger()
            #end for
            print("\tDone.")
        #end for
        print("File parsing complete.")
    #end run


    def tokenize(self, line):
        if '`' in line:
            #TODO: Fully implement this later, it's a ghetto-rigged POS
            #print(line)
            tokens = re.split(self.graveKeyPattern, line)
            tokens = tokens[1:3]
        else:
            tokens = shlex.split(line)
        #end if/else
        #print(tokens)
        return tokens
    #end tokenize


    def getIndentLevel(self, line):
        tabCount = len(line) - len(line.lstrip(' '))
        #print(tabCount)
        return tabCount
    #end getIndentLevel


    def storeComponentData(self, component, tokens):
        for i, token in enumerate(tokens):
            if token is not None:
                component[i] = token
            else:
                break
            # end if/else
        # end for
        #print(component)
    #end storeComponentData
#end class MissionFileParser