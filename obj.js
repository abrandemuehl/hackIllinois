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
  this.scale.setTo(scale,scale);
  game.add.existing(this);
}

Obj.prototype = Object.create(Phaser.Sprite.prototype);
Obj.prototype.constructor = Obj;

Obj.prototype.update = function(){

}
