# Ant-Clustering

## Description
This project implements the Ant Clustering algorithm written in Python. 
Clustering is commonly done in Data Mining and involves the grouping of 
objects based on their similarity to each other. There are multiple 
algorithms used to acheive this, one of which is called the Ant Clustering
Algorithm. 

Ant Clustering Algorithms is a swarm intelligent method on clustering objects
by their similarity to each other, and it was inspired by ant colonies found 
in nature. The idea is that you have a bunch of agents (called ants) that act 
in simple predefined ways, but when these agents interact withing a large 
group, then intelligent behavior emerges that can allow the whole
to solve complex problems.  

In this program there is a room with a bunch of red and blue objects scattered
around randomly. The ant colony is tasked with grouping each object by it's color. 
Each ant simply moves around the room randomly. When an ant comes across an
object that is more unlike the other objects around it, then the ant has a higher 
probability of picking up the object than if the object was around other objects 
similar to it. At the same time, if an ant is carrying an object that is like the 
objects currently around the ant carrying it, then the ant has a higher 
probability of dropping the object than if the ant was around other objects that
where unlike it. Through these simple behavoirs, the ant colony is able to group 
the objects by color relatively well over time.

This project has been adapted from a project created for the CSC 349 Natural 
Computing course at The South Dakota School of Mines and Technology for educational 
purposes. 


## Installation
Note that these projects were developed and tested in Ubuntu on the command
line.

### Required Software
* g++
   * Linux C++ Compiler 
* freeglut3-dev
   * OpenGL - Development libraries
* SOIL
   * Image processing package
* make
   * Linux compiler script manager
* gdb
   * Linux debugger

### Optional Software for Windows Users
* Xming
   * X-server package for displaying platform on windows
   
### Clone the repository
* Clone with SSH
  * git clone git@github.com:denkovarik/Battle-Tanks.git
* Clone with HTTPS
  * git clone https://github.com/denkovarik/Battle-Tanks.git
    
### Build the Project
* make
  
## Usage
* This command will start a set of example runs for demonstration
  * ./start
    
* Alternatively, you can start a single run by typing the following
  * ./projectx/platform
    
* You can modify the map the platform runs by modifying the projectx configuration file 'config.txt'. This file is located in the 'projectx' directory. 
* To have your tank run on the platform, it must be compiled as a .so file and located in the 'projectx/tanks' directory. In addition, you must add the name of your tank to config.txt for itto be loaded onto the platform. An example config file can be found in the projectx directory as a file named 'config.sample'.

## Credits
* Squad7++ 
  * Dennis Kovarik
  * Samuel Backes
  * Adeshkumar Naik
  
* Projectx Platform
  * Jon McKee
  * Riley Kopp
  * Levi Butts
  * JD Pessoa 
