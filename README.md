# AI_game_XO
You can run this game using such command: python game.py -n 3 -k 3 -gamemode PvsAI -turn Second

-n a : size of the field a\*a. a = 3 by default

-k a : a number of characters in a row to win. a = 3 by default

-gamemode 'PvsP' - Player vs Player mode, 'PvsAI' - player vs AI mode, 'AIvsAI' - AI vs AI mode. mode = 'PvsAI' by default

-turn 'First' - Play for 'x', 'Second' - Play for 'o'. Works only in 'PvsAI' mode. 'First' by default

*(a, b)* sets the character into the cell *(a, b)*, where *a* is the number of column, counting from the left, *b* is the number of row, counting from the top.
