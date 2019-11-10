import pygame
from math import cos, sin, acos, pi, sqrt


SCREEN_SIZE = (600, 600)
CENTER = (300, 300)
ROTATE_RATE = 0.0025
CUBE_SIZE = 150
TRI_PRISM_SIZE = 150
TRI_PRISM_LENGTH = 150
PYRAMID_SIZE = 150


class Model:
	def __init__(self, points, mesh, colors):
		self.points = points
		self.mesh = mesh
		self.colors = colors

	def rotate_x(self, theta):
		for point in self.points:
			new = [0.0, 0.0, 0.0]
			new[0] = point[0]
			new[1] = point[1] * cos(theta) - point[2] * sin(theta)
			new[2] = point[1] * sin(theta) + point[2] * cos(theta)
			point[:] = new[:]

	def rotate_y(self, theta):
		for point in self.points:
			new = [0.0, 0.0, 0.0]
			new[0] = point[0] * cos(theta) + point[2] * sin(theta)
			new[1] = point[1]
			new[2] = -point[0] * sin(theta) + point[2] * cos(theta)
			point[:] = new[:]

	def rotate_z(self, theta):
		for point in self.points:
			new = [0.0, 0.0, 0.0]
			new[0] = point[0] * cos(theta) - point[1] * sin(theta)
			new[1] = point[0] * sin(theta) + point[1] * cos(theta)
			new[2] = point[2]
			point[:] = new[:]

	def draw(self, screen):
		tris = []
		i = 0
		for tri in self.mesh:
			v1 = [self.points[tri[1]][0] - self.points[tri[0]][0],
					self.points[tri[1]][1] - self.points[tri[0]][1],
					self.points[tri[1]][2] - self.points[tri[0]][2]]
			v2 = [self.points[tri[2]][0] - self.points[tri[0]][0],
					self.points[tri[2]][1] - self.points[tri[0]][1],
					self.points[tri[2]][2] - self.points[tri[0]][2]]
			cross = [v1[1] * v2[2] - v1[2] * v2[1],
					 -v1[0] * v2[2] + v1[2] * v2[0],
					 v1[0] * v2[1] - v1[1] * v2[0]]
			camera = [0, 0, 1]
			dot = cross[0] * camera[0] + cross[1] * camera[1] + cross[2] * camera[2]
			cross_length = sqrt(cross[0] ** 2 + cross[1] ** 2 + cross[2] ** 2)
			angle = acos(dot / cross_length)
			if angle > pi / 2:
				tris.append(tri + [self.colors[i]])
			i += 1


		for tri in tris:
			p1x = int(self.points[tri[0]][0]) + CENTER[0]
			p1y = -int(self.points[tri[0]][1]) + CENTER[1]
			p2x = int(self.points[tri[1]][0]) + CENTER[0]
			p2y = -int(self.points[tri[1]][1]) + CENTER[1]
			p3x = int(self.points[tri[2]][0]) + CENTER[0]
			p3y = -int(self.points[tri[2]][1]) + CENTER[1]
			pygame.draw.polygon(screen, tri[3], ((p1x, p1y), (p2x, p2y), (p3x, p3y)))

class Cube(Model):
	def __init__(self, size):
		points = [[-size / 2, -size / 2, -size / 2], [-size / 2, size / 2, -size / 2],
				[size / 2, size / 2, -size / 2], [size / 2, -size / 2, -size / 2],
				[-size / 2, -size / 2, size / 2], [-size / 2, size / 2, size / 2],
			   	[size / 2, size / 2, size / 2], [size / 2, -size / 2, size / 2]]

		mesh = [[3, 0, 1], [1, 2, 3], [3, 2, 7], [6, 7,2],
				[4, 7, 6], [6, 5, 4], [5, 1, 0], [0, 4, 5],
				[2, 1, 5], [5, 6, 2], [0, 3, 7], [7, 4, 0]]

		colors = [(255, 0, 0), (235, 0, 0), (0, 255, 0), (0, 235, 0),
				(0, 0, 255), (0, 0, 235), (200, 0, 200), (185, 0, 185),
				(255, 255, 0), (235, 235, 0), (0, 235, 235), (0, 200, 200)]

		super().__init__(points, mesh, colors)


class TriangularPrism(Model):
	def __init__(self, tri_size, length):
		height = sqrt(tri_size ** 2 - (tri_size / 2) ** 2)
		points = [[-tri_size / 2, -height / 2, -length / 2],
				  [0, height / 2, -length / 2],
				  [tri_size / 2, -height / 2, -length / 2],
				  [-tri_size / 2, -height / 2, length / 2],
		  		  [0, height / 2, length / 2],
		  		  [tri_size / 2, -height / 2, length / 2]]
		mesh = [[0, 1, 2], [3, 1, 0], [3, 4, 1], [2, 1, 4], [4, 5, 2],
				[0, 2, 5], [5, 3, 0], [5, 4, 3]]
		colors = [(255, 255, 0), (255, 0, 0), (235, 0, 0), (0, 255, 0),
				  (0, 235, 0), (0, 0, 255), (0, 0, 235), (200, 0, 200)]

		super().__init__(points, mesh, colors)


class Pyramid(Model):
	def __init__(self, size):
		height = sqrt(size ** 2 - (size / 2) ** 2)
		points = [[-size / 2, -height / 2, -size / 2],
				  [-size / 2, -height / 2, size / 2],
				  [size / 2, -height / 2, size / 2],
				  [size / 2, -height / 2, -size / 2],
				  [0, height / 2, 0]]
		mesh = [[0, 4, 3], [1, 4, 0], [2, 4, 1], [3, 4, 2], [1, 0, 3], [3, 2, 1]]
		colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (200, 0, 200), (185, 0, 185)]

		super().__init__(points, mesh, colors)


def main():
	screen = pygame.display.set_mode(SCREEN_SIZE)
	current_obj = Cube(CUBE_SIZE)
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					current_obj = Cube(CUBE_SIZE)
				elif event.key == pygame.K_p:
					current_obj = Pyramid(PYRAMID_SIZE)
				elif event.key == pygame.K_t:
					current_obj = TriangularPrism(TRI_PRISM_SIZE, TRI_PRISM_LENGTH)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_d]:
			current_obj.rotate_y(ROTATE_RATE)
		if keys[pygame.K_a]:
			current_obj.rotate_y(-ROTATE_RATE)
		if keys[pygame.K_w]:
			current_obj.rotate_x(ROTATE_RATE)
		if keys[pygame.K_s]:
			current_obj.rotate_x(-ROTATE_RATE)
		if keys[pygame.K_q]:
			current_obj.rotate_z(-ROTATE_RATE)
		if keys[pygame.K_e]:
			current_obj.rotate_z(ROTATE_RATE)


		screen.fill((0, 0, 0))
		current_obj.draw(screen)
		pygame.display.flip()


if __name__ == "__main__":
	main()
