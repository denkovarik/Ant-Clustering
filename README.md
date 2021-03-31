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
This project was developed and tested in Ubuntu on the command line. This guide 
assumes the user is working in Ubuntu on the command line

### Required Software
* Git
* Python 3
   * OpenCV 2
   * Python NumPy module
   * Python random module
   * Python time module
   * Python sys module
   * Python signal module
   * Python os module
   * Python threading module

### Optional Software for Windows Users running Windows Subsystem for Linux (Ubuntu)
* Xming
   * X-server package for displaying platform on windows
   * Note that if you get a error like "(Ant Clustering Simulation:34): 
   Gtk-WARNING **: 21:14:58.430: cannot open display: " when trying to run the program, 
   then make sure Xming is running and then try typing the following command into the 
   shell: "export DISPLAY=:0.0".
   
   
### Clone the repository
* Clone with SSH
  * git clone git@github.com:denkovarik/Ant-Clustering.git
* Clone with HTTPS
  * git clone https://github.com/denkovarik/Ant-Clustering.git
  
## Usage
* This command will start a set of example runs for demonstration
```
python3 antClustering.py
```

## Credits
* Dennis Kovarik

