# TheUltimatePacman

Now it is time for Pacman to show off how good he has become. Pacman will face off against more intelligent opponents in a trickier maze. In particular, the ghosts will actively chase Pacman instead of wandering around randomly, and the maze features more twists and dead-ends, but also extra pellets to give Pacman a fighting chance.

I implemented Minimax search with alpha-beta pruning, using an optimized heuristic function. 
<h4> python pacman.py -l ultimateClassic -p UltimateAgent -g DirectionalGhost -s 1 -n 10 </h4>
Try it yourself, it's super fun to watch how good pacman has become!!

![Alt Text](https://media.giphy.com/media/42xJd9iZp5mn89JU8s/giphy.gif)

<h4> python pacman.py -l ultimateClassic -p UltimateAgent -g DirectionalGhost -s 1 -q -n 10 </h4>
This is the command line to run 10 games and get an average score. 2488 is around the current record. I get a score of 2292.6;

