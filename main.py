import math
fullGauge = 10000
combatantsDict = {}
currentTurn = None

# Syntax library for commands
commandSyntax = {
    "create": "create [name] [base speed] [current speed]",
    "inspect": "inspect [name]",
    "progress": "progress",
    "advance": "advance [name] [amount (percent)]",
    "delay": "delay [name] [amount (percent)]",
    "speedup": "speedup [name] [amount (percent or flat)] [duration (turns)]",
    "slow": "slow [name] [amount (percent or flat)] [duration (turns)]",
    "exit": ""
}

# Prints the syntax for attempted command
def syntax(name):
    print(f"syntax for {name[0]}: " + commandSyntax[name[0]])

# Class for combatants that are created
class Combatant:
    def __init__(self, name, baseSpeed, currentSpeed):
        # Basic stats and such
        self.name = name
        self.baseSpeed = baseSpeed
        self.currentSpeed = currentSpeed
        self.gauge = fullGauge
        self.dead = False
        self.AV = fullGauge/currentSpeed
        #Lists of lists
        #[[amount, turnsLeft], [amount, turnsLeft]]
        self.speedBuffs = []
        self.speedDebuffs = []
    
    # Checks the AV of the combatant
    def checkAV(self):
        return self.gauge / self.currentSpeed
    
    # Updates the AV of the class
    def updateAV(self):
        self.AV = self.gauge / self.currentSpeed

    # Resets the gauge of the combatant to the default value, checks duration of buffs/debuffs and removes them if necessary
    def resetGauge(self):
        buffDeletions = []
        debuffDeletions = []

        for i in range(len(self.speedBuffs)):
            amount = self.speedBuffs[i][0]
            self.speedBuffs[i][1] = self.speedBuffs[i][1] - 1
            if self.speedBuffs[i][1] == 0:
                if amount[-1] == "%":
                    self.currentSpeed = self.currentSpeed - (self.baseSpeed * (float(amount.rstrip(amount[-1])) / 100))
                else:
                    self.currentSpeed = self.currentSpeed - float(amount)
                buffDeletions.append(self.speedBuffs[i])
        for i in buffDeletions:
            self.speedBuffs.remove(i)

        for i in range(len(self.speedDebuffs)):
            amount = self.speedDebuffs[i][0]
            self.speedDebuffs[i][1] = self.speedDebuffs[i][1] - 1
            if self.speedDebuffs[i][1] == 0:
                if amount[-1] == "%":
                    self.currentSpeed = self.currentSpeed + (self.baseSpeed * (float(amount.rstrip(amount[-1])) / 100))
                else:
                    self.currentSpeed = self.currentSpeed + float(amount)
                debuffDeletions.append(self.speedDebuffs[i])
        for i in debuffDeletions:
            self.speedDebuffs.remove(i)

        self.gauge = fullGauge
        self.AV = self.checkAV()
        combatantsDict[self.name] = self

    # Ticks the AV of the combatatnt tickCount times
    def tickAV(self, tickCount):
        tickCount = math.ceil(tickCount)
        for x in range(tickCount):
            self.gauge = self.gauge - self.currentSpeed
            self.AV = self.checkAV()
            combatantsDict[self.name] = self
        print(f"{self.name} AV: {str(self.AV)} SPD: {self.currentSpeed}")
        combatantsDict[self.name] = self

    # Advances combatant's turn by a percentage
    def advanceTurn(self, amount):
        beforeGauge = self.gauge
        lowestGauge = 0
        #Determines the combatant with the lowest gauge
        for combatant in combatantsDict:
            if combatantsDict[combatant].gauge < lowestGauge:
                lowestGauge = combatantsDict[combatant].gauge
        # Special case for 100% or more advance
        if float(amount) >= 100:
            self.gauge = lowestGauge - 1
        else:
            self.gauge = self.gauge - ((float(amount) / 100) * 10000)
            if self.gauge <= lowestGauge:
                self.gauge = lowestGauge + 1
        combatantsDict[self.name] = self
        self.updateAV()
        print(f"{self.name} AV Advanced Forward from {beforeGauge} to {self.gauge}")
        #TODO replace with "update turn order" function
        for combatant in combatantsDict:
            combatantVar = combatantsDict[combatant]
            print(f"{combatantVar.name} AV: {combatantVar.AV} SPD: {combatantVar.currentSpeed}")
        updateCurrentTurn()
        print(f"Current Turn: {currentTurn.name}")

    # Delays the combatant's turn by a percent amount
    def delayTurn(self, amount):
        beforeGauge = self.gauge
        self.gauge = self.gauge + ((float(amount)/100) * 10000)
        combatantsDict[self.name] = self
        self.updateAV()
        print(f"{self.name} AV Delayed from {beforeGauge} to {self.gauge}")
        #TODO replace with "update turn order" function
        for combatant in combatantsDict:
            combatantVar = combatantsDict[combatant]
            print(f"{combatantVar.name} AV: {combatantVar.AV} SPD: {combatantVar.currentSpeed}")
        updateCurrentTurn()
        print(f"Current Turn: {currentTurn.name}")

    # Applies a speed buff to the combatant (percent or flat) for turnCount turns
    def speedUp(self, amount, turnCount):
        self.speedBuffs.append([amount, round(float(turnCount))])
        if amount[-1] == "%":
            self.currentSpeed = self.currentSpeed + (self.baseSpeed * (float(amount.rstrip(amount[-1])) / 100))
        else:
            self.currentSpeed = self.currentSpeed + float(amount)
        combatantsDict[self.name] = self
        #TODO add update turn order

    # Applies a speed debuff to the combatant (percent or flat) for turnCount turns
    def slowDown(self, amount, turnCount):
        self.speedDebuffs.append([amount, round(float(turnCount))])
        if amount[-1] == "%":
            self.currentSpeed = self.currentSpeed - (self.baseSpeed * (float(amount.rstrip(amount[-1])) / 100))
        else:
            self.currentSpeed = self.currentSpeed - float(amount)
        combatantsDict[self.name] = self
        #TODO add update turn order



