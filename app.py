import os
import random

import tkinter as tk # build GUI
from PIL import Image, ImageTk # manage image
from playsound import playsound # play audio

WINDOW_TITLE = "Wardrobe App"
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 220
IMG_WIDTH = 200
IMG_HEIGHT = 200
BEIGE_COLOR_HEX = '#E3C396'
SOUND_EFFECT_FILE_PATH = 'assets/Slynk.mp3'
# store all the Tops into a file we can access
ALL_TOPS = [str("tops/") + imagefile for imagefile in os.listdir("tops/") if not imagefile.startswith('.')]
ALL_BOTTOMS = [str("bottoms/") + imagefile for imagefile in os.listdir("bottoms/") if not imagefile.startswith('.')]

class WardrobeApp:
	def __init__(self, root):
		self.root = root

		# show top/bottoms image in the window
		self.top_images = ALL_TOPS
		self.bottom_images = ALL_BOTTOMS

		# save single top & bottom
		self.top_image_path = self.top_images[0]
		self.bottom_image_path = self.bottom_images[0]

		# pack img into top screen, then pack top screen into root
		# create and add top & bottom image into Frame
		self.tops_frame = tk.Frame(self.root, bg = BEIGE_COLOR_HEX)		
		self.bottom_frame = tk.Frame(self.root, bg = BEIGE_COLOR_HEX)		

		self.top_image_label = self.create_photo(self.top_image_path, self.tops_frame)
		self.bottom_image_label = self.create_photo(self.bottom_image_path, self.bottom_frame)
		# add it to pack
		self.top_image_label.pack(side=tk.TOP)
		self.bottom_image_label.pack(side=tk.TOP)

		# create background
		self.create_background()

	def create_background(self):
		# add title to window and change the size
		self.root.title(WINDOW_TITLE)
		self.root.geometry('{0}x{1}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))

		# add all buttons
		self.create_buttons()

		# add clothing
		self.tops_frame.pack(fill=tk.BOTH, expand=tk.YES)
		self.bottom_frame.pack(fill=tk.BOTH, expand=tk.YES)

	def create_buttons(self):
		top_prev_button = tk.Button(self.tops_frame, text="Prev", command = self.get_next_top)
		top_prev_button.pack(side=tk.LEFT)

		create_outfit_button = tk.Button(self.bottom_frame, text="CREATE OUTFIT", command = self.create_outfit())
		create_outfit_button.pack(side=tk.LEFT)

		top_next_button = tk.Button(self.tops_frame, text="Next", command = self.get_prev_top)
		top_next_button.pack(side=tk.RIGHT)

		bottom_prev_button = tk.Button(self.bottom_frame, text="Prev", command = self.get_next_bottom)
		bottom_prev_button.pack(side=tk.LEFT)

		bottom_next_button = tk.Button(self.bottom_frame, text="Next", command = self.get_prev_bottom)
		bottom_next_button.pack(side=tk.RIGHT)

	# generak function that will allow us to move front and back
	def _get_next_item(self, current_item, category, increment = True):

		# if we know where the current item index is in a category, then we find the pic before/after it
		item_index = category.index(current_item)
		final_index = len(category) -1
		next_index = 0

		# consider the edge cases
		if increment and item_index == final_index:
			# add the end, and need to up, cycle back to beginning
			next_index = 0
		elif not increment and item_index == 0:
			# cycle back to end
			next_index = final_index
		else:
			# regular up and down
			# based on increment
			increment = 1 if increment else -1
			next_index = item_index + increment

		next_image = category.index[next_index]

		# reset and update the image based on next_image path
		if current_item in self.top_images:
			image_label = self.top_image_label
			self.top_image_path = next_image
		else:
			image_label = self.bottom_image_label
			self.bottom_image_path = next_image			

		# use update function to change the image
		self.update_image(next_image, image_label)

	def update_image(self, new_image_path, image_label):
		# use pillow to change image to something tkinter can understand
		# collect and change image into tk photo obj
		image_file = Image.open(image_path)
		image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
		tk_photo = Image.Tk.PhotoImage(image_resized)

		#update based on provided image label
		image_label.configure(image=tk_photo)

		# weird tkinter quirk
		image_label.image = tk_photo

	def get_next_top(self):
		self._get_next_item(self.top_image_path, self.top_images)

	def get_prev_top(self):
		self._get_next_item(self.top_image_path, self.top_images, increment = False)

	def get_next_bottom(self):
		self._get_next_item(self.bottom_image_path, self.bottom_images)

	def get_prev_bottom(self):
		self._get_next_item(self.bottom_image_path, self.bottom_images, increment = False)



	def create_photo(self, image_path, frame): # adds an image to window
		image_file = Image.open(image_path)
		image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
		tk_photo = ImageTk.PhotoImage(image_resized) # turn into compatible image
		image_label = tk.Label(frame, image=tk_photo, anchor=tk.CENTER)
		#weird tkinter quirk
		image_label.image = tk_photo

		# so we can add later
		return image_label

	def create_outfit(self):

		# rand select a top & bottom index
		new_top_index = random.randint(0, len(self.top_images)-1)
		new_bottom_index = random.randint(0, len(self.bottom_images)-1)

		# add clothes onto screen
		self.update_image(self.top_images[new_top_index], self.top_image_label)
		self.update_image(self.bottom_images[new_bottom_index], self.bottom_image_label)

		# add noise
		playsound(SOUND_EFFECT_FILE_PATH)

root = tk.Tk()
app = WardrobeApp(root)
print(ALL_TOPS)
root.mainloop()