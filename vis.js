var SCREENWIDTH = 800;  //canvas pixel width
var SCREENHEIGHT = 600; //canvas pixel height
var GAME = new Phaser.Game(SCREENWIDTH, SCREENHEIGHT, Phaser.AUTO, '',
                { preload: preload, create: create, update: update });

var NROUTS = 3;
var ROUT = []; //NROUTS routers ...
var THING;     //detecting one "thing"

var ROUT0X = 23;
var ROUT0Y = 88;
var ROUT1X = 105;
var ROUT1Y = 406;
var ROUT2X = 341;
var ROUT2Y = 230;
var THINGX = 300;
var THINGY = 300;


function preload(){
  GAME.scale.pageAlignHorizontally = true;
  GAME.scale.pageAlignVertically = true;
  GAME.scale.refresh();

  GAME.load.image('ROUTER','router.png');
  GAME.load.image('THING','thing.png');

}
function create(){
  GAME.stage.backgroundColor = '#f2f2f2';


  var rout0 = new Obj(GAME,ROUT0X,ROUT0Y,true);
  var rout1 = new Obj(GAME,ROUT1X,ROUT1Y,true);
  var rout2 = new Obj(GAME,ROUT2X,ROUT2Y,true);

}
function update(){

}
