from django.shortcuts import render

from django.http import HttpResponse

from .models import Footprint, SheepEntry, SheepSpottedFrom, Trip, Drive, PredatorLocation, DeadSheep
from desktop_data.models import PredatorArea, ReportEntry
from google_drive_downloader import GoogleDriveDownloader as gdd
from pathlib import Path
from googleapiclient.discovery import build
from .drive_service import signInAndDownloadDB, signOut, getSignInStatus
from .db_helper_functions import calculateSheepData, calculatePredatorData, calculateDeadSheep
from .pdf_service import generatePDF

import requests

def index(request):
    
    if request.method == 'POST':
        predatorJsonString = request.POST['savePredatorArea']
        predatorArea = PredatorArea.objects.create(
            predator_json_string = predatorJsonString
        )
        predatorArea.save()

        print(predatorJsonString);
        message = 'update successful'
        return HttpResponse('s')


    else:
        footprints = Footprint.objects.all()
        sheepEntries = SheepEntry.objects.all()
        sheepSpottedFroms = SheepSpottedFrom.objects.all()
        predatorAreas = PredatorArea.objects.all()
        trips = Trip.objects.all()
        predators = PredatorLocation.objects.all()
        deadSheep = DeadSheep.objects.all()
        print(deadSheep)
        
        return render(request,
        'index.html',
        {
            'footprints': footprints,
            'sheepEntries': sheepEntries,
            'sheepSpottedFroms': sheepSpottedFroms,
            'predatorAreas': predatorAreas,
            'trips': trips,
            'predators': predators,
            'deadSheep': deadSheep
        }
     )

def drive(request):
    if request.method == "POST":
        if 'download' in request.POST:
            postMessage = signInAndDownloadDB()
        elif 'signout' in request.POST:
            postMessage = signOut()
            
        return render(request, 'post_dialogue.html',
        {
            'postMessage': postMessage
        }
        )

    else:
        loginStatus = getSignInStatus()
        print(loginStatus)
        return render(request, 'drive.html',
        {
            'loginStatus': loginStatus
        }
    )

def howToUse(request):
    return render(request, 'how_to_use.html')

def generateReport(request):
    if request.method == "POST":
        pass
    else:
        reports = ReportEntry.objects.all()
        sheepEntries = SheepEntry.objects.all()
        trips = Trip.objects.all()
        regIDs = []
        for trip in trips:
            reg = False
            for report in reports:
                if trip.trip_id == report.trip.trip_id:
                    regIDs.append(report.report_id)
                    print("JA")
                    reg = True
                    break
            if(not reg):
                regIDs.append(0)
                
        print(regIDs)
        zipped_trips = zip(trips, regIDs)
        return render(request, 'generate_report.html',
        {
            'reports': reports,
            'zipped_trips': zipped_trips,
            'sheepEntries': sheepEntries,
        })


def registerTrip(request, tripID):
    if request.method == "POST":
        reports = ReportEntry.objects.filter(trip=tripID)
        if len(reports) != 0:
            postMessage = "Report already registered. Delete if you want to submit it again"
            return render(request, 'post_dialogue.html',
            {
            'postMessage': postMessage
            })
        
        else: 
            trip = Trip.objects.get(trip_id=str(tripID))
            desc = request.POST.get('description')
            
            report = ReportEntry(description=desc, trip=trip)
            report.save()
            postMessage = "Successfully registered trip!"

            return render(request, 'post_dialogue.html',
                {
                'postMessage': postMessage
                }
            )
    else:
            try:
                trip = Trip.objects.get(trip_id=str(tripID))

                totalSheep, totalLambs, totalExpectedLambs = calculateSheepData(tripID)
                totalWolves, totalLynx, totalWolverines = calculatePredatorData(tripID)
                deadSheep = calculateDeadSheep(tripID)

                return render(request, 'trip_registration.html',
                {
                    'trip': trip,
                    'totalSheep': totalSheep,
                    'totalLambs': totalLambs,
                    'totalExpectedLambs': totalExpectedLambs,
                    'missingLambs':totalExpectedLambs - totalLambs,
                    'deadSheep': deadSheep,
                    'totalWolves': totalWolves,
                    'totalLynx': totalLynx,
                    'totalWolverines': totalWolverines
                })
            except:
                return HttpResponse("Trip " + str(tripID) + " does not exist in database")

def inspectRegistration(request, reportID):
    report = ReportEntry.objects.get(report_id=str(reportID))
    trip = Trip.objects.get(trip_id=str(report.trip.trip_id))
    totalSheep, totalLambs, totalExpectedLambs = calculateSheepData(trip.trip_id)
    totalWolves, totalLynx, totalWolverines = calculatePredatorData(trip.trip_id)
    deadSheep = calculateDeadSheep(trip.trip_id)

    return render(request, 'inspect_registration.html',
    {
        'trip': trip,
        'report': report,
        'totalSheep': totalSheep,
        'totalLambs': totalLambs,
        'totalExpectedLambs': totalExpectedLambs,
        'missingLambs': totalExpectedLambs - totalLambs,
        'deadSheep': deadSheep,
        'totalWolves': totalWolves,
        'totalLynx': totalLynx,
        'totalWolverines': totalWolverines
    })

def unregister(request, reportID):
    report = ReportEntry.objects.get(report_id=reportID).delete()
    postMessage = "Deleted report with ID " + str(reportID)
    return render(request, 'post_dialogue.html',
    {
    'postMessage': postMessage
    })

def makePDF(request):
    try:
        reports = ReportEntry.objects.all()
        generatePDF(reports)
        postMessage = "Generated report. Check the reports folder."
        return render(request, 'post_dialogue.html',
        {
        'postMessage': postMessage
        })
    except:
        return HttpResponse("NO REGISTERED TRIPS")