# Creates a combatant class of a certain name, base speed, and current speed
def createCombatant(name, baseSpeed, currentSpeed):
    combatantsDict[name] = Combatant(name, int(baseSpeed), int(currentSpeed))

#TODO move to a fucntion in the class
def inspectCombatant(name):
    print(combatantsDict[name])
    #TODO how the FUCK do i print a dictionary entry
    #for value in combatantsDict[name]:
    #    print(value,':',combatantsDict[name][value])

# Updates the combatant who is currently up
def updateCurrentTurn():
    global currentTurn
    if currentTurn == None:
        currentTurn = combatantsDict[list(combatantsDict.keys())[0]]
    for combatant in combatantsDict:
        if combatantsDict[combatant].AV < currentTurn.AV:
            currentTurn = combatantsDict[combatant]

#Progresses the turn order to the next turn 
def progressTurn():
    global currentTurn
    print('Progressing to the next turn')

    if currentTurn != None:
        currentTurn.resetGauge()
    else:
        currentTurn = combatantsDict[list(combatantsDict.keys())[0]]

    for combatant in combatantsDict:
        if combatantsDict[combatant].AV < currentTurn.AV:
            currentTurn = combatantsDict[combatant]

    ticksNeeded = currentTurn.AV
    for combatant in combatantsDict:
        combatantsDict[combatant].tickAV(ticksNeeded)
    print(f"Current Turn: {currentTurn.name}")


#TODO update turn order (nicely display turn order?)
# Input loop - command interface
while True:
    inputText = input("").split()
    if len(inputText) == 0:
        inputText = [""]

    match inputText[0]:
        case 'create':
            if len(inputText) != 4:
                syntax(inputText)
            else:
                createCombatant(inputText[1], inputText[2], inputText[3])
                print(f"Created {inputText[1]} with base speed {inputText[2]} and current speed {inputText[3]}")

        case 'progress':
            progressTurn()
        case 'advance':
            if len(inputText) != 3:
                syntax(inputText)
            else:
                combatantsDict[inputText[1]].advanceTurn(inputText[2])
        case 'delay':
            if len(inputText) != 3:
                syntax(inputText)
            else:
                combatantsDict[inputText[1]].delayTurn(inputText[2])

        case 'speedup':
            if len(inputText) != 4:
                syntax(inputText)
            else:
                combatantsDict[inputText[1]].speedUp(inputText[2], inputText[3])
        case 'slow':
            if len(inputText) != 4:
                syntax(inputText)
            else:
                combatantsDict[inputText[1]].slowDown(inputText[2], inputText[3])

        case 'inspect':
            #TODO need to fix
            if len(inputText) != 2:
                syntax(inputText)
            else:
                inspectCombatant(inputText[1])

        #TODO help command - iterate through syntax dict
        case 'watermelon':
            print('success')
        case 'exit':
            break
        case _:
            print("command not recognized")