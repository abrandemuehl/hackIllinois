var SCREENWIDTH = 800;  //canvas pixel width
var SCREENHEIGHT = 600; //canvas pixel height
var GAME = new Phaser.Game(SCREENWIDTH, SCREENHEIGHT, Phaser.AUTO, '',
                { preload: preload, create: create, update: update});

var ROUT0X = 10;
var ROUT0Y = 19;
var ROUT1X = 146;
var ROUT1Y = -21;
var ROUT2X = 90;
var ROUT2Y = 100;
var THINGSX = []; THINGSX.push(-100); THINGSX.push(250); THINGSX.push(30); THINGSX.push(650);
var THINGSY = []; THINGSY.push(350); THINGSY.push(275); THINGSY.push(-160); THINGSY.push(375);

var MOUSEDOWNX = undefined;
var MOUSEDOWNY = undefined;
var CLICKCAMERAX;
var CLICKCAMERAY;

var GRAPHICS;

function preload(){
  GAME.scale.pageAlignHorizontally = true;
  GAME.scale.pageAlignVertically = true;
  GAME.scale.refresh();

  GAME.load.image('ROUTER','router.png');
  GAME.load.image('THING','thing.png');

}
function create(){
  GAME.stage.backgroundColor = '#f2f2f2';
  GAME.world.setBounds(0,0,2*SCREENWIDTH,2*SCREENHEIGHT);
  GAME.camera.x = SCREENWIDTH*.5;
  GAME.camera.y = SCREENHEIGHT*.5;

  GRAPHICS = GAME.add.graphics(0,0);
  for(var a = 0; a < SCREENWIDTH*2; a+=(SCREENWIDTH/2)){
    GRAPHICS.beginFill(0xCCCCCC);
    GRAPHICS.moveTo(a,0);
    GRAPHICS.lineTo(a, SCREENHEIGHT*2);
    GRAPHICS.lineTo(a+1, SCREENHEIGHT*2);
    GRAPHICS.lineTo(a+1, 0);
    GRAPHICS.endFill();
  }
  for(var a = 0; a < SCREENHEIGHT*2; a+=(SCREENHEIGHT/2)){
    GRAPHICS.beginFill(0xCCCCCC);
    GRAPHICS.moveTo(0,a);
    GRAPHICS.lineTo(SCREENWIDTH*2, a);
    GRAPHICS.lineTo(SCREENWIDTH*2, a+1);
    GRAPHICS.lineTo(0, a+1);
    GRAPHICS.endFill();
  }


  resizeObjs(ROUT0X,ROUT0Y,ROUT1X,ROUT1Y,ROUT2X,ROUT2Y,THINGSX,THINGSY);

  var rout0 = new Obj(GAME,ROUT0X,ROUT0Y,true);
  var rout1 = new Obj(GAME,ROUT1X,ROUT1Y,true);
  var rout2 = new Obj(GAME,ROUT2X,ROUT2Y,true);
  for(var a = 0; a < THINGSX.length; a++){
    var thing = new Obj(GAME,THINGSX[a],THINGSY[a],false);
  }


}
function update(){
  if(GAME.input.activePointer.isDown){
    if(typeof MOUSEDOWNX === 'undefined'){
      MOUSEDOWNX = GAME.input.mousePointer.x;
      MOUSEDOWNY = GAME.input.mousePointer.y;
      CLICKCAMERAX = GAME.camera.x;
      CLICKCAMERAY = GAME.camera.y;
    }
    GAME.camera.x = CLICKCAMERAX + MOUSEDOWNX - GAME.input.mousePointer.x;
    GAME.camera.y = CLICKCAMERAY + MOUSEDOWNY - GAME.input.mousePointer.y;
  }
  else{
    if(typeof MOUSEDOWNX !== 'undefined'){
      MOUSEDOWNX = undefined;
      MOUSEDOWNY = undefined;
    }
  }

}

//thingsx, thingsy are arrays of things
function resizeObjs(rout0x,rout0y,rout1x,rout1y,rout2x,rout2y,thingsx,thingsy){

  var centerX = (rout0x+rout1x+rout2x)/3;
  var centerY = (rout0y+rout1y+rout2y)/3;

  var dist0 = distance(rout0x,rout0y,centerX,centerY);
  var dist1 = distance(rout1x,rout1y,centerX,centerY);
  var dist2 = distance(rout2x,rout2y,centerX,centerY);
  var bigDist = Math.max(dist0,dist1,dist2)/100;

  rout0x/=bigDist; rout1x/=bigDist; rout2x/=bigDist;
  rout0y/=bigDist; rout1y/=bigDist; rout2y/=bigDist;

  for(var a = 0; a < thingsx.length; a++){
    thingsx[a]/=bigDist;
    thingsy[a]/=bigDist;
  }

  centerX/=bigDist;
  centerY/=bigDist;

  var moveX = SCREENWIDTH - centerX;  //set thing at center, move all that translation
  var moveY = SCREENHEIGHT - centerY; //same

  rout0x+=moveX; rout1x+=moveX; rout2x+=moveX;
  rout0y+=moveY; rout1y+=moveY; rout2y+=moveY;

  for(var a = 0; a < thingsx.length; a++){
    thingsx[a]+=moveX;
    thingsy[a]+=moveY;
  }

  ROUT0X = rout0x;
  ROUT0Y = rout0y;
  ROUT1X = rout1x;
  ROUT1Y = rout1y;
  ROUT2X = rout2x;
  ROUT2Y = rout2y;

  for(var a = 0; a < thingsx.length; a++){
    THINGSX[a] = thingsx[a];
    THINGSY[a] = thingsy[a];
  }

}

function distance(x1,y1,x2,y2){
  return Math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2));
}
