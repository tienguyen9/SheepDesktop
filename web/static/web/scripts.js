var showingBar = false;
var checkedTripData = L.layerGroup();
var showingPredatorAreas = false;


function openNav() {
    document.getElementById("mySidepanel").style.width = "35%";
    showingBar = true;
  }
  
function closeNav() {
    document.getElementById("mySidepanel").style.width = "0";
    showingBar = false;
  }

function toggle() {
    if (showingBar) {
        closeNav();
    } else {
        openNav()
    }
}


var map = L.map('map', { zoomControl: false});

L.control.zoom({
    position: 'topright'
}).addTo(map);

var drawnItems = new L.FeatureGroup()
map.addLayer(drawnItems)

var drawControl = new L.Control.Draw({
  draw:{
        polyline: false,
        marker: false,
        circlemarker: false,
        rectangle: false,
        polygon: {
            shapeOptions: {
                color : 'yellow'
            }

        },
        circle:false
    },
  edit: {
    featureGroup: drawnItems,
    remove: true,
    edit: false
  },
  position : 'topright'
});


drawControl.setDrawingOptions({
    polygon: {
    	shapeOptions: {
        	color: 'grey'
        }
    }
});

map.addControl(drawControl);


map.on(L.Draw.Event.CREATED, function (e) {
    var type = e.layerType,
    layer = e.layer;
    // Do whatever else you need to. (save to db; add to map etc)
    layer.addTo(drawnItems)
    console.log("c")
    map.addLayer(layer);

    var savePredButton = document.getElementById('savePredDB');
    savePredButton.style.display = "block";

    var shape = layer.toGeoJSON()
    var shape_for_db = JSON.stringify(shape);

    var node=document.createElement("LI");
    var textnode=document.createTextNode(shape_for_db);
    node.appendChild(textnode);
    node.className="pd";
    node.id=L.stamp(layer);
    document.getElementById('pretatorJsonStrings').appendChild(node);
 });


map.on('draw:deleted', function (e) {
    var layers = e.layers;
    layers.eachLayer(function (layer) {
        //do whatever you want; most likely save back to db
        var savePredButton = document.getElementById('savePredDB');
        savePredButton.style.display = "none";
        console.log("d")
        var listItem = document.getElementById(L.stamp(layer));
        listItem.parentNode.removeChild(listItem);
    });
});

function drawPredatorAreas(){
    if(!showingPredatorAreas){
        var predatorAreas = document.getElementsByClassName('predlist')[0].getElementsByTagName("li");
        showingPredatorAreas = true;
        for (let i = 0;i < predatorAreas.length;i++) {
            var jsonString = predatorAreas[i].textContent
            console.log(jsonString + i);
    
            
            var poly = new L.geoJSON(JSON.parse(jsonString), {'color': 'grey', 'opacity': 0.5});
            drawnItems.addLayer(poly);
        }
    }else{
        showingPredatorAreas = false;
        drawnItems.clearLayers();
    }

}


sheepBoxesToggled = false

function toggleSheepBoxes(){
    checkboxes = document.getElementsByName('sheep_marks')
    if(sheepBoxesToggled){
        for(var i=0, n=checkboxes.length;i<n;i++) {
            checkboxes[i].checked = false;
        }
        sheepBoxesToggled = false
    }else{
        for(var i=0, n=checkboxes.length;i<n;i++) {
            checkboxes[i].checked = true;
        }
        sheepBoxesToggled = true
    }

}

tripBoxesToggled = false

function toggleTripBoxes(){
    checkboxes = document.getElementsByName('user_trips')
    if(tripBoxesToggled){
        for(var i=0, n=checkboxes.length;i<n;i++) {
            checkboxes[i].checked = false;
        }
        tripBoxesToggled = false
    }else{
        for(var i=0, n=checkboxes.length;i<n;i++) {
            checkboxes[i].checked = true;
        }
        tripBoxesToggled = true
    }

}


function checkCBs(className){
    var checkboxes = document.getElementsByClassName(className)
    var checkboxesChecked = [];
    for ( let i = 0; i < checkboxes.length; i++){
        if(checkboxes[i].checked){
            checkboxesChecked.push(checkboxes[i]);
        }
    }
    return checkboxesChecked;
}


