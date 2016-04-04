
'use strict';

(function (window, document) {

var EMPTY_MARK = 0
var DIMENSION = 4
var field = new Array()
var cur_pos = [0,0]

var __author__ = 'aevlampiev'

    function shuffle_field() {
      var x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];

      for (var i = x.length - 1; i > 0; i--) {
        var num = Math.floor(Math.random() * (i + 1));
        var d = x[num];
        x[num] = x[i];
        x[i] = d;
   		 }
   	    x.push(EMPTY_MARK)  // empty is always last
      for (var i = 0; i < DIMENSION; i++){
          var new_row = new Array();
          for (var j = 0; j < DIMENSION; j++)
              new_row.push(x[i*4+j]);
          field.push(new_row);
          }

                cur_pos[0] = DIMENSION-1
                cur_pos[1] = DIMENSION-1
      return
    }

    function is_game_finished() {
        var flag = true
        for (var i = 0; i < DIMENSION; i++)
          for (var j = 0; j < DIMENSION; j++){
            if (i == DIMENSION-1 && j == DIMENSION-1 && flag)
                    break;
                if (field[i][j] != i*DIMENSION+j+1)
                    flag = false;
          }

        return flag
    }

    function perform_move(key) {
    if (key === 38 && cur_pos[0] != 0)  //up
        {
            var tmp = field[cur_pos[0]-1][cur_pos[1]]
            field[cur_pos[0]-1][cur_pos[1]] = EMPTY_MARK
            field[cur_pos[0]][cur_pos[1]] = tmp
            cur_pos[0] -= 1
        }
    else if (key === 40 && cur_pos[0] != DIMENSION-1) { //down
            var tmp = field[cur_pos[0]+1][cur_pos[1]]
            field[cur_pos[0]+1][cur_pos[1]] = EMPTY_MARK
            field[cur_pos[0]][cur_pos[1]] = tmp
            cur_pos[0] += 1
            }
    else if (key === 37 && cur_pos[1] != 0) {  //left
            var tmp = field[cur_pos[0]][cur_pos[1]-1]
            field[cur_pos[0]][cur_pos[1]-1] = EMPTY_MARK
            field[cur_pos[0]][cur_pos[1]] = tmp
            cur_pos[1] -= 1
            }
    else if (key === 39 && cur_pos[1] != DIMENSION-1) {  //right
            var tmp = field[cur_pos[0]][cur_pos[1]+1]
            field[cur_pos[0]][cur_pos[1]+1] = EMPTY_MARK
            field[cur_pos[0]][cur_pos[1]] = tmp
            cur_pos[1] += 1
            }

    return
	}


 function draw(box) {
  for (var i = 0; i < DIMENSION; i++)
          for (var j = 0; j < DIMENSION; j++){
    var tile = box.childNodes[i*4+j];
    tile.textContent = field[i][j];
    tile.style.visibility = field[i][j]? 'visible' : 'hidden';
    }
  }


 document.addEventListener('DOMContentLoaded',
  function(e) {
        var box = document.body.appendChild(document.createElement('div'));
		for (var i = 0; i < 16; i++)
    		box.appendChild(document.createElement('div'));

    shuffle_field();
    draw(box);

    var key_handler =  function(e) {
      perform_move(e.keyCode);
        draw(box);
        if (is_game_finished()) {
            box.style.backgroundColor = "gold";
            alert("You win!!!")
            window.removeEventListener('keydown',key_handler);
        }
     }

     window.addEventListener('keydown', key_handler)
  });
})(window, document);


