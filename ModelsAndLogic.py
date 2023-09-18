import random
import time

# Diccionario para almacenar información de los procesos
dicProcess = {}

# Lista para almacenar eventos
listEvents = []

# Diccionario para el estado de la CPU
getBussy = {'status': False}



class Cpu:

    def __init__(self):
        self.bussy = False
    
    def process(self):
        # Simula el procesamiento de la CPU durante 1 segundo
        time.sleep(1)

    def getBussy(self):
        return self.bussy

    def setBussy(self, newBussy):
        # Actualiza el estado de la CPU
        getBussy['status'] = newBussy
        self.bussy = newBussy

class Simulator:

    def __init__(self, simulation_time, delay, max_next_process_time, max_process_life_time, max_next_IO_time, max_IO_execution_time, quantum):
        self.simulation_time = simulation_time
        self.delay = delay
        self.max_next_process_time = max_next_process_time
        self.max_process_life_time = max_process_life_time
        self.max_next_IO_time = max_next_IO_time
        self.max_IO_execution_time = max_IO_execution_time
        self.quantum = quantum
        self.nextProcessCreator = self.randomGeneratorTimeNextProcess()
        self.actualProcess = None
        self.processCreator = ProcessCreator(0)
        self.cpu = Cpu()
        getCpu = self.cpu
        self.blocketProcessList = []
        self.readyProcessList = []
        self.finishedProcesses = 0
        self.clock_cycle = 0
    
    def getCpu(self):
        return self.cpu
    
    def randomGeneratorTimeNextProcess(self):
        return random.randint(2, self.max_next_process_time)

    def start(self):
        self.nextProcessCreator = 1
        while self.simulation_time > 0:
            self.showInformation()
            self.updateIoInBlockedList()
            self.nextProcessActualization()
            self.actualProcessActualization()
            self.actualizateSimulatiorTimer()
            if self.actualProcess == None:
                self.cpu.setBussy(False)
                getBussy = False
                if len(self.readyProcessList) > 0:
                    self.actualProcess = self.readyProcessList.pop(0)
                    self.actualProcess.setQuantum(self.quantum)
                    self.actualProcess.setStatus("Running")
                    print("Process ", self.actualProcess.getId(), "assigned to CPU")
                    listEvents.append("Process " + str(self.actualProcess.getId()) + " assigned to CPU")
                    self.cpu.setBussy(True)
                    getBussy = True
            self.cpu.process()

    def showInformation(self):
        print("----------------------------------")
        print("Ciclo de reloj:", self.clock_cycle)
        print("CPU:", end=" ")  
        if self.cpu.getBussy():
            print("Bussy")
        else:
            print("Idle")
        if self.actualProcess != None:
            print("-> Process: ", end=" ")
            self.actualProcess.print_information()
        else:
            print("none")
        print("\n Ready processes queue")
        if len(self.readyProcessList) > 0:
            for i in self.readyProcessList:
                print("-> Process -> ", end=" ")
                i.print_information()
        else:
            print("None")
        print("\n blocked processes queue")
        if len(self.blocketProcessList) > 0:
            for j in self.blocketProcessList:
                print("-> Process -> ", end=" ")
                j.print_information()
        else:
            print(" None")
        print("\nEvents")
        print("Next process will be created in : ", self.nextProcessCreator)
        listEvents.append("Next process will be created in : " + str(self.nextProcessCreator))
        self.clock_cycle += 1

    def actualProcessActualization(self):
        if self.actualProcess != None:
            if self.actualProcess.getLifeTime() <= 0:
                self.actualProcess.setStatus("finished")
                self.actualProcess = None
                self.finishedProcesses = self.finishedProcesses + 1
            if self.actualProcess != None:
                if self.actualProcess.getNextIo() <= 0:
                    print("Process ", self.actualProcess.getId(), " assigned to blocked processes queue")
                    listEvents.append("Process " + str(self.actualProcess.getId()) + " assigned to blocked processes queue")
                    self.actualProcess.setNextIo(self.actualProcess.getDefaultNextIo())
                    self.actualProcess.setQuantum(0)
                    self.blocketProcessList.append(self.actualProcess)
                    self.actualProcess.setStatus("Blocked")
                    self.actualProcess = None
            if self.actualProcess != None:
                if self.actualProcess.getQuantum() > 0:
                    self.actualProcess.setNextIo(self.actualProcess.getNextIo() - 1)
                    self.actualProcess.setQuantum(self.actualProcess.getQuantum() - 1)
                    self.actualProcess.setLifeTime(self.actualProcess.getLifeTime() - 1)
                elif self.actualProcess.getQuantum() == 0:
                    print("Process ", self.actualProcess.getId(), " assigned to ready processes queue")
                    listEvents.append("Process " + str(self.actualProcess.getId()) + " assigned to ready processes queue")
                    self.actualProcess.setStatus("Ready")
                    self.readyProcessList.append(self.actualProcess)
                    self.actualProcess = None

    def actualizateSimulatiorTimer(self):
        self.simulation_time = self.simulation_time - 1
        self.nextProcessCreator = self.nextProcessCreator - 1

    def nextProcessActualization(self):
        if self.nextProcessCreator <= 0:
            self.readyProcessList.append(self.processCreator.createProcess(self.max_process_life_time, self.max_next_IO_time, self.max_IO_execution_time))
            self.nextProcessCreator = self.randomGeneratorTimeNextProcess()
            print("Process ", self.processCreator.getProcessNumber(), " Will be created")
            
    def updateIoInBlockedList(self):
        for n in self.blocketProcessList:
            if n.getIo() <= 0:
                n.setIo(n.getDefaultIo())
                n.setStatus("Ready")
                print("Process ", n.getId(), " assigned to ready processes queue")
                self.readyProcessList.append(n)
                self.blocketProcessList.remove(n)
            else:
                n.setIo(n.getIo() - 1)

