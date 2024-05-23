############################################################################
# File Name: GUI_class.py
# Description: define some simple gui class like text area and buttons
############################################################################
import pygame

pygame.init()
click_sound=pygame.mixer.Sound('sound_effects/click.wav')

class Text_Area:
  def __init__(self, x, y, text, text_color=(0,0,0), text_size=14, bg_color=(255,255,255),padding=5,border_width=0, bg_show=False):
    # to run faster, only only create text surface for one time
    # to apply bg_show, split text surface and bg surface
    self.create_text_surface(text,text_size,text_color)
    self.create_bg(bg_color,padding,border_width)
    self.text_rect=self.text_surface.get_rect(center=(x,y))
    self.bg_rect=self.bg.get_rect(center=(x,y))
    self.bg_show=bg_show

  def create_bg(self,bg_color,padding,border_width):
    # create background of text
    width,height=self.text_width,self.text_height
    self.bg_color=bg_color
    self.padding=padding
    self.border_width=border_width
    # background rect
    self.bg=pygame.Surface((width+padding*2,height+padding*2))
    self.bg.fill(bg_color)
    # draw border
    if border_width>0:
      pygame.draw.rect(self.bg,(0,0,0),(0,0,width+padding*2,height+padding*2),border_width)

  def create_text_surface(self,text,text_size,text_color):
    # create text surface
    self.text=text
    self.text_size=text_size
    self.text_color=text_color
    t_font=pygame.font.Font('monogram.ttf',text_size)
    self.text_surface=t_font.render(text,False,text_color)
    self.text_width,self.text_height=self.text_surface.get_size()

  def draw(self,screen):
    # if background is show, draw background
    if self.bg_show:
      screen.blit(self.bg,self.bg_rect)
    screen.blit(self.text_surface,self.text_rect)

class Fade_Text_Area(Text_Area):
  # this text area class can fade out or in
  def __init__(self,x, y, text, text_color=(0,0,0), text_size=14, bg_color=(255,255,255),padding=5,border_width=0, bg_show=False, transparency=255, fade_speed=1, out_or_in='out'):
    super().__init__(x, y, text, text_color,text_size,bg_color,padding,border_width, bg_show)
    self.out_or_in=out_or_in
    self.transparency=transparency
    self.fade_speed=fade_speed
    self.text_surface.set_alpha(self.transparency)
    self.bg.set_alpha(self.transparency)
    
  def set_transparency(self,transparency):
    self.transparency=transparency
    self.text_surface.set_alpha(self.transparency)
    self.bg.set_alpha(self.transparency)
    
  def draw(self,screen):
    # if visible then draw
    if self.transparency>0:
      super().draw(screen)
    
  def update(self):
    if self.out_or_in=='in':
      self.transparency+=self.fade_speed
    if self.out_or_in=='out':
      self.transparency-=self.fade_speed
    # set restrictions of transparency
    self.transparency=min(255,max(0,int(self.transparency)))
    # if transparency reach max or min, don't set image alpha to run faster
    if 0<self.transparency<255:
      self.text_surface.set_alpha(self.transparency)
      self.bg.set_alpha(self.transparency)

class Rect_Button(Text_Area):
  def __init__(self,x, y,command=None,text='button', text_color=(0,0,0), text_size=10, bg_color=(255,255,255),padding=5,border_width=1,clickable=True):
    super().__init__(x, y, text, text_color,text_size,bg_color,padding,border_width, bg_show=True)
    self.command=command
    self.create_image()
    self.rect=self.image.get_rect(center=(x,y))
    self.clickable=clickable
    self.last_tick_pressed=False
    self.pressed=False
    self.released=False

  def create_image(self):
    # create image, touched image and pressed image of button
    self.image=self.bg.copy()
    self.image.blit(self.text_surface,(self.padding,self.padding))
    self.touched_image=self.image.copy()
    self.touched_image.set_alpha(180)
    self.pressed_image=self.image.copy()

  def check_touched(self):
    # check if user touch the button
    return self.rect.collidepoint(pygame.mouse.get_pos())

  def check_pressed(self):
    # check if user press the button
    return self.check_touched() and pygame.mouse.get_pressed()[0] and self.clickable

  def check_released(self):
    # check if user release the button
    # if last tick pressed and this tick not pressed, then user release the button
    return self.check_touched() and self.last_tick_pressed and not self.pressed

  def draw(self,screen):
    if self.check_touched():
      if self.pressed:
        # if user press the button, draw pressed image
        screen.blit(self.pressed_image,self.rect)
      else:
        # if user touch the button, draw touched image
        screen.blit(self.touched_image,self.rect)
    else:
      # if not touch the button, draw normal image
      screen.blit(self.image,self.rect)

  def update(self,**arg):
    # last_tick_pressed to recode last tick pressed state
    self.last_tick_pressed=self.pressed
    self.pressed=self.check_pressed()
    self.released=self.check_released()
    if self.released:
      click_sound.play()
      # if user release the button, run command
      if self.command:
        self.command(**arg)

class Circle_Button(Rect_Button):
  def __init__(self,x, y,command=None,text='button', text_color=(0,0,0), text_size=10, bg_color=(255,255,255),padding=5,border_width=1,clickable=True):
    super().__init__(x, y, command,text, text_color,text_size,bg_color,padding,border_width,clickable)
    self.mask=pygame.mask.from_surface(self.image)
    
  def create_bg(self,bg_color, padding, border_width):
    # create circle background of text
    self.bg_color=bg_color
    self.padding=padding
    self.border_width=border_width
    width,height=self.text_width,self.text_height
    # radius is determined by longest side of text
    self.r=width//2 if width>height else height//2
    self.r+=padding
    r=self.r
    self.bg=pygame.Surface((r*2,r*2),pygame.SRCALPHA,32)
    pygame.draw.circle(self.bg,bg_color,(r,r),r)
    # draw border
    pygame.draw.circle(self.bg,(0,0,0),(r,r),r,border_width)

  def create_image(self):
    # create image, touched image and pressed image of button
    width,height=self.text_width,self.text_height
    r=self.r
    self.image=self.bg.copy()
    self.image.blit(self.text_surface,((2*r-width)//2,(2*r-height)//2))
    self.touched_image=self.image.copy()
    self.touched_image.set_alpha(180)
    self.pressed_image=self.image.copy()

  def check_touched(self):
    # check if user touch the button
    # use mask for accurate collision detection
    mx,my=pygame.mouse.get_pos()
    return super().check_touched() and self.mask.get_at((mx-self.rect.x,my-self.rect.y))