function drawCheckedData(){
    checkedTripData.clearLayers();
    drawCheckedTrails();
    drawCheckedCBs();
}

function drawCheckedCBs(){
    var checkedSheepTrips = checkCBs('sheep_marks');
    for ( let i = 0; i < checkedSheepTrips.length; i++){
        console.log("i=" + i);
        var sheepEntries = document.getElementsByClassName("sheep_"+checkedSheepTrips[i].value);
        var predatorEntries = document.getElementsByClassName("predator_"+checkedSheepTrips[i].value);
        var deadEntries = document.getElementsByClassName("dead_"+checkedSheepTrips[i].value);
        for( let j = 0; j < sheepEntries.length; j++) {
            var latlonArray = sheepEntries[j].innerHTML.split(',');
            console.log("latitude: " + latlonArray[0]);
            console.log("longitude:" + latlonArray[1]);
            var circle = L.circle([latlonArray[0], latlonArray[1]], {
                color: 'red',
                fillColor: '#f03',
                fillOpacity: 0.5,
                radius: sheepCircleRadius
            }).addTo(checkedTripData);
            checkedTripData.addTo(map);
        }
        var predatorCheckBox = document.getElementById("includePredators");
        if(predatorCheckBox.checked == true){
            for( let j = 0; j < predatorEntries.length; j++) {
                var latlonArray = predatorEntries[j].innerHTML.split(',');
                console.log("latitude: " + latlonArray[0]);
                console.log("longitude:" + latlonArray[1]);
                var circle = L.circle([latlonArray[0], latlonArray[1]], {
                    color: 'black',
                    fillColor: 'black',
                    fillOpacity: 1,
                    radius: 40
                }).addTo(checkedTripData);
                checkedTripData.addTo(map);
            }
        }

        var deadCheckBox = document.getElementById("includeDeads");
        if(deadCheckBox.checked == true){
            for( let j = 0; j < deadEntries.length; j++) {
                var latlonArray = deadEntries[j].innerHTML.split(',');
                console.log("latitude: " + latlonArray[0]);
                console.log("longitude:" + latlonArray[1]);
                var circle = L.circle([latlonArray[0], latlonArray[1]], {
                    color: 'yellow',
                    fillColor: 'yellow',
                    fillOpacity: 1,
                    radius: 25
                }).addTo(checkedTripData);
                checkedTripData.addTo(map);
            }
        }

    }
}

function drawCheckedTrails(){
    var checkedTrailsTrips = checkCBs("user_trips");
    var pointA;
    var pointB;
    for ( let i = 0; i < checkedTrailsTrips.length; i++){
        var footprints = document.getElementsByClassName("foot_"+checkedTrailsTrips[i].value);
        for( let j = 0; j < footprints.length; j++) {
            var latlonArray = footprints[j].innerHTML.split(',');
            if (j%2 == 0){
                pointA = new L.LatLng(latlonArray[0], latlonArray[1]);
            }else{
                pointB = new L.LatLng(latlonArray[0], latlonArray[1]);
            }
            
            if (pointA != null && pointB != null){
                new L.Polyline([pointA, pointB], {color: 'blue'}).addTo(checkedTripData)
                checkedTripData.addTo(map);
            }

        }
        pointA= null;
        pointB=null;
    }
}


 

var firstPointMarker;
var currentPositionMarker;

var sheepMarker;
var sheepMarkerLat;
var sheepMarkerLon;
sheepCircles = {};
var sheepCircleRadius = 25;

//Corners of rectangle for downloading map
var corner1;
var corner2;
var rectangle;

//Strings to be used in Java as input for gownloadTile
var SouthEastString;
var NorthWestString;

function hei(){
    console.log("SGFSAG")
}

function loadOnlineMap(currentLat, currentLon){
    map.setView([currentLat, currentLon], 13);
    L.tileLayer('https://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?layers=norges_grunnkart&zoom={z}&x={x}&y={y}', {
        attribution: '<a href="http://www.kartverket.no/">Kartverket</a>',
    }).addTo(map);

}


