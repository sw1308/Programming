#! /usr/bin/python -tt

import pygame
import GravitationalBody

BLACK	= (0,	0,	 0)
WHITE	= (255,	255, 255)
RED		= (255,	0,	 0)
GREEN	= (0,	255, 0)
BLUE	= (0,	0,	 255)

# Initialize pygame status and such
pygame.init()
screenSize = (1000,1000)
screen = pygame.display.set_mode(screenSize)
done = False

def renderOnce(gravBodies=[], done=False):
	if not done:
		screen.fill(BLACK)

		for event in pygame.event.get():
			if event.type == pygame.KEYUP:
				done = True

		for body in gravBodies:
			pygame.draw.circle(
				screen,
				BLUE,
				[int(body.xPos), int(body.yPos)],
				int(body.radius)
			)

		pygame.display.flip()
	else:
		pygame.quit()

	return done

if __name__ == '__main__':
	done = False
	testObject = GravitationalBody.GravitationalBody(10, 250, 250, 3, 2)

	while not done:
		done = renderOnce([testObject], done)
		testObject.updatePos()