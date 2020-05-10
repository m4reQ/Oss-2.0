if __name__ == "__main__":
    import sys
    sys.exit()

import pygame
from PIL import Image
import os
import random
import ctypes
from .math import Clamp
import math

__user32 = ctypes.windll.user32

STANDARD_RESOLUTION = (640, 480)

def ConvertImage(filepath):
	"""
	Converts image from jpg to png and adds alpha.
	Shouldn't be used frequently because of very low performance.
	:param filepath: (str) Path to an image
	"""
	img = Image.open(filepath)

	newImg = img.copy()
	newImg.putalpha(255)

	newImg.save(filepath[:-4] + '.png')

def DimImage(image, dimPercent):
	"""
	Dims image and returns its copy.
	:param image: (pygame.Surface) Image to dim
	:param dimPercent: (float) Indicates how dark an image should be
	:returns: pygame.Surface
	"""
	img_d = image.copy()

	dark = pygame.Surface(img_d.get_size()).convert_alpha()
	dark.fill((0, 0, 0, dimPercent*255))
	img_d.blit(dark, (0, 0))

	return img_d

class TranslationMode:
	Encode, Decode = range(2)

def TranslateCoord(data, res, mode):
	"""
	Translates position of point to unified coordinate system
	Max value in each direction is 1.0 and the min is 0.0
	:param data: (tuple(float, float)) Position to be translated
	:param res: (tuple(float, float)) Target resolution
	:param mode: (TranslationMode) Work mode. Available modes are: Encode, Decode.
	:returns: (tuple(int, int), tuple(float, float))
	"""

	x, y = data
	resX, resY = res

	#encode
	if mode == TranslationMode.Encode:
		uX = x / resX
		uY = y / resY

		return (uX, uY)
	#decode
	elif mode == TranslationMode.Decode:
		x = Clamp(x, 0, 1)
		y = Clamp(y, 0, 1)

		tX = x * resX
		tY = y * resY

		return (int(tX), int(tY))

def GetTextColor(bgColor):
	avg = sum(bgColor) / len(bgColor)
	textColor = (255, 255, 255) if avg <= 128 else (0, 0, 0)

	return textColor

def IsFullyVisible(rect, winSize):
	xTest = (rect.left >= 0 and rect.left <= winSize[0] - rect.width) and (rect.right <= winSize[0] and rect.right >= rect.width)
	yTest = (rect.bottom <= winSize[1] and rect.bottom >= rect.height) and (rect.top >= 0 and rect.top <= winSize[1] - rect.height)

	return xTest and yTest

def IsPartiallyVisible(rect, winSize):
	winRect = pygame.Rect(0, 0, winSize[0], winSize[1])

	return winRect.colliderect(rect)

def GetScale(width, height):
	return (width / STANDARD_RESOLUTION[0], height / STANDARD_RESOLUTION[1])

def GetScalingFactor(scale):
	return math.ceil((scale[0] + scale[1]) / 2)

class Color():
	Red = (255,0,0)
	Green = (0,255,0)
	Blue = (0,0,255)
	Yellow = (128,128,0)
	Purple = (128,0,128)
	Cyan = (0,128,128)
	White = (255,255,255)
	Black = (0,0,0)
	Gray = (128, 128, 128)
	LightGray = (192, 192, 192)

	@staticmethod
	def Random():
		"""
		Generates random color.
		:returns: tuple(int, int, int)
		"""
		return (random.randint(0, 225), random.randint(0, 225), random.randint(0, 225))

	@staticmethod
	def GetNegative(color):
		r = 255 - color[0]
		g = 255 - color[1]
		b = 255 - color[2]

		return (r, g, b)

class Resolutions():
	SD = (640, 480)
	HD = (1360, 768)
	FHD = (1920, 1080)

	@staticmethod
	def Native():
		"""
		Uses the native display resolution.
		:returns: tuple(int, int)
		"""
		return (__user32.GetSystemMetrics(0), __user32.GetSystemMetrics(1))

	@staticmethod
	def User(width=0, height=0):
		return (width, height)