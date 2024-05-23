############################################################################
# File Name: music_player_class.py
# Description: an integrate music player class for better use
############################################################################
import pygame


class Snowman:
  def __init__(self,x,y):
    self.load_images()
    self.image_index=0
    self.image=self.images[self.image_index]
    self.rect=self.image.get_rect(center=(x,y))

  def load_images(self):
    # load all snowman images
    self.images=[]
    for i in range(8):
      image=pygame.image.load('snowman_images/snowman{}.png'.format(i)).convert_alpha()
      self.images.append(image)

  def draw(self,screen):
    # draw snowman image
    self.image=self.images[self.image_index]
    screen.blit(self.image,self.rect)