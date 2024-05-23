############################################################################
# File Name: button_group_class.py
# Description: define Alphabet_Button_Group class and Category_Button_Group
#   class. These classes are used to create buttons integrated and easier
#   for user to interact with.
############################################################################
from GUI_class import Circle_Button, Rect_Button


class Alphabet_Button_Group:
  def __init__(self,scr_w,scr_h,command):
    self.create_alphabet_buttons(scr_w,scr_h)
    self.command=command
  
  def create_alphabet_buttons(self,scr_w,scr_h):
    # create alphabet buttons
    text_size=26
    padding=1
    spacing=10
    # start position
    # center buttons on the screen
    x,y=(scr_w-(text_size+padding*2)*12-spacing*12)/2,scr_h-(text_size+padding*2+spacing)*2
    self.buttons=[]
    alphabet=list('abcdefghijklmnopqrstuvwxyz'.upper())
    # 13 buttons per line
    for i,letter in enumerate(alphabet):
      button=Circle_Button(x,y,text=letter,text_size=text_size,border_width=1)
      x+=text_size+padding*2+spacing
      if i==12:
        # next line of buttons
        # set x to init value
        x=(scr_w-(text_size+padding*2)*12-spacing*12)/2
        y+=text_size+padding*2+spacing
      self.buttons.append(button)

  def update(self):
    # update buttons in the group
    for button in self.buttons:
      button.update()
      # run button's command when user release the button
      if button.released:
        self.command(button)

  def draw(self,screen):
    # draw buttons in the group
    for button in self.buttons:
      button.draw(screen)

class Category_Button_Group:
  def __init__(self,categories,scr_w,scr_h,command):
    self.create_category_buttons(categories,scr_w,scr_h)
    self.command=command
    
  def create_category_buttons(self,categories,scr_w,scr_h):
    # create category buttons
    text_size=28
    padding=15
    spacing=20
    # start position
    x,y=scr_w//2+180,scr_h//2-50
    self.buttons=[]
    for category in categories:
      button=Rect_Button(x,y,text=category,text_size=text_size,padding=padding)
      y+=text_size+padding*2+spacing
      self.buttons.append(button)

  def draw(self,screen):
    # draw buttons in the group
    for button in self.buttons:
      button.draw(screen)

  def update(self):
    # update buttons in the group
    for button in self.buttons:
      button.update()
      # run button's command when user release the button
      if button.released:
        self.command(button)