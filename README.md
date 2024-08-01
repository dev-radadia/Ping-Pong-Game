# Ping-Pong-Game

The aim of the project is to create a ping-pong game having a two ‘2 Players’ game-mode with a smooth, intuitive gameplay.

**NOTE:** Before running "The Game.py", change the value of the variable 'Password' to your current MySQL password in 'r.db_info.py' file.

## Salient Features :

	1. The project is divided into 5 packages :
		a. image - Contains the images used in the project
		b. r - Contains the screen-wise strings, resources and font styles used in the project
		c. screens - Contains the logic for every screen in the project, with a module for every screen
		d. sound - Contains the sounds used in the project
		e. sprites - Contains the different pygame drawables that have been used frequently in the project, like ball, paddle, button, etc.


	2. All the GUI Elements in the project are developed solely using Pygame from scratch, in order to keep the GUI consistent throughout the application.


	3. The project also includes various sounds in it, which are played when a button is clicked, or when the ball bounces with the paddle or the wall.


	4. There are a total of 6 screens in the project :
		a. About - Tells the user about the developers and the basic controls of the game
		b. Main Menu - The main screen that has options to go to the other screens
		c. Player Names - The screen where players can enter their names and choose their paddle colours
		d. Game - The game screen, where the players play
		e. Pause - The screen which comes up when players choose to pause the game
		f. EndGame - The screen which declares the winner of the game that was just played


	5. All the screens are then bound and controlled using "The Game.py", the main controller code of this project.
