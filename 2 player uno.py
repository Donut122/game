import pygame
import os
import random
import time
import sys
import threading

width, height = 1920, 1080

#config
fps = 60
turn = "player 1"
deck_size = 8
outline_width = 6
card_scale = 2
animation_speed = 5

card_width = 50 * card_scale
card_height = 100 * card_scale
card_dimensions = (card_width, card_height)

WIN = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Game running @ " + str(width) + " x" + str(height))
clock = pygame.time.Clock()
pygame.display.init()
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 50 * card_scale)
title = pygame.font.Font('freesansbold.ttf', 100 * card_scale)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)

#custom colours
dark_green = (0, 87, 3)
yellow = (235, 255, 5)
grey = (100, 100, 100)

lay_card = pygame.mixer.Sound(os.path.join('sfx', 'lay_card.mp3'))
lay_card.set_volume(1)
countdown = pygame.mixer.Sound(os.path.join('sfx', 'countdown.mp3'))
countdown.set_volume(1)
win_sfx = pygame.mixer.Sound(os.path.join('sfx', 'win.mp3'))
win_sfx.set_volume(1)
denied_sfx = pygame.mixer.Sound(os.path.join('sfx', 'denied.mp3'))
denied_sfx.set_volume(1)

red_tx = pygame.image.load(os.path.join("uno cards", "red.png"))
green_tx = pygame.image.load(os.path.join("uno cards", "green.png"))
blue_tx = pygame.image.load(os.path.join("uno cards", "blue.png"))
yellow_tx = pygame.image.load(os.path.join("uno cards", "yellow.png"))
plus4_tx = pygame.image.load(os.path.join("uno cards", "+4.png"))
wild_tx = pygame.image.load(os.path.join("uno cards", "wild.png"))
bg_tx = pygame.image.load(os.path.join("Textures", "table.png"))
spotlight = pygame.image.load(os.path.join("Textures", "spotlight.png"))
new_card_tx = pygame.image.load(os.path.join("uno cards", "pile.png"))
corner_light = pygame.image.load(os.path.join("Textures", "corner light.png"))

corner_light = pygame.transform.scale(corner_light, (width * 2, height * 2))
corner_rect = corner_light.get_rect()
corner_rect.x = 0 - width
corner_rect.y = 0 - height
leave = False

def light_animation():
    global corner_light
    global corner_rect
    global main_lighting
    main_lighting = pygame.Surface((width, height))
    while True:
        corner_rect.x += animation_speed
        corner_rect.y += round(animation_speed / 1.7)
        if corner_rect.y > 0 or corner_rect.x > 0:
            corner_rect.x = 0 - width
            corner_rect.y = 0 - height
        main_lighting.fill(grey)
        main_lighting.blit(corner_light, (corner_rect))
        time.sleep(0.005)
        if leave:
            break
thread = threading.Thread(target=light_animation)
thread.start()


new_card_tx = pygame.transform.scale(new_card_tx, (100 * card_scale, 200 * card_scale))
spotlight = pygame.transform.scale(spotlight, (width * 2.5, height * 2))
spotlight_rect = spotlight.get_rect()
bg_tx = pygame.transform.scale(bg_tx, (width, height))
bg = bg_tx.get_rect()
bg.x, bg.y = 0, 0

red_tx = pygame.transform.scale(red_tx, (card_dimensions))
green_tx = pygame.transform.scale(green_tx, (card_dimensions))
blue_tx = pygame.transform.scale(blue_tx, (card_dimensions))
yellow_tx = pygame.transform.scale(yellow_tx, (card_dimensions))
plus4_tx = pygame.transform.scale(plus4_tx, (card_dimensions))
wild_tx = pygame.transform.scale(wild_tx, (card_dimensions))

