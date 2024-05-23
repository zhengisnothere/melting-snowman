############################################################################
# File Name: snowflake_class.py
# Description: Snowflakes falling from the sky
############################################################################
import math
import random

import pygame


class Snowflake_Group:
  # snowflake group class, better control of snowflakes
  def __init__(self):
    self.snowflakes=pygame.sprite.Group()
    self.last_generate_tick=0

  def generate_one_snowflake(self,scr_w):
    # generate one snowflake in random position
    x=random.randint(0,scr_w)
    y=-50
    snowflake=Snowflake(x,y)
    self.snowflakes.add(snowflake)

  def draw(self,screen):
    # draw all snowflakes
    self.snowflakes.draw(screen)

  def update(self,scr_w,scr_h,tick):
    # every 0.25s generate one snowflake
    if tick-self.last_generate_tick>250:
      self.generate_one_snowflake(scr_w)
      self.last_generate_tick=tick
    # update snowflakes
    for snowflake in self.snowflakes:
      snowflake.update(scr_h)

class Snowflake(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    self.load_image()
    self.x,self.y=x,y
    self.rect = self.o_image.get_rect(center=(x, y))
    # generate some random attrs
    self.speed = random.uniform(1, 2.5)
    self.rotate_speed=random.uniform(2,5)
    self.x_dir=random.choice([-1,1])
    self.v1=random.randint(15,25)
    self.v2=random.uniform(1,2)
    self.angle=0

  def load_image(self):
    # load image
    self.o_image = pygame.image.load('snowman_images/snowflake.png').convert_alpha()
    r_size = random.randint(10, 20)
    self.o_image=pygame.transform.scale(self.o_image, (r_size, r_size))
    self.image = self.o_image.copy()

  def rotate(self):
    # rotate image
    self.angle+=self.rotate_speed
    self.image = pygame.transform.rotate(self.o_image, int(self.angle))
    self.rect=self.image.get_rect(center=(self.x,self.y))
    if self.angle>360:
      self.angle=0

  def draw(self, screen):
    screen.blit(self.image, self.rect)

  def update(self, scr_h):
    self.rotate()
    # x coordinate swings left and right
    # sin wave
    self.x+=self.x_dir*math.sin(self.y/self.v1)*self.v2
    # falling down
    self.y += self.speed
    self.rect.center=self.x,self.y
    # if snowflake is out of screen, kill it
    if self.rect.y > scr_h+50:
      self.kill()
