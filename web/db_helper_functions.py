from .models import SheepEntry, Trip, PredatorLocation, DeadSheep



def calculateSheepData(tripID):
    totalSheep = 0
    totalSpottedSheep = 0
    totalLambs = 0
    expectedLambs= 0
    sheepEntries = SheepEntry.objects.filter(trip=tripID)
    for entry in sheepEntries:
        totalSheep += entry.red_ties + entry.yellow_ties + entry.green_ties + entry.blue_ties
        totalSpottedSheep += entry.total_spotted
        totalLambs -= entry.red_ties + entry.yellow_ties + entry.green_ties + entry.blue_ties
        expectedLambs += entry.red_ties*0 + entry.yellow_ties*1 + entry.green_ties*2 + entry.blue_ties*3

    totalLambs += totalSpottedSheep
    
    return totalSheep, totalLambs, expectedLambs

def calculatePredatorData(tripID):
    totalWolves = 0
    totalLynx = 0
    totalWolverines = 0
    predatorEntries = PredatorLocation.objects.filter(trip=tripID)
    for entry in predatorEntries:
        if(entry.type == "Wolf"):
            totalWolves+=1
        elif(entry.type == "Lynx"):
            totalLynx+=1
        elif(entry.type == "Wolverine"):
            totalWolverines+=1
    
    return totalWolves, totalLynx, totalWolverines

def calculateDeadSheep(tripID):
    deadSheep = DeadSheep.objects.filter(trip=tripID)
    totalDeadSheep = len(deadSheep)
    return totalDeadSheep
    