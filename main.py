############################################################################
# Program Name: Melting Snowman
# Author: Zheng Wei
# Date: 2024/05/15
# File Name: main.py
# Description: main file of the game, where the game run.
#   import other files, defines some necessary functions,
#   create variables and objects, call functions, define main function.
############################################################################
import sys

import pygame

from button_group_class import Alphabet_Button_Group, Category_Button_Group
from GUI_class import Rect_Button, Text_Area, Fade_Text_Area
from music_player_class import Music_Player
from puzzle_reader_class import Puzzle_Display, Puzzle_Reader
from snowflake_class import Snowflake_Group
from snowman_class import Snowman

pygame.init()

def update():
  # update objects
  # when user is playing
  if game_start:
    # when lose or win, update play_again_button
    if losing or winning:
      play_again_button.update()
      pause_music_for_sound()
    else:
      alphabet_buttons.update()
      correct_text.update()
      wrong_text.update()
  # when user is selecting category
  else:
    category_buttons.update()
  snowflakes.update(scr_w,scr_h,pygame.time.get_ticks())

def redraw_screen():
  # redraw images on the screen
  if game_start:
    snowman.draw(screen)
    puzzle_display.draw(screen)
    # when lose or win, draw play_again_button
    if losing or winning:
      play_again_button.draw(screen)
      # if win, draw win_text
      # if lose, draw lose_text
      if winning:
        win_text.draw(screen)
      else:
        lose_text.draw(screen)
    # when user is selecting category
    else:
      alphabet_buttons.draw(screen)
      correct_text.draw(screen)
      wrong_text.draw(screen)
  else:
    screen.blit(cover_image,(0,0))
    category_buttons.draw(screen)
  #draw snowflakes
  snowflakes.draw(screen)
  pygame.display.update()

def category_puzzle_select(button):
  # when user click at category button, it will run this dunction
  # it will set the category, choose puzzle and start the game
  global category,game_start,puzzle_display
  category=button.text
  game_start=True
  ans,clue=puzzle_reader.random_choose_puzzle(category)
  puzzle_display=Puzzle_Display(ans,clue,scr_w,scr_h)
  # change music
  music_player.play_random_music()

def alphabet_button_action(button):
  # when user click at alphabet button, it will run this dunction
  # it will check if the letter is a right guess
  correct=puzzle_display.check_letter(button.text)
  button.clickable=False
  if correct:
    guess_correct(button)
  else:
    guess_wrong(button)
  # update button image
  button.create_image()

def check_win():
  # check if player win
  return '_' not in puzzle_display.answer_dispaly.display_str

def check_lose():
  # check if player lose
  return wrong_count == 7

def guess_correct(button):
  # when player guess a correct letter, it will run this function
  correct_sound.play()
  correct_text.set_transparency(255)
  wrong_text.set_transparency(0)
  # set button bg color to green
  bpadding,bbwidth=button.padding,button.border_width
  button.create_bg((0,255,0),bpadding,bbwidth)
  global winning
  if check_win():
    winning=True
    win_sound.play()

def guess_wrong(button):
  # when player guess a wrong letter, it will run this function
  wrong_sound.play()
  correct_text.set_transparency(0)
  wrong_text.set_transparency(255)
  # set button bg color to red
  bpadding,bbwidth=button.padding,button.border_width
  button.create_bg((255,0,0),bpadding,bbwidth)
  global losing,wrong_count
  wrong_count+=1
  snowman.image_index+=1
  if check_lose():
    losing=True
    lose_sound.play()

def game_restart():
  # when player click play_again_button, it will run this function
  # stop all music and sounds
  win_sound.stop()
  lose_sound.stop()
  music_player.play_random_music()
  # reset game variables
  correct_text.set_transparency(0)
  wrong_text.set_transparency(0)
  global game_start,wrong_count,winning,losing,alphabet_buttons
  game_start=False
  wrong_count=0
  winning=False
  losing=False
  snowman.image_index=0
  alphabet_buttons=Alphabet_Button_Group(scr_w,scr_h,alphabet_button_action)

def pause_music_for_sound():
  # when game win or lose, pause background music for win/lose sound
  if get_busy_sound(win_sound) or get_busy_sound(lose_sound):
    if pygame.mixer.music.get_busy():
      pygame.mixer.music.pause()
  else:
    if not pygame.mixer.music.get_busy():
      pygame.mixer.music.unpause()

def get_busy_sound(sound):
  # check if sound is playing
  return sound.get_num_channels() > 0

def load_sound(sound_file):
  # load sound file
  sound=pygame.mixer.Sound('sound_effects/'+sound_file)
  sound.set_volume(0.5)
  return sound

def load_sounds():
  # load all necessary sounds
  global correct_sound,wrong_sound,lose_sound,win_sound
  correct_sound=load_sound('correct.mp3')
  wrong_sound=load_sound('wrong.mp3')
  lose_sound=load_sound('game_over.wav')
  win_sound=load_sound('game_win.wav')

# define some necessary variables
scr_w,scr_h=740,480
screen = pygame.display.set_mode((scr_w,scr_h))
pygame.display.set_caption('melting snowman')
clock=pygame.time.Clock()

running=True
game_start=False
wrong_count=0
winning=False
losing=False

# create objects
alphabet_buttons=Alphabet_Button_Group(scr_w,scr_h,alphabet_button_action)
puzzle_reader=Puzzle_Reader()
categories=puzzle_reader.categories
category_buttons=Category_Button_Group(categories,scr_w,scr_h,category_puzzle_select)
snowman=Snowman(scr_w/2,scr_h/3)
play_again_button=Rect_Button(scr_w/2,scr_h/2+180,command=game_restart,text='Play Again',text_size=60)
win_text=Text_Area(scr_w/2,scr_h/2-80,text='You Win',text_size=100,text_color=(0,255,0),border_width=4,bg_show=True)
lose_text=Text_Area(scr_w/2,scr_h/2-80,text='You Lose',text_size=100,text_color=(255,0,0),border_width=4,bg_show=True)
correct_text=Fade_Text_Area(scr_w/2,scr_h/2-80, 'snowman is happy',text_size=80,text_color=(0,255,0),transparency=0,fade_speed=5)
wrong_text=Fade_Text_Area(scr_w/2,scr_h/2-80, 'snowman is sad',text_size=80,text_color=(255,0,0),transparency=0,fade_speed=5)
cover_image=pygame.transform.scale(pygame.image.load('snowman_images/snowman_cover.png'),(scr_w,scr_h))
snowflakes=Snowflake_Group()
# load sounds and musics
load_sounds()
music_player=Music_Player()
music_player.play_random_music()

# main loop
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running=False
  screen.fill((153, 217, 234))

  update()
  redraw_screen()
  clock.tick(30)

pygame.quit()
sys.exit()