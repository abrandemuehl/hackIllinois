var SCREENWIDTH = 800;  //canvas pixel width
var SCREENHEIGHT = 600; //canvas pixel height
var GAME = new Phaser.Game(SCREENWIDTH, SCREENHEIGHT, Phaser.AUTO, '',
                { preload: preload, create: create, update: update});

var test = 0;

var ROUT0,ROUT1,ROUT2;
var ROUTS = [];

var MAP = {};

var CENTERX,CENTERY,BIGDIST,MOVEX,MOVEY;
var SCALE = 100;

var MOUSEDOWNX = undefined;
var MOUSEDOWNY = undefined;
var CLICKCAMERAX;
var CLICKCAMERAY;

var GRAPHICS;

function preload(){
  GAME.scale.pageAlignHorizontally = true;
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


  var rout0 = {
    xPos: 230,
    yPos: 143
  };
  var rout1 = {
    xPos: 23,
    yPos: -43
  };
  var rout2 = {
    xPos: -310,
    yPos: 200
  };

  setRouters(rout0,rout1,rout2);

  var thing0 = {
    xPos: 20,
    yPos: 530
  };
  var thing1 = {
    xPos: 430,
    yPos: -200
  };
  var thing2 = {
    xPos: -10,
    yPos: 1
  };

  setThing('a',thing0);
  setThing('b',thing1);
  setThing('c',thing2);

}
function update(){
  test+=1;

  var thing0 = {
    xPos: test,
    yPos:test
  };
  setThing('a',thing0);

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

/*
function thingsSet(){
  for(var mac in MAP) {
    if (MAP.hasOwnProperty(mac)) {
      MAP[mac]
    }
  }
}
*/
