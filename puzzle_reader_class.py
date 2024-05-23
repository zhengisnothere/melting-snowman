############################################################################
# File Name: puzzle_reader_class.py
# Description: define a class to read puzzle files and a class to
#   display puzzle
############################################################################
import random
from copy import deepcopy

from GUI_class import Text_Area


class Puzzle_Reader:
  def __init__(self):
    self.load_puzzles('puzzles.txt')
  
  def load_puzzles(self,puzzle_file):
    # read in puzzle data from puzzles.txt and store them in a dict
    self.categories=[]
    self.puzzles={}
    with open(puzzle_file,'r') as pf:
      read_mode=0
      category=''
      temp_dict={}
      for line in pf:
        # this line is category
        if read_mode==0:
          category=line.strip()
          if category not in self.categories:
            self.puzzles[category]=[]
            self.categories.append(category)
          read_mode=1
        # this line is answer
        elif read_mode==1:
          temp_dict['answer']=line.strip().upper()
          read_mode=2
        # this line is clue
        elif read_mode==2:
          temp_dict['clue']=line.strip()
          self.puzzles[category].append(temp_dict.copy())
          temp_dict.clear()
          read_mode=3
        # this line is blank
        else:
          read_mode=0
    self.puzzles_copy=deepcopy(self.puzzles)

  def random_choose_puzzle(self,category):
    # choose a random puzzle from a category
    # if no puzzle in this category, then restore all puzzles
    if len(self.puzzles[category])==0:
      self.puzzles[category]=deepcopy(self.puzzles_copy[category])
    index=random.randint(0,len(self.puzzles[category])-1)
    # remove this puzzle from this category
    puzzle=self.puzzles[category].pop(index)
    return puzzle['answer'],puzzle['clue']

class Answer_Display(Text_Area):
  def __init__(self,answer,scr_w,scr_h):
    self.answer=answer
    self.scr_w=scr_w
    self.scr_h=scr_h
    self.create_display_str(answer)
    super().__init__(scr_w/2,scr_h/2+75,self.display_str,text_size=36)

  def create_display_str(self,answer):
    # create display string, all letter except ',' will be converted to '_'
    self.display_str=''
    for index,letter in enumerate(answer):
      if letter in ' ,"':
        self.display_str+=letter
      else:
        self.display_str+='_'
      # dubble space
      if index!=len(answer)-1:
        self.display_str+=' '

  def check_letter(self,letter):
    # check if letter is in answer
    if letter in self.answer:
      # if letter is in answer, replace '_' with letter
      for i,char in enumerate(self.answer):
        if char==letter:
          self.display_str=self.display_str[:i*2]+letter+self.display_str[i*2+1:]
      super().__init__(self.scr_w/2,self.scr_h/2+75,self.display_str,text_size=36)
      return True
    else:
      return False

class Puzzle_Display:
  def __init__(self,answer,clue,scr_w,scr_h):
    self.answer_dispaly=Answer_Display(answer,scr_w,scr_h)
    self.clue_display=Text_Area(scr_w/2,scr_h/2+115,clue,text_size=30)

  def draw(self,screen):
    # draw answer display and clue display
    self.answer_dispaly.draw(screen)
    self.clue_display.draw(screen)

  def check_letter(self,letter):
    # check if letter is in answer
    return self.answer_dispaly.check_letter(letter)
