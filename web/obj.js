/*

  either a router or a thing

*/

Obj = function(game, x, y, isRout){

  if(isRout){
    key = 'ROUTER';
    scale = .1;
  }
  else{
    key = 'THING';
    scale = .02;
  }

  Phaser.Sprite.call(this,game,x,y,key);
  this.pivot.x = this.width*.5;
  this.pivot.y = this.height*.5;
  this.scale.setTo(scale,scale);
  this.inputEnabled = true;
  this.events.onInputDown.add(listener, this);
  game.add.existing(this);
}

Obj.prototype = Object.create(Phaser.Sprite.prototype);
Obj.prototype.constructor = Obj;

function scaleObj(obj){
  obj.x/=BIGDIST;
  obj.y/=BIGDIST;
}
function moveObj(obj){
  obj.x+=MOVEX;
  obj.y+=MOVEY;
}

function listener(obj){
  CURROBJ = obj;
}