function addPoint(lat, lon){
    var point = new L.LatLng(lat, lon);
    map.panTo(point);
    return point;
}

//used in OfflineMapActivity
function addFirstPoint(lat, lon){
    firstPointMarker = L.marker([lat, lon]).addTo(map).bindPopup("This is your starting point").openPopup();
    var point = new L.LatLng(lat, lon);
    map.panTo(point);
    return point;
}

//used in OnlineMapActivity
function showCurrentPosition(lat, lon){
    if(currentPositionMarker != null){
        map.removeLayer(currentPositionMarker);
    }
    currentPositionMarker = L.marker([lat, lon]).addTo(map).bindPopup("This is your current position").openPopup();
    map.panTo(currentPositionMarker.getLatLng());
    return currentPositionMarker;
}

function drawLineBetweenPoints(pointA, pointB){
    var pointList = [pointA, pointB];
    var firstpolyline = new L.Polyline(pointList, {color: 'red'}).addTo(map);
}

function moveSheepMarker(startLat, startLon){
    sheepMarker = L.marker([startLat, startLon], {draggable: true}).addTo(map);
    sheepMarker.setOpacity(1);
    sheepMarker.bindPopup("Drag marker to where you spottet the sheep").openPopup();
    var coord = String(sheepMarker.getLatLng()).split(',');
    sheepMarkerLat = startLat;
    sheepMarkerLon = startLon;
    var newLatLng = new L.LatLng(startLat, startLon);

    sheepMarker.on('dragend', function() {
        sheepMarkerLat = sheepMarker.getLatLng().lat;
        sheepMarkerLon = sheepMarker.getLatLng().lng;
    });
}

function removeSheepMarker(){
    map.removeLayer(sheepMarker);
}

function getSheepMarkerPos(){
    return sheepMarkerLat + "_" + sheepMarkerLon;
}


function hideSheepMarker(){
    sheepMarker.setOpacity(0);
    sheepMarker.closePopup();
}

function isExistingCircle(){
    for (let i = 0;i < sheepCircles.length;i++) {
        console.log(i.getLatLng())
        var ltln = new L.LatLng(sheepMarkerLat, sheepMarkerLon);
        var isInCircleRadius = Math.abs(ltln.distanceTo(sheepCircles[i.getLatLng()])) <= sheepCircleRadius;
        if(isInCircleRadius) {
        console.log("in")
        return true;
        }else{
        console.log("out")
        return false;
        }
}
}

function registerSheepPointMarker(sheepID){
    alert("ASGDBSSDB")
    var circle = L.circle([sheepMarkerLat, sheepMarkerLon], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: sheepCircleRadius
    }).addTo(map);
    sheepCircles[sheepID] = circle;
    circle.on('click', function (e) {
        alert("Hello, circle!" + sheepID);
        AndroidFunction.editSheepRegister(sheepID);
    });
    }


function registerSheepPointLatLng(lat, lon){
var circle = L.circle([lat, lon], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: sheepCircleRadius
}).addTo(map);
    var point = new L.LatLng(lat, lon);
    return point;
}

//for OfflineMapActivity
function drawLineSheepPositionPoint(lastPoint, sheepLat, sheepLon) {
    var point = new L.LatLng(sheepLat, sheepLon);
    var pointList = [lastPoint, point];
    var polyline = new L.Polyline(pointList, {color: 'blue'}).addTo(map);
}

//for TrackingHistoryActivity
function drawLineSheepPositionLatLng(spottedLat, spottedLon, sheepLat, sheepLon) {
    var point1 = new L.LatLng(spottedLat, spottedLon);
    var point2 = new L.LatLng(sheepLat, sheepLon);
    var pointList = [point1, point2];
    var polyline = new L.Polyline(pointList, {color: 'blue'}).addTo(map);
}

