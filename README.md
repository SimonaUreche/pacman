# Pacman AI Projects 🎮🧠

# 📌 Overview
This repository contains two Artificial Intelligence (AI) projects for Pacman, implemented using Python as part of the Berkeley AI course:

* Pacman Search: Uses search algorithms for pathfinding.
  
* Pacman Multi-Agent: Implements decision-making strategies using AI techniques.
  
Both projects focus on optimizing Pacman’s movement and decision-making through various AI approaches.

# 🚀 1. Pacman Search
# 🔍 Goal
Teach Pacman to navigate the game world using search algorithms.

# 🧠 Implemented Search Algorithms

✅ Depth-First Search (DFS) – Explores deep paths first.

✅ Breadth-First Search (BFS) – Explores all possible paths level by level.

✅ Uniform Cost Search (UCS) – Finds the least-cost path.

✅ A Search (A-Star)* – Uses heuristics to find the best path efficiently.

![WhatsApp Image 2025-03-03 at 09 14 55_764f03e2](https://github.com/user-attachments/assets/d1a86d7a-af4e-456d-843e-60df8db13fc8)


# 🎯 2. Pacman Multi-Agent AI
# 🔍 Goal
Develop AI agents that make intelligent decisions in an environment with ghosts and food pellets.

# 🤖 Implemented AI Techniques

✅ Minimax Algorithm – Decision-making with adversarial agents (ghosts).

✅ Alpha-Beta Pruning – Optimized Minimax for better performance.

✅ Expectimax Algorithm – Probabilistic decision-making.

✅ Evaluation Functions – Custom heuristics for better gameplay.

# 🐍 Python Technologies Used
# ✅ Python Standard Library
* heapq – Used for priority queues in A and UCS algorithms*.
  
* collections.deque – Used for efficient BFS queue implementation.
  
* random – Helps in randomizing ghost movements in multi-agent Pacman.
  
# ✅ Algorithm Implementation in Python

* Implemented graph traversal algorithms in pure Python using data structures like:

  * Lists ([]) → Used for storing open and closed nodes in search algorithms.
  * Tuples (()) → Used for storing (state, cost) pairs in priority queues.
  * Dictionaries ({}) → Used for keeping track of visited states.
    
    ![WhatsApp Image 2025-03-03 at 09 15 14_a3f51d11](https://github.com/user-attachments/assets/0f3aa393-453b-4736-a14d-adc775ad4aa8)

* Object-Oriented Programming (OOP)

  * Class-based agents: SearchAgent, MinimaxAgent, ExpectimaxAgent.
  * Encapsulated behaviors using methods inside classes.
