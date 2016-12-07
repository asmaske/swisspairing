# Swiss Pairing project

Swiss Pairing project is a Python based project.


### Tech

The project uses the following software:

* [Python](https://www.python.org/) - Programming Language
* [Vagrant](https://www.vagrantup.com/) - Virtual Machine

## Project Details

### Running the application
#### 1. Swiss Pairing project
+ Clone/copy the Swiss Pairing source files to a local directory

#### 2. Project Directory Structure
* swisspairing
	+ tournament
    	+ README.md
    	+ tournament.py
    	+ tournament.sql
    	+ tournament_test.py
#### 3. Vagrant environment
+ Clone the **fullstack-nanodegree-vm** repo
+ To use the Vagrant virtual machine, navigate to the **full-stack-nanodegree-vm/vagrant** directory in the terminal
+ cd to **tournament** directory
+ copy **tournament.sql** and **tournament.py** files from cloned source directory to current directory
+ cd to parent directory
+ Execute command **vagrant up** to start the virtual machine
+ Execute command **vagrant ssh** to start the shell
+ cd to **/vagrant/tournament** directory
+ Execute **psql**
	- execute command **\i tournament.sql** to create database, tables and view
	- exit from **psql**
+ Execute python program **python tournament_test.py**
+ On successful execution similar output should be displayed (NOTE: ids will be different):
1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
set([frozenset([61, 63]), frozenset([58, 60]), frozenset([57, 59]), frozenset([64, 58]), frozenset([57, 61]), frozenset([64, 60]), frozenset([64, 62]), frozenset([59, 63]), frozenset([57, 63]), frozenset([60, 62]), frozenset([59, 61]), frozenset([58, 62])])
set([frozenset([58, 60]), frozenset([57, 63]), frozenset([59, 61]), frozenset([64, 62])])
10. After one match, players with one win are properly paired.
Success!  All tests pass!