colours = ["red", "green", "blue", "yellow"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+2", "R", "block"]
cards = []
class card:
    def __init__(self, colour, type):
        if type == "wild":
            self.colour = "any"
            self.texture = wild_tx
        elif type == "+4":
            self.colour = "any"
            self.texture = plus4_tx
        else:
            self.colour = colour
        self.type = type
        if colour == "red":
            self.colour_val = red
            self.texture = red_tx
        elif colour == "green":
            self.colour_val = green
            self.texture = green_tx
        elif colour == "blue":
            self.colour_val = blue
            self.texture = blue_tx
        elif colour == "yellow":
            self.colour_val = yellow
            self.texture = yellow_tx
        else:
            self.colour_val = white
        self.rect = self.texture.get_rect()
        if type == "wild" or type == "block" or type == "+4" or type == "R":
            self.skip = True
        else:
            self.skip = False

for colour in colours:
    for number in numbers:
        product = card(colour, number)
        cards.append(product)

cards.append(card("any", "wild"))
cards.append(card("any", "+4"))

p1_deck = []
p2_deck = []
last_card = ""
turn_text = title.render("PLAYER TURN", True, black)
turn_rect = turn_text.get_rect()
turn_rect.y = 0
turn_rect.x = 0
moves = 0
new_card_button = new_card_tx.get_rect()
new_card_button.centery = height /4
new_card_button.centerx = width / 1.2
screen_darkness = pygame.Surface((width, height))
spotlight_rect.centerx = width / 2
spotlight_rect.centery = height / 2
screen_darkness.blit(spotlight, spotlight_rect)


for x in range(deck_size):
    p1_deck.append(cards[random.randint(0, (len(cards) - 1))])
    p2_deck.append(cards[random.randint(0, (len(cards) - 1))])



def can_play(card):
    if moves > 0:
        if card.colour == last_card.colour or card.type == last_card.type or last_card.colour == "any" or card.colour == "any":
            return True
        else:
            return False
    else:
        return True

def look_away():
    countdown.play()
    font = pygame.font.Font('freesansbold.ttf', 100)
    wintext = title.render("5", True, black)
    winrect = wintext.get_rect()
    winrect.centery = height / 2
    winrect.centerx = width / 2
    for x in range(5):
        WIN.blit(bg_tx, bg)
        wintext = title.render(str(5 - x), True, grey)
        WIN.blit(wintext, winrect)
        WIN.blit(screen_darkness, (0, 0), special_flags=pygame.BLEND_MULT)
        pygame.display.update() # counter
        clock.tick(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    break
look_away()
def win(player):
    wintext = title.render(player + " wins!", True, green, black)
    winrect = wintext.get_rect()
    winrect.centery = height / 2
    winrect.centerx = width / 2
    win_sfx.play()
    while True:
        WIN.blit(bg_tx, bg)
        WIN.blit(wintext, winrect)
        WIN.blit(screen_darkness, (0, 0), special_flags=pygame.BLEND_MULT)
        pygame.display.update()
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                leave = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    leave = True
                    break
def add_card(player, amount):
    for x in range(amount):
        if player == "player 1":
            p1_deck.append(cards[random.randint(0, (len(cards) - 1))])
        elif player == "player 2":
            p2_deck.append(cards[random.randint(0, (len(cards) - 1))])
def draw_graphics():
    if moves > 0:
        last_card.rect.centerx = width / 2
        last_card.rect.centery = height / 2
        WIN.blit(last_card.texture, last_card.rect)
        if not (last_card.type == "wild" or last_card.type == "+4" or last_card.type == "block"):
            wintext = font.render(last_card.type, True, black)
            winrect = wintext.get_rect()
            winrect.centery = height / 2
            winrect.centerx = width / 2
            WIN.blit(wintext, winrect)
        if last_card.type == "block":
            wintext = font.render("Ø", True, black)
            winrect = wintext.get_rect()
            winrect.centery = height / 2
            winrect.centerx = width / 2
            WIN.blit(wintext, winrect)
    WIN.blit(new_card_tx, new_card_button)
    WIN.blit(turn_text, turn_rect)
    WIN.blit(main_lighting, (0, 0), special_flags=pygame.BLEND_MULT)
    pygame.display.update()
selection = pygame.Rect(0, 0, 1, 1)
while True:
    clock.tick(fps)
    turn_text = title.render(turn, True, grey)
    key_pressed = pygame.key.get_pressed()
    mouse_pressed = pygame.mouse.get_pressed()
    mx, my = pygame.mouse.get_pos()
    WIN.blit(bg_tx, bg)
    if turn == "player 1":
        count = 0
        last_width = 0
        last_x = 0
        y = height - 120
        if new_card_button.collidepoint(mx, my):
            selection.width = new_card_button.width + outline_width
            selection.height = new_card_button.height + outline_width
            selection.centerx = new_card_button.centerx
            selection.centery = new_card_button.centery
            pygame.draw.rect(WIN, black, selection)
            if mouse_pressed[0]:
                lay_card.play()
                p1_deck.append(cards[random.randint(0, (len(cards) - 1))])
                turn = "player 2"
                look_away()
                moves += 1

        for play in p1_deck:
            has_laid = False
            count += 1
            play.rect.left = (count * 55) * card_scale
            play.rect.bottom = (height - outline_width) - 5
            if not (play.type == "wild" or play.type == "+4" or play.type == "block"):
                wintext = font.render(play.type, True, black)
                winrect = wintext.get_rect()
                winrect.centery = play.rect.centery
                winrect.centerx = play.rect.centerx
            else:
                wintext = "none"
            if play.type == "block":
                wintext = font.render("Ø", True, black)
                winrect = wintext.get_rect()
                winrect.centery = play.rect.centery
                winrect.centerx = play.rect.centerx
            if play.rect.collidepoint(mx, my):
                selection.width = play.rect.width + outline_width
                selection.height = play.rect.height + outline_width
                selection.centerx = play.rect.centerx
                selection.centery = play.rect.centery
                if mouse_pressed[0]:
                    if can_play(play):
                        last_card = play
                        lay_card.play()
                        if play.type == "+2":
                            add_card("player 2", 2)
                        elif play.type == "+4":
                            add_card("player 2", 4)
                        if not play.skip:
                            turn = "player 2"
                            look_away()
                        else:
                            time.sleep(0.5)
                        p1_deck.remove(play)
                        del play
                        has_laid = True
                        moves += 1
                        if len(p1_deck) == 0:
                            win("player 1")
                    else:
                        denied_sfx.play()
                        time.sleep(0.5)
                pygame.draw.rect(WIN, black, selection)
            if not has_laid:
                WIN.blit(play.texture, play.rect)
                if not wintext == "none":
                    WIN.blit(wintext, winrect)
        draw_graphics()
    elif turn == "player 2":
        count = 0
        last_width = 0
        last_x = 0
        y = height - 120
        if new_card_button.collidepoint(mx, my):
            selection.width = new_card_button.width + outline_width
            selection.height = new_card_button.height + outline_width
            selection.centerx = new_card_button.centerx
            selection.centery = new_card_button.centery
            pygame.draw.rect(WIN, black, selection)
            if mouse_pressed[0]:
                lay_card.play()
                p2_deck.append(cards[random.randint(0, (len(cards) - 1))])
                turn = "player 1"
                look_away()
                moves += 1
        for play in p2_deck:
            has_laid = False
            count += 1
            play.rect.left = (count * 55) * card_scale
            play.rect.bottom = (height - outline_width) - 5
            if not (play.type == "wild" or play.type == "+4" or play.type == "block"):
                wintext = font.render(play.type, True, black)
                winrect = wintext.get_rect()
                winrect.centery = play.rect.centery
                winrect.centerx = play.rect.centerx
            else:
                wintext = "none"
            if play.type == "block":
                wintext = font.render("Ø", True, black)
                winrect = wintext.get_rect()
                winrect.centery = play.rect.centery
                winrect.centerx = play.rect.centerx
            if play.rect.collidepoint(mx, my):
                selection.width = play.rect.width + outline_width
                selection.height = play.rect.height + outline_width
                selection.centerx = play.rect.centerx
                selection.centery = play.rect.centery
                if mouse_pressed[0]:
                    if can_play(play):
                        lay_card.play()
                        last_card = play
                        if play.type == "+2":
                            add_card("player 1", 2)
                        elif play.type == "+4":
                            add_card("player 1", 4)
                        if not play.skip:
                            turn = "player 1"
                            look_away()
                        else:
                            time.sleep(0.5)
                        p2_deck.remove(play)
                        del play
                        has_laid = True
                        moves += 1
                        if len(p2_deck) == 0:
                            win("player 2")
                    else:
                        denied_sfx.play()
                        time.sleep(0.5)
                        
                pygame.draw.rect(WIN, black, selection)
            if not has_laid:
                WIN.blit(play.texture, play.rect)
                if not wintext == "none":
                    WIN.blit(wintext, winrect)
        draw_graphics()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            leave = True
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.quit()
                pygame.quit()
                leave = True
                sys.exit(0)
