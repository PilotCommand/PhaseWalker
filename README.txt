Hello Dr. Kivy!

You will notice this zip file contains 4 individual codes and a pdf of our presentation poster.
The python file you should run is called "PhaseWalker.py".
I created the other python files for the sake of organization.

I also hope you will notice that we really went all out on this project,
trying not only to accurately model microstructures, but procedurally generate them, and implement a GUI.

Perhaps this can make up for all the latework during senior project time.

Also, I must formally credit my older brother Khalid Samir Elassaad who led us through this programming adventure.
He is a rather experienced coder and we simply could not have done it without him.

You will need to install some modules using pip: Pygame, Numpy, and PIL (Math should already come with Python but if it doesn't for you, install that as well).

Controls:

W - Up
A - Left
S - Down
D - Right
N - Lower Threshold (Change Phase Concnetration)
M - Increase Threshold (Change Phase Concentration)

Currently, this code uses two unique datastructures that overlap to generate the microstructure.
One models phases, the other models grainboundaries within the same phase.

N and M changes the threshold (value that determines if a data point becomes black or white) for both.
However, if some brave students seek to separate these thresholds they can do it by creating a second threshold variable
like threshold_2 or something, and adding to all the functions that call threshold (and of course some new keybinds).

It has been an honor to study under you, even though it was only for one quarter. I truly did learn alot about modeling, simulations, and especially quantum.

If you need any help running the code or have any questions feel free to contact me through email or even personal cell.
melassaa@calpoly.edu
(408) 876 - 8502

God willing I will see you at graduation!

- Mohammad Samir Elassaad