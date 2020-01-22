import pygame
from math import cos, sin, acos, pi, sqrt


class ModelViewer:
	""" Displays a 3d model. 
	Use w/s, d/a, and q/e to rotate about x, y, and z axi respectively.
	Use c to switch to a cube, p for a pyramid, and t for a triangular prism """
	SCREEN_SIZE = (600, 600)
	CENTER = (300, 300)
	BACKGROUND_COLOR = (0, 0, 0)
	TEXT_COLOR = (255, 255, 255)
	ROTATE_RATE = 0.0075
	CUBE_SIZE = 150
	TRI_PRISM_SIZE = 150
	TRI_PRISM_LENGTH = 150
	PYRAMID_SIZE = 150
	FONT_SIZE = 12
	TEXT_SPACING = 3
	TEXT_TOP = 5
	TEXT_LEFT = 5
	FPS = 120

	def __init__(self):
		""" Create a new application, displaying a cube by default """
		pygame.init()
		self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
		pygame.display.set_caption("Model Viewer")
		self.font = pygame.font.SysFont("Arial", self.FONT_SIZE)
		self.clock = pygame.time.Clock()
		self.current_model = Cube(self.CUBE_SIZE)
		self.running = True
		self.loop()

	def loop(self):
		""" Handle events and draw to screen """
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_c:
						self.current_model = Cube(self.CUBE_SIZE)
					elif event.key == pygame.K_p:
						self.current_model = Pyramid(self.PYRAMID_SIZE)
					elif event.key == pygame.K_t:
						self.current_model = TriangularPrism(self.TRI_PRISM_SIZE, self.TRI_PRISM_LENGTH)
			keys = pygame.key.get_pressed()
			if keys[pygame.K_d]:
				self.current_model.rotate_y(-self.ROTATE_RATE)
			if keys[pygame.K_a]:
				self.current_model.rotate_y(self.ROTATE_RATE)
			if keys[pygame.K_w]:
				self.current_model.rotate_x(self.ROTATE_RATE)
			if keys[pygame.K_s]:
				self.current_model.rotate_x(-self.ROTATE_RATE)
			if keys[pygame.K_q]:
				self.current_model.rotate_z(self.ROTATE_RATE)
			if keys[pygame.K_e]:
				self.current_model.rotate_z(-self.ROTATE_RATE)

			self.screen.fill((0, 0, 0))
			self.current_model.draw(self.screen, self.CENTER)
			self.draw_instructions()
			pygame.display.flip()
			self.clock.tick(self.FPS)

	def draw_instructions(self):
		""" Draw instruction text to screen """
		t1 = self.font.render("w/s - rotate about x-axis", True, self.TEXT_COLOR)
		t2 = self.font.render("d/a - rotate about y-axis", True, self.TEXT_COLOR)
		t3 = self.font.render("q/e - rotate about z-axis", True, self.TEXT_COLOR)
		t4 = self.font.render("c - change to cube model", True, self.TEXT_COLOR)
		t5 = self.font.render("p - change to pyramid model", True, self.TEXT_COLOR)
		t6 = self.font.render("t - change to triangular prism model", True, self.TEXT_COLOR)
		labels = [t1, t2, t3, t4, t5, t6]
		y = self.TEXT_TOP
		for label in labels:
			self.screen.blit(label, (self.TEXT_LEFT, y))
			y += label.get_height() + self.TEXT_SPACING



class Model:
	""" Holds data for a 3d model """

	def __init__(self, points, mesh, colors):
		""" Create a model from the given vertices and mesh of the given colors.
			Points: List of tuples in the format (x, y, z)
			Mesh: List of tuples representing triangles in the format (p1, p2, p3)
					where each p is the index of a vertex  
			Colors: List of tuples in the format (r, g, b) for the corresponding triangles of the mesh """ 
		self.points = points
		self.mesh = mesh
		self.colors = colors

	def rotate_x(self, theta):
		""" Rotate about the x-axis by theta radians """
		for point in self.points:
			new = [0.0, 0.0, 0.0]
			new[0] = point[0]
			new[1] = point[1] * cos(theta) - point[2] * sin(theta)
			new[2] = point[1] * sin(theta) + point[2] * cos(theta)
			point[:] = new[:]

	def rotate_y(self, theta):
		""" Rotate about the y-axis by theta radians """
		for point in self.points:
			new = [0.0, 0.0, 0.0]
			new[0] = point[0] * cos(theta) + point[2] * sin(theta)
			new[1] = point[1]
			new[2] = -point[0] * sin(theta) + point[2] * cos(theta)
			point[:] = new[:]

	def rotate_z(self, theta):
		""" Rotate about the z-axis by theta radians """
		for point in self.points:
			new = [0.0, 0.0, 0.0]
			new[0] = point[0] * cos(theta) - point[1] * sin(theta)
			new[1] = point[0] * sin(theta) + point[1] * cos(theta)
			new[2] = point[2]
			point[:] = new[:]

	def draw(self, screen, center):
		""" Draw model to the screen """
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
			p1x = int(self.points[tri[0]][0]) + center[0]
			p1y = -int(self.points[tri[0]][1]) + center[1]
			p2x = int(self.points[tri[1]][0]) + center[0]
			p2y = -int(self.points[tri[1]][1]) + center[1]
			p3x = int(self.points[tri[2]][0]) + center[0]
			p3y = -int(self.points[tri[2]][1]) + center[1]
			pygame.draw.polygon(screen, tri[3], ((p1x, p1y), (p2x, p2y), (p3x, p3y)))

class Cube(Model):
	""" A cube model """
	
	def __init__(self, size):
		""" Create new cube model where the length of each edge is size """
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
	""" A triangular prism model """
	
	def __init__(self, tri_size, length):
		""" Create a new model where tri_size is the length of the triangle edges 
				and length is the depth of the prism """
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
	""" A pyramid model """
	
	def __init__(self, size):
		""" Create a new model where size is the length of each edge """
		height = sqrt(size ** 2 - (size / 2) ** 2)
		points = [[-size / 2, -height / 2, -size / 2],
				  [-size / 2, -height / 2, size / 2],
				  [size / 2, -height / 2, size / 2],
				  [size / 2, -height / 2, -size / 2],
				  [0, height / 2, 0]]
		mesh = [[0, 4, 3], [1, 4, 0], [2, 4, 1], [3, 4, 2], [1, 0, 3], [3, 2, 1]]
		colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (200, 0, 200), (185, 0, 185)]

		super().__init__(points, mesh, colors)


if __name__ == "__main__":
	ModelViewer()
