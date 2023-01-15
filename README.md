
# Syntax Error Project

### Project Description

The project uses python's computer vision (**opencv**) library to detect the movement and orientation of the gloves the user is wearing. Using these controls the game can be played. In the game the user chases and shoots down enemy bikes while trying to avoid obstacles

### Installation

The modules needed for this project can be downloaded using
```
pip install -r requirements.txt
```
to clone the git repository use
```
git clone https://github.com/ShreeSinghi/syntax-error.git
```
After cloning the repository, run the `game.py` file

### Libraries Used

 - OpenCV
	 - to input live video feed from webcam
 - Pygame
	 - to render shapes and images on the screen
	 - to play sounds
 - Threading
	 - to run the video feed processing in parallel to the game logic for efficiency
 - Numpy
	 - to carry out the carry out the artificial intelligence and computer vision computations on the video feed
	 - for collision detection
	 - for inverse-trigonometric operations
 - Pillow 
	 - to enhance the image quality of video feed

### Usage

The user wears specially designed gloves which act as controllers for the game
The green line (in left hand) is used to steer the car and the green dot (in right hand) is used to shoot laser beams

![gloves](https://i.imgur.com/bV5gQbe.jpeg)

### Usage

The user wears specially designed gloves which act as controllers for the game
The green cardboard (on the left glove) is used to steer the car and the green dot (on the right glove) is used to shoot laser beams

How much the user rotates their left hand clockwise/anti-clockwise determines the steering of the car. If the user clenches their right fist then the laser beam is fired and if the hand is kept open (green spot is visible) then there is no shooting.

### Working
**For steering:**
The "greenest" points on the screen are filtered by comparing the values in the red, green and blue channels of the retrieved frame. After obtaining a boolean matrix "image" of the green and non-green points, statistics formulae are used to find the slope/angle of the resulting scatter-plot

**For shooting**
The greenest points are filtered again and the shooting action is decided by a threshold of the fraction of green points covering the camera feed

### Image Credits

[car](https://www.worldtribune.org/2020/lets-talk-about-the-basics/)
[motorbike](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.istockphoto.com%2Fvector%2Fmotorcycle-rider-back-view-simple-flat-illustration-gm1310011771-399553546&psig=AOvVaw0upRyIti1XPtaXAEY5FK4d&ust=1673810890878000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCOj7ps7lx_wCFQAAAAAdAAAAABAD)
[barrier](https://www.flaticon.com/free-icon/barrier_4097450?term=barrier&related_id=4097450)
[rock](https://www.flaticon.com/free-icon/stone_7996088?term=rock&page=1&position=11&origin=tag&related_id=7996088)
[banana](https://www.flaticon.com/free-icon/banana_7112984?term=banana+peel&page=1&position=1&origin=search&related_id=7112984)