class Process:

    def __init__(self, id, life_Time, NextIO, IO, status):
        self.id = id
        self.life_Time = life_Time
        self.NextIO = NextIO
        self.IO = IO
        self.status = status
        self.quantum = 0
        self.default_life_time = life_Time
        self.default_nextIo = NextIO
        self.default_IO = IO

    def getId(self):
        return self.id

    def setNextIo(self, newNextIo):
        self.NextIO = newNextIo

    def getNextIo(self):
        return self.NextIO

    def setIo(self, newIO):
        self.IO = newIO

    def getIo(self):
        return self.IO

    def getDefaultIo(self):
        return self.default_IO

    def setQuantum(self, newQuantum):
        self.quantum = newQuantum

    def setLifeTime(self, newLifeTime):
        self.life_Time = newLifeTime

    def getLifeTime(self):
        return self.life_Time

    def getDefaultNextIo(self):
        return self.default_nextIo

    def getQuantum(self):
        return self.quantum

    def setStatus(self, newStatus):
        self.status = newStatus

    def print_information(self):
        print("Id: ", self.id, ", Life Time: ", self.life_Time, "/", self.default_life_time, ", Next IO:", self.NextIO, "/", self.default_nextIo, ", IO: ", self.IO, "/", self.default_IO, ", Status: ", self.status, ", quantum: ", self.quantum)
        dicProcess[self.id] = (self.id, self.life_Time, self.default_life_time, self.NextIO, self.default_nextIo, self.IO, self.default_IO, self.status, self.quantum)

class ProcessCreator:

    def __init__(self, processNumber):
        self.processNumber = processNumber

    def getProcessNumber(self):
        return self.processNumber

    def generateRandomTimeLife(self, max_process_life_time):
        return random.randint(1, max_process_life_time)

    def generateRandomIOaction(self, max_next_IO_time):
        return random.randint(1, max_next_IO_time)

    def generateRandomIOtimeAction(self, max_IO_execution_time):
        return random.randint(1, max_IO_execution_time)

    def createProcess(self, max_process_life_time, max_next_IO_time, max_IO_execution_time):
        self.processNumber = self.processNumber + 1
        return Process(self.processNumber, self.generateRandomTimeLife(max_process_life_time), self.generateRandomIOaction(max_next_IO_time), self.generateRandomIOtimeAction(max_IO_execution_time), "Ready")