function chooseMapRectangle(){

    var mapbounds = map.getBounds();
    if(currentPositionMarker != null){
            currentPositionMarker.setOpacity(0);
    }
    var northWest = mapbounds.getNorthWest();
    var southEast = mapbounds.getSouthEast();
    var centerXdiff = northWest.lat - southEast.lat;
    var centerYdiff = northWest.lng - southEast.lng;
    var corner1StartX = northWest.lat - centerXdiff/4;
    var corner1StartY = northWest.lng - centerYdiff/4;
    var corner2StartX = southEast.lat + centerXdiff/4;
    var corner2StartY = southEast.lng + centerYdiff/4;
    corner1 = L.marker([corner1StartX, corner1StartY], {draggable: true}).addTo(map);
    corner2 = L.marker([corner2StartX, corner2StartY], {draggable: true}).addTo(map);
    UpdateNorthWestCorner();
    UpdateSouthEastCorner();
    
    rectangle = L.polygon([
        corner1.getLatLng(),
        [corner1.getLatLng().lat, corner2.getLatLng().lng],
        corner2.getLatLng(),
        [corner2.getLatLng().lat, corner1.getLatLng().lng]
    ]).addTo(map);
    corner1.on('dragend', function() {
    if(rectangle != null){
        map.removeLayer(rectangle);
    }
    rectangle = L.polygon([
        corner1.getLatLng(),
        [corner1.getLatLng().lat, corner2.getLatLng().lng],
        corner2.getLatLng(),
        [corner2.getLatLng().lat, corner1.getLatLng().lng]
    ]).addTo(map);
    UpdateNorthWestCorner();
    UpdateSouthEastCorner();

    });

    corner2.on('dragend', function() {
    if(rectangle != null){
        map.removeLayer(rectangle);
    }

    rectangle = L.polygon([
        corner1.getLatLng(),
        [corner1.getLatLng().lat, corner2.getLatLng().lng],
        corner2.getLatLng(),
        [corner2.getLatLng().lat, corner1.getLatLng().lng]
    ]).addTo(map);
    UpdateNorthWestCorner();
    UpdateSouthEastCorner();
    });
}

function hideMapRectangle(){
    if(currentPositionMarker != null){
            currentPositionMarker.setOpacity(0);
    }
    map.removeLayer(rectangle);
    map.removeLayer(corner1);
    map.removeLayer(corner2);

}

function UpdateNorthWestCorner(){
    c1Lat = corner1.getLatLng().lat;
    c1Lon = corner1.getLatLng().lng;
    c2Lat = corner2.getLatLng().lat;
    c2Lon = corner2.getLatLng().lng;
    if(c1Lat >= c2Lat && c1Lon <= c2Lon){
        NorthWestString = corner1.getLatLng().lat + "_" + corner1.getLatLng().lng;
    } else if(c1Lat <= c2Lat && c1Lon <= c2Lon){
        NorthWestString = corner2.getLatLng().lat + "_" + corner1.getLatLng().lng;
    } else if(c1Lat >= c2Lat && c1Lon >= c2Lon){
        NorthWestString = corner1.getLatLng().lat + "_" + corner2.getLatLng().lng;
    } else{
        NorthWestString = corner2.getLatLng().lat + "_" + corner2.getLatLng().lng;
    }
}

function UpdateSouthEastCorner(){
    c1Lat = corner1.getLatLng().lat;
    c1Lon = corner1.getLatLng().lng;
    c2Lat = corner2.getLatLng().lat;
    c2Lon = corner2.getLatLng().lng;
    if(c1Lat >= c2Lat && c1Lon <= c2Lon){
        SouthEastString = corner2.getLatLng().lat + "_" + corner2.getLatLng().lng;
    } else if(c1Lat <= c2Lat && c1Lon <= c2Lon){
        SouthEastString = corner1.getLatLng().lat + "_" + corner2.getLatLng().lng;
    } else if(c1Lat >= c2Lat && c1Lon >= c2Lon){
        SouthEastString = corner2.getLatLng().lat + "_" + corner1.getLatLng().lng;
    } else{
        SouthEastString = corner1.getLatLng().lat + "_" + corner1.getLatLng().lng;
    }
}

function GetNorthWestCorner(){
    return NorthWestString;
}

function GetSouthEastCorner(){
    return SouthEastString;
}