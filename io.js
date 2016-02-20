/*
write your web socket here

order of code:
- get the x,y positions of the 3 routers
- make them rout objects (see setRouters() function header)
- call setRouters() (this should be done only once)
- the following should be done whenever data is recieved from socket:
  - for each device:
    - get the mac address
    - get the x,y cords of the device
    - make a cords object (see setThing() function header)
    - call setThing()
  - call thingsSet() (not seen in this file. it takes no parameters)
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

  ROUT0.scale();ROUT1.scale();ROUT2.scale();


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
