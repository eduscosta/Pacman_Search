# Pacman Search

* You will need to have Python version 2.7 installed on your computer.

Unzip the file Pacman_Search-master.zip and mounted in the root directory of the following command to test an installation:

```sh
$ cd busca
$ python pacman.py
```

Now you can play pacman game!!

### To run the search algorithms

* DFS (Depth First Search) - Busca em Profundidade 
```sh
$ python pacman.py -l mediumMaze -p SearchAgent
$ python pacman.py -l bigMaze -z .5 -p SearchAgent
```

* BFS (Breadth First Search) - Busca em Largura 
```sh
$ python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
$ python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
```

*  IDS (Iterative Deepening Search) - Busca de Aprofundamento Iterativo 
```sh
$ python pacman.py -l mediumMaze -p SearchAgent -a fn=ids
$ python pacman.py -l bigMaze -p SearchAgent -a fn=ids -z .5
```
*  UCS (Uniform Cost Search) - Busca de Custo Uniforme 
```sh
$ python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
```
*  A* (aStar Search) - Busca A* 
```sh
$ python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

### To see more: https://www.ime.usp.br/~ddm/mac425/ep1.pdf 


