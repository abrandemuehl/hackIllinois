var DEBUGMODE = true; //turn this off when doing websockets

/*
write your web socket here

order of code:
- get the x,y positions of the 3 routers
- make them rout objects (see setRouters() function header)
- call setRouters()
- the following should be done whenever data is recieved from socket:
  - for each device:
    - get the mac address
    - get the x,y cords of the device
    - make a cords object (see setThing() function header)
    - call setThing()
  - repeat whenever new data recieved
*/




/*
  rout0,rout1,rout2 are objects:
    var rout = {
      xPos: 231,
      yPos: 154
    };
*/
function setRouters(rout0,rout1,rout2){
  ROUT0 = new Obj(GAME,rout0.xPos,rout0.yPos,true);
  ROUT1 = new Obj(GAME,rout1.xPos,rout1.yPos,true);
  ROUT2 = new Obj(GAME,rout2.xPos,rout2.yPos,true);

  setCenter(rout0,rout1,rout2);
  setBigDist(rout0,rout1,rout2);
  scaleCenter();

  scaleObj(ROUT0);scaleObj(ROUT1);scaleObj(ROUT2);

  setMove();
  moveObj(ROUT0);moveObj(ROUT1);moveObj(ROUT2);

}

/*
  mac = mac address
  cords = x,y cords corresponding to mac address
    var cords = {
      xPos: 142,
      yPos: 411
    };
*/
function setThing(mac, cords){
  if(mac in MAP){
    MAP[mac].x = cords.xPos;
    MAP[mac].y = cords.yPos;
  }
  else{
    MAP[mac] = new Obj(GAME,cords.xPos,cords.yPos,false);
  }
  scaleObj(MAP[mac]);
  moveObj(MAP[mac]);
}

/*

  the following are helper functions

*/
function setCenter(rout0,rout1,rout2){
  CENTERX = (rout0.xPos+rout1.xPos+rout2.xPos)/3;
  CENTERY = (rout0.yPos+rout1.yPos+rout2.yPos)/3;
}
function setBigDist(rout0,rout1,rout2){
  var dist0 = distance(rout0.xPos,rout0.yPos,CENTERX,CENTERY);
  var dist1 = distance(rout1.xPos,rout1.yPos,CENTERX,CENTERY);
  var dist2 = distance(rout2.xPos,rout2.yPos,CENTERX,CENTERY);
  BIGDIST = Math.max(dist0,dist1,dist2)/SCALE;
}
function scaleCenter(){
  CENTERX/=BIGDIST;
  CENTERY/=BIGDIST;
}
function setMove(){
  MOVEX = SCREENWIDTH - CENTERX;
  MOVEY = SCREENHEIGHT - CENTERY;
}
function distance(x1,y1,x2,y2){
  return Math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2));
}


var ws = new WebSocket('ws://' + window.location.hostname + '/data/ws');


ws.onmessage = function(event) {
    var data = JSON.parse(event.data);
    if(data.type == "routers") {
        setRouters(data.values[0], data.values[1], data.values[2])
    }
    else if(data.type == "device") {
        setThing(data.mac, data);
        
    }
}


