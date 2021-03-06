''' Mission.py
# Copyright (c) 2019 by Andrew Sneed
#
# Endless Sky Mission Builder is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# Endless Sky Mission Builder is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.


'''

import MissionComponents

class Mission(object):

    def __init__(self, missionName, default=False):
        print("Building mission:", missionName)

        self.components   = MissionComponents.MissionComponents()
        self.missionLines = []  # List of the mission text
        self.convoList    = []  # List of lists containing one
                                # conversation section per element

        if default is False:
            self.missionName  = missionName
        else:
            self.setDefaultValues(missionName)
        #end if/else

    #end init


    def setDefaultValues(self, missionName):
        self.missionName = missionName
        self.addLine("mission \"%s\"\n" % missionName)


    def addLine(self, line):
        self.missionLines.append(line + "\n")
    #end addLine


    def printMissionToConsole(self):
        print(self.missionLines)
    #end printMission


    def printMissionLinesToText(self):
        missionText = ""
        for line in self.missionLines:
            missionText+=str(line)
        return missionText
    #end printMissionLinesToText


    def parseMission(self):
        print("Parsing mission...", end="\t\t\t")
        self.missionLines = []          # empty the default values
        self.addLine("mission \"%s\"" % self.missionName)

        # mission display name
        if self.components.missionDisplayName is not None:
            self.addLine("\tname `%s`" % self.components.missionDisplayName)

        # description
        if self.components.description is not None:
            self.addLine("\tdescription `%s`" % self.components.description)

        # isBlocked
        if self.components.blocked is not None:
            self.addLine("\tblocked \"%s\"" % self.components.blocked)

        # deadline
        if self.components.deadline.isDeadline:
            line = "\tdeadline"
            if self.components.deadline.deadline[0] is not None:
                line = line + " " + self.components.deadline.deadline[0]
                if self.components.deadline.deadline[1] is not None:
                    line = line + " " + self.components.deadline.deadline[1]
                #end if
            #end if
            self.addLine(line)
        #end if

        # cargo
        if self.components.cargo.isCargo:
            line = "\tcargo"
            if self.components.cargo.cargoType[0] is "random":
                line = line + " random"
            else:
                line = line + " \"%s\"" % self.components.cargo.cargoType[0]
            #end if/else
            for part in self.components.cargo.cargoType[1:]:
                if part is not None:
                    line = line + " " + part
                else:
                    break
                #end if/else
            #end for
            self.addLine(line)
        #end if

        # passengers
        if self.components.passengers.isPassengers:
            line = "\tpassengers %s" % self.components.passengers.passengers[0]
            for part in self.components.passengers.passengers[1:]:
                if part is not None:
                    line = line + " " + part
                else:
                    break
                #end if/else
            #end for
            self.addLine(line)
        #end if

        # illegal
        if self.components.illegal.isIllegal:
            line = "\tillegal %s" % self.components.illegal.illegal[0]
            if self.components.illegal.illegal[1] is not None:
                line = line + " " + self.components.illegal.illegal[1]
            # end if
            self.addLine(line)
        #end if

        # stealth
        if self.components.isStealth:
            self.addLine("\tstealth")

        # isInvisible
        if self.components.isInvisible:
            self.addLine("\tinvisible")

        # priorityLevel
        if self.components.priorityLevel is not None:
            self.addLine("\t%s" % self.components.priorityLevel)

        # whereShown
        if self.components.whereShown is not None:
            self.addLine("\t%s" % self.components.whereShown)

        # repeat
        if self.components.isRepeat:
            line = "\trepeat"
            if self.components.repeat is not None:
                line = line + " " + self.components.repeat
            #end if
            self.addLine(line)
        #end if

        # clearance
        #TODO: fully implement this when filters are implemented
        if self.components.clearance.isClearance:
            self.addLine("\tclearance `%s`" % self.components.clearance.clearance)

        # isInfiltrating
        if self.components.isInfiltrating:
            self.addLine("\tinfiltrating")

        # waypoint
        if self.components.waypoint is not None:
            self.addLine("\twaypoint \"%s\"" % self.components.waypoint)

        # stopover
        #TODO: fully implement this when filters are implemented
        if self.components.stopover.isStopover:
            self.addLine("\tstopover \"%s\"" % self.components.stopover.stopover)

        # source
        #TODO: fully implement this when filters are implemented
        if self.components.source.isSource:
            self.addLine("\tsource \"%s\"" % self.components.source.source)

        # destination
        #TODO: fully implement this when filters are implemented
        if self.components.destination.isDestination:
            self.addLine("\tdestination \"%s\"" % self.components.destination.destination)

        # Trigger(s)
        for trigger in self.components.triggerList:
            if trigger.isActive:

                # triggerType
                if trigger.triggerType is not None:
                    self.addLine("\ton %s" % trigger.triggerType)

                # dialog
                if trigger.dialog is not None:
                    self.addLine("\t\tdialog `%s`" % trigger.dialog)

                # TODO: HANDLE CONVERSATIONS HERE

                # outfit
                if trigger.outfit[0] is not None:
                    line = "\t\toutfit "
                    line += self.addQuotes(trigger.outfit[0])
                    for data in trigger.outfit[1:]:
                        if data is None:
                            break
                        line = line + " " + data
                    #end for
                    self.addLine(line)
                #end if

                # request
                if trigger.require[0] is not None:
                    line = "\t\trequire "
                    line += self.addQuotes(trigger.require[0])
                    for data in trigger.require[1:]:
                        if data is None:
                            break
                        line = line + " " + data
                    # end for
                    self.addLine(line)
                # end if

                # payment
                if trigger.isPayment:
                    line = "\t\tpayment"
                    for data in trigger.payment:
                        if data is None:
                            break
                        line = line + " " + data
                    # end for
                    self.addLine(line)
                # end if

                # Conditions
                for condition in trigger.conditions:
                    if condition.isActive:
                        if condition.conditionType == 0:
                            self.addLine("\t\t\"%s\" %s %s" % (condition.condition[0], condition.condition[1], condition.condition[2]))
                        elif condition.conditionType == 1:
                            self.addLine("\t\t\"%s\" %s" % (condition.condition[0], condition.condition[1]))
                        elif condition.conditionType == 2:
                            self.addLine("\t\t%s \"%s\"" % (condition.condition[0], condition.condition[1]))
                        else:
                            print("Data corrupted!")
                        # end if/else
                    # end if
                # end for

                # event
                if trigger.event[0] is not None:
                    line = "\t\tevent "
                    line += self.addQuotes(trigger.event[0])
                    for data in trigger.event[1:]:
                        if data is None:
                            break
                        line = line + " " + data
                    # end for
                    self.addLine(line)
                # end if

                # fail
                if trigger.isFail:
                    line = "\t\tfail "
                    if trigger.fail is not None:
                        line += self.addQuotes(trigger.fail)
                    # end if
                    self.addLine(line)
                #end if

                # Logs
                for log in trigger.logs:
                    if log.isActive:
                        line = "\t\tlog"
                        if log.formatType == "<message>":
                            self.addLine("%s `%s`" % (line, log.log[0]))
                            continue
                        #end if
                        self.addLine("%s \"%s\" \"%s\" `%s`" % (line, log.log[0], log.log[1], log.log[2]))
                    #end if
                #end for

            #end if
        #end for

        print("Done.")
    #end parseMission


    def addTrigger(self):
        newTrigger = MissionComponents.Trigger()
        self.components.triggerList.append(newTrigger)
        return newTrigger
    #end addTrigger


    def removeTrigger(self, trigger):
        #print(trigger)
        self.components.triggerList.remove(trigger)
    #end removeTrigger


    def addQuotes(self, line):
        if " " in line:
            line = "\"%s\"" % line
        return line
    #end addQuotes

#end class Mission