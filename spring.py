#!/usr/bin/env python
"""
Spring
by cubee - 2025

Simple Pygame launcher for loading executables in subdirectories.


"""

import sys
import subprocess
import platform
from math import *
from pygame import *
from pygame.locals import *
from os import path, listdir, access, X_OK, makedirs

frozen = getattr(sys, 'frozen', False)

os_name = platform.system()
print("Running on", platform.system(), frozen and "(frozen)" or "")
res_root = path.dirname(path.realpath(__file__))
exec_root = res_root

# are we running in executable mode?
if frozen:
  exec_root = path.dirname(sys.executable)
  #res_root = sys._MEIPASS


def pretty_string(s):
  return s.replace("_", " ").replace("-", " ").capitalize()

games = []
search = path.join(exec_root, "games")

if not path.isdir(search):
  print("Search path", search, "does not exist, creating.")
  try:
    makedirs(search)
  except:
    print("Could not create path, exiting. Try creating it manually.")
    sys.exit(1)

print("Looking for games in", search)
for d in listdir(search):
  working_dir = path.join(search, d)

  if not path.isdir(working_dir):
    continue

  game = {
    "name": pretty_string(d),
    "dir_name": d,
    "working_dir": working_dir,
    "exe_path": [],
    "icon_path": []
  }
  for file in listdir(working_dir):

    p = path.join(search, d, file)
    file_i = file.lower()

    # get windows executables, excluding crash handlers, installers/uninstallers, etc
    if os_name == "Windows" and ".exe" in file_i and path.isfile(p) and not any(x in file_i for x in [".lnk", "crashhandler", "install"]):
      game["exe_path"].append(p)
      continue

    # get linux executables, excluding crash handlers, installers/uninstallers, etc
    elif os_name == "Linux" and access(p, X_OK) and path.isfile(p) and (any(x in file_i for x in [".x86_64", ".x86", ".sh"]) or "." not in file_i) and not any(x in file_i for x in ["crashhandler", "install", ".dll", ".exe"]):
      game["exe_path"].append(p)
      continue

    # load icon file
    elif "icon" in file_i:
    # prioritise .png icons
      if file_i.endswith(".png"):
        game["icon_path"].insert(0, p)
      else:
        game["icon_path"].append(p)
      continue

    # fancy name file
    elif "name.txt" in file_i:
      with open(p, "r") as name_file:
        game["name"] = name_file.readlines()[0].strip()
      continue

  # add game only if it has any executables
  if len(game.get("exe_path")) > 0:
    print("- Added:", game.get("name"), "(" + game.get("dir_name") + ")")
    games.append(game)
  else:
    print("- Did not find any executables in " + game.get("dir_name") + ", skipping.")


#print(games)
# sort games by directory name, case insensitive, ignoring first "the" and some symbols
games = sorted(games, key = lambda x: x["dir_name"].lower().replace("the", "", 1).strip(" _-."))

def main():
  t = 0

  screen_width = 1280
  screen_height = 720

  columns = 3

  margin = 16 # more like 50% margin, 50% padding, but whatever
  scroll = 0
  scroll_target = scroll

  entry_width = screen_width / columns - margin * 2
  entry_height = 64
  corner_radius = 10

  use_mouse = False
  mouse_pos = (0, 0)
  mouse_pos_prev = mouse_pos
  mouse_left = False
  mouse_right = False
  mouse_middle = False
  mouse_left_last = False
  mouse_right_last = False
  mouse_middle_last = False

  select = 0

  # init ui
  clock = time.Clock()
  sound = True

  init()
  display.init()
  font.init()
  try:
      mixer.init()
  except:
      sound = False
      print("Failed to init mixer, sound disabled")


  # Setup the window
  display.set_caption("Spring")
  display.set_icon(image.load(path.join(res_root, "res", "icon.png")))
  screen = display.set_mode((screen_width, screen_height))

  label_font = font.Font(path.join(res_root, "res", "Lexend-Regular.ttf"), int((entry_height * 0.75) / 2))
  icon_font = font.Font(path.join(res_root, "res", "Lexend-Regular.ttf"), int(entry_height - 16))

  # render labels and load icons
  for game in games:
    game["label_surface"] = label_font.render(game.get("name"), True, (255, 255, 255))
    game["dir_surface"] = label_font.render(game.get("dir_name"), True, (150, 150, 150))

    icon_paths = game.get("icon_path")
    if len(icon_paths) > 0:
      try:
        game["icon"] = image.load(icon_paths[0])
      except:
        print("couldn't load icon: ", icon_paths[0])


  # generate assets
  icon_mask = Surface((entry_height, entry_height))
  icon_mask.fill((0, 0, 0))
  round_rect(icon_mask, Rect(0, 0, entry_height, entry_height), (255, 255, 255), corner_radius)
  icon_mask = mask.from_threshold(icon_mask, (255, 255, 255))


  missing_icon = Surface((entry_height, entry_height))
  missing_icon.fill((255, 120, 120))
  qmark = icon_font.render("?", False, (255, 50, 50))
  #missing_icon.blit(qmark, (qmark.get_width() / 2, qmark.get_height() / 2))
  missing_icon.blit(qmark, (20, 0))

  missing_label = label_font.render("missing label", False, (255, 50, 50))


  #subprocess.run(games[0].get("exe_path")[0])


  while True:
    # update
    clock.tick(60)

    # Event handler
    mouse_scroll = 0
    run_game = False
    for e in event.get():
        # Close key
        if e.type == QUIT:
            sys.exit(0)
        
        # keypresses
        elif e.type == KEYDOWN:
          use_mouse = False
          if e.key == K_UP and select >= columns:
            select -= columns
          if e.key == K_DOWN and select <= len(games) - (columns + 1):
            select += columns
          if e.key == K_LEFT and select % columns > 0:
            select -= 1
          if e.key == K_RIGHT and select % columns < columns - 1:
            select += 1
          if e.key == K_RETURN:
            run_game = True
        
        # scrolling
        elif e.type == MOUSEWHEEL:
          mouse_scroll -= e.y

    select = math.clamp(select, 0, len(games) - 1)

    mouse_pos_prev = mouse_pos
    mouse_pos = mouse.get_pos()
    mouse_left, mouse_middle, mouse_right = mouse.get_pressed()

    if mouse.get_rel() != (0, 0):
      use_mouse = True

    mouse.set_visible(use_mouse)


    #select %= len(games)

    #button = math.clamp(button, 0, len(games[row].get("options") or {"none"}))

    t += 1

    # draw
    screen.fill((50, 50, 50))

    entry_container_height = (margin * 2 + entry_height)
    entries_on_screen_y = screen_height / entry_container_height

    # centre buttons when they fit on-screen
    if entries_on_screen_y > len(games) / columns:
      scroll = (len(games) / columns + 0.5 - entries_on_screen_y) / 2
    
    # scrolling with mouse wheel
    elif use_mouse:
      scroll_target = math.clamp(scroll_target + mouse_scroll, 0, ceil(len(games) / columns) - entries_on_screen_y)
      scroll += (scroll_target - scroll) / 10

    # autoscroll with buttons
    else:
      scroll_target = math.clamp(floor(floor(select / columns) - entries_on_screen_y / 2), 0, ceil(len(games) / columns) - entries_on_screen_y)
      scroll += (scroll_target - scroll) / 10

    idx = 0
    for game in games:
      pos_x = margin + (idx % columns) * (margin * 2 + entry_width)
      pos_y = margin + floor(idx / columns) * entry_container_height - round(scroll * entry_container_height)


      # background card
      selected = idx == select
      bg_rect = Rect(pos_x - margin / 2, pos_y - margin / 2, entry_width + margin, entry_height + margin)
      bg_colour = selected and (100, 100, 100) or (80, 80, 80)
      round_rect(screen, bg_rect, bg_colour, corner_radius, 0)


      # display icon and label text
      icon = game.get("icon") or missing_icon
      if icon:

        # text and icon
        text_width = entry_width - margin / 2 - entry_height
        screen.blit(fit_text(game.get("label_surface") or missing_label, text_width), (pos_x + entry_height + margin / 2, pos_y))
        screen.blit(fit_text(game.get("dir_surface") or missing_label, text_width), (pos_x + entry_height + margin / 2, pos_y + entry_height / 2))
        screen.blit(transform.scale(icon, (entry_height, entry_height)), (pos_x, pos_y))

        # selection border
        if selected:
          round_rect(screen, bg_rect, (200, 200, 200), corner_radius, int(margin / 4))
          #screen.blit(transform.scale(icon, (entry_width + margin, entry_height + margin)), (pos_x - margin / 2, pos_y - margin / 2))

      # check overlap for next frame (otherwise 2 may be selected)
      if use_mouse and bg_rect.collidepoint(mouse_pos):
        select = idx
        if mouse_left and not mouse_left_last:
          run_game = True



      idx += 1

    # run when clicked
    if run_game:
      game = games[select]

      # todo: menu to select executable
      exe_path = game.get("exe_path")[0]
      if len(game.get("exe_path")) > 1:
        print("multiple executables, running", exe_path)

      print("Running", game.get("name"), "from", exe_path)
      try:
        if os_name == "Windows":
          proc = subprocess.Popen([exe_path], cwd = game.get("working_dir"), creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        elif os_name == "Linux":
          proc = subprocess.Popen([exe_path], cwd = game.get("working_dir"))
          # todo: launch linux executables
          #print("No linux native support yet (this is made for HeroicLauncher+Wine)")
      except:
        print("Run failed! Is this file valid?")



    display.flip()
    mouse_left_last = mouse_left
    mouse_right_last = mouse_right
    mouse_middle_last = mouse_middle


def fit_text(surface, width):
  return transform.scale(surface, (min(surface.get_width(), width), surface.get_height()))

def round_rect(screen, rect, col, radius, fill = 0):
  draw.rect(screen, col, rect, fill, radius, radius, radius, radius)

if __name__ == "__main__":
  main()
