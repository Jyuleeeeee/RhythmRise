import pygame, sys, math, time, os
from pygame.locals import *

pygame.init()

# Default Settings
FPS = 30
WIDTH = 900
HEIGHT = 1300
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rhythm Rise')
bold_font = pygame.font.Font('Galmuri11-Bold.ttf', 68)
s_bold_font = pygame.font.Font('Galmuri11-Bold.ttf', 25)
font = pygame.font.Font("Galmuri11.ttf", 48)
small_font = pygame.font.Font("Galmuri11.ttf", 28)
more_s_font = pygame.font.Font("Galmuri11.ttf", 20)

# Colors
BLACK = (0, 0, 0)
DISPLAY = (119, 166, 111)
BACKGROUND = (227, 221, 170)

# Music Load
BackgroundMusic = pygame.mixer.Sound("Fantasia Fantasia.mp3")
BackgroundMusic.set_volume(0.5)
BackgroundMusic.play(-1, 0, 0)
Button_click = pygame.mixer.Sound("click.mp3")
Music_1 = pygame.mixer.Sound("Cruising for Goblins.mp3")
Music_1.set_volume(0.3)
Music_2 = pygame.mixer.Sound("Surf Shimmy.mp3")
Music_2.set_volume(0.7)

# Music tempo
music1_bpm = 155
music1_milliseconds = int(60000 / music1_bpm)  # BPM -> milliseconds
music2_bpm = 170
music2_milliseconds = int(60000 / music2_bpm)

# Image Load
Q = pygame.image.load('Q.png')
Q = pygame.transform.scale(Q, (100, 100))
pressed_Q = pygame.image.load('Q_P.png')
pressed_Q = pygame.transform.scale(pressed_Q, (100, 100))
W = pygame.image.load('W.png')
W = pygame.transform.scale(W, (100, 100))
pressed_W = pygame.image.load('W_P.png')
pressed_W = pygame.transform.scale(pressed_W, (100, 100))
E = pygame.image.load('E.png')
E = pygame.transform.scale(E, (100, 100))
pressed_E = pygame.image.load('E_P.png')
pressed_E = pygame.transform.scale(pressed_E, (100, 100))
R = pygame.image.load('R.png')
R = pygame.transform.scale(R, (100, 100))
pressed_R = pygame.image.load('R_P.png')
pressed_R = pygame.transform.scale(pressed_R, (100, 100))
plus = pygame.image.load('plus.png')
plus = pygame.transform.scale(plus, (250, 250))
S = pygame.image.load('S.png')
S = pygame.transform.scale(S, (400, 400))
A = pygame.image.load('A.png')
A = pygame.transform.scale(A, (400, 400))
B = pygame.image.load('B.png')
B = pygame.transform.scale(B, (400, 400))
F = pygame.image.load('F.png')
F = pygame.transform.scale(F, (400, 400))

# Background settings
screen.fill(BACKGROUND)
pygame.draw.rect(screen, BLACK, pygame.Rect(40, 40, 820, 900))
pygame.draw.rect(screen, DISPLAY, pygame.Rect(80, 80, 740, 820))

# Button settings
button_Q = pygame.Rect(660 ,1000, 100, 100)
screen.blit(Q, button_Q)
button_W = pygame.Rect(590 ,1070, 100, 100)
screen.blit(W, button_W)
button_E = pygame.Rect(660 ,1140, 100, 100)
screen.blit(E, button_E)
button_R = pygame.Rect(730 ,1070, 100, 100)
screen.blit(R, button_R)
screen.blit(plus, (80, 1000))

# Get note information
m1_e_notes = []
with open('music1_easy.txt', 'r') as inFile:
    text_e = inFile.readlines()
for i in range(0, len(text_e)):
    m1_e_notes.append(list(map(str, text_e[i].split())))
m1_n_notes = []
with open('music1_normal.txt', 'r') as inFile:
    text_n = inFile.readlines()
for i in range(0, len(text_n)):
    m1_n_notes.append(list(map(str, text_n[i].split())))
m1_h_notes = []
with open('music1_hard.txt', 'r') as inFile:
    text_h = inFile.readlines()
for i in range(0, len(text_h)):
    m1_h_notes.append(list(map(str, text_h[i].split())))
m2_e_notes = []
with open('music2_easy.txt', 'r') as inFile:
    text_e2 = inFile.readlines()
for i in range(0, len(text_e2)):
    m2_e_notes.append(list(map(str, text_e2[i].split())))
m2_n_notes = []
with open('music2_normal.txt', 'r') as inFile:
    text_n2 = inFile.readlines()
for i in range(0, len(text_n2)):
    m2_n_notes.append(list(map(str, text_n2[i].split())))
m2_h_notes = []
with open('music2_hard.txt', 'r') as inFile:
    text_h2 = inFile.readlines()
for i in range(0, len(text_h2)):
    m2_h_notes.append(list(map(str, text_h2[i].split())))

# Create Note Class
class Note:
    def __init__(self, x, y, size_x, size_y, speed):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.speed = speed

# Note Judgment Function
def get_note_position(key_index):
    if key_index == 0:
        return 250
    elif key_index == 1:
        return 350
    elif key_index == 2:
        return 450
    elif key_index == 3:
        return 550

def check_judgment(note_line, key_index):
    result = 0
    for note in note_line:
        if note.x == get_note_position(key_index):  # Check only at the appropriate location
            if abs(note.y - 800) <= 60:
                if (note.y + 10) >= 790 and (note.y) <= 810: # Perfect
                    result = 1
                elif (note.y + 10) >= 760 and (note.y + 10) <= 840: # Great
                    result = 2
                else: # Miss
                    result = 3

                note_line.remove(note)
    
    return result

# Setting Variables
game_state = 0
q_pressed = False
w_pressed = False
e_pressed = False
r_pressed = False
now_notes = []
score = 0
combo = 0
max_combo = 0
per_count = 0
gre_count = 0
mis_count = 0
easy_max = 305
normal_max = 675
hard_max = 720

# Program loop
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN: # Key Input Processing
            if event.key == K_q:
                q_pressed = True
                screen.blit(pressed_Q, button_Q)
                Button_click.play()
            if event.key == K_w:
                w_pressed = True
                screen.blit(pressed_W, button_W)
                Button_click.play()
            if event.key == K_e:
                e_pressed = True
                screen.blit(pressed_E, button_E)
                Button_click.play()
            if event.key == K_r:
                r_pressed = True
                screen.blit(pressed_R, button_R)
                Button_click.play()
        if event.type == KEYUP:
            if event.key == K_q:
                q_pressed = False
                screen.blit(Q, button_Q)
            if event.key == K_w:
                w_pressed = False
                screen.blit(W, button_W)
            if event.key == K_e:
                e_pressed = False
                screen.blit(E, button_E)
            if event.key == K_r:
                r_pressed = False          
                screen.blit(R, button_R)

    if game_state == 0: # Mainmenu
        pygame.draw.rect(screen, DISPLAY, pygame.Rect(80, 80, 740, 820))
        title = bold_font.render("RHYTHM RISE", True, BLACK)
        screen.blit(title, (210, 250))

        text_lines = ["Q_ game start", "W_ tutorial", "E_ licenses", "R_ exit game"]
        rendered_lines = [font.render(line, True, BLACK) for line in text_lines]
        for i, line in enumerate(rendered_lines):
            screen.blit(line, (270, 400 + i * 100))
        
        pygame.display.flip()

        if q_pressed == True:
            game_state = 1
            q_pressed = False
        if w_pressed == True:
            game_state = 2
            w_pressed = False
        if e_pressed == True:
            game_state = 3
            e_pressed = False
        if r_pressed == True:
            game_state = 4
            r_pressed = False

    elif game_state == 1: # music select
        pygame.draw.rect(screen, DISPLAY, pygame.Rect(80, 80, 740, 820))

        music1 = font.render("Q_ Cruising for Goblins", True, BLACK)
        screen.blit(music1, (150, 300))
        music1_texts = ["Kevin MacLeod", "155 BPM"]
        m1_ren_texts = [small_font.render(text, True, BLACK) for text in music1_texts]
        for i, text in enumerate(m1_ren_texts):
            screen.blit(text, (170, 370 + i*40))

        music2 = font.render("E_ Surf Shimmy", True, BLACK)
        screen.blit(music2, (150, 530))
        music2_texts = ["Kevin MacLeod", "170 BPM"]
        m2_ren_texts = [small_font.render(text, True, BLACK) for text in music2_texts]
        for i, text in enumerate(m2_ren_texts):
            screen.blit(text, (170, 600 + i*40))

        pygame.display.flip()

        if q_pressed == True:
            music = 1
            game_state = 5
            q_pressed = False
        elif e_pressed == True:
            music = 2
            game_state = 5
            e_pressed = False
 
    elif game_state == 2: # tutorial
        pygame.draw.rect(screen, DISPLAY, pygame.Rect(80, 80, 740, 820))

        tutorial = small_font.render("Tutorial", True, BLACK)
        screen.blit(tutorial, (120, 120))
        tuto_lines = ["When the note comes to the decision line,", "press the button that matches the location.", 
        "The more you press at the correct timing,", "the higher your score will be.", "Try a higher level of difficulty!"]
        t_ren_lines = [small_font.render(line, True, BLACK) for line in tuto_lines]
        for i, line in enumerate(t_ren_lines):
            screen.blit(line, (120, 200+i*40))
        
        rect = pygame.draw.rect(screen, BLACK, (600, 830, 200, 50), 2)
        back = more_s_font.render("PRESS R TO MAIN", True, BLACK)
        screen.blit(back, (610, 842))

        pygame.display.flip()

        if r_pressed == True:
            game_state = 0
            r_pressed = False

    elif game_state == 3: # licencse
        pygame.draw.rect(screen, DISPLAY, pygame.Rect(80, 80, 740, 820))

        B_licenses = ["Background Music", '"Fantasia Fantasia" Kevin MacLeod', "(incompetech.com)"]
        B_ren_licenses = [small_font.render(license, True, BLACK) for license in B_licenses]
        for i, license in enumerate(B_ren_licenses):
            screen.blit(license, (120, 120+i*40))
        M1_licenses = ["Music 1", '"Cruising for Goblins" Kevin MacLeod', "(incompetech.com)"]
        M1_ren_licenses = [small_font.render(license, True, BLACK) for license in M1_licenses]
        for i, license in enumerate(M1_ren_licenses):
            screen.blit(license, (120, 280+i*40))        
        M2_licenses = ["Music 2", '"Surf Shimmy" Kevin MacLeod', "(incompetech.com)"]
        M2_ren_licenses = [small_font.render(license, True, BLACK) for license in M2_licenses]
        for i, license in enumerate(M2_ren_licenses):
            screen.blit(license, (120, 440+i*40))   
        Font_licenses = ["Font", 'Galmuri11, Galmuri11-Bold', "© 2019-2023 Minseo Lee", "(itoupluk427@gmail.com)"]
        Font_ren_licenses = [small_font.render(license, True, BLACK) for license in Font_licenses]
        for i, license in enumerate(Font_ren_licenses):
            screen.blit(license, (120, 600+i*40)) 

        rect = pygame.draw.rect(screen, BLACK, (600, 830, 200, 50), 2)
        back = more_s_font.render("PRESS R TO MAIN", True, BLACK)
        screen.blit(back, (610, 842))

        pygame.display.flip()

        if r_pressed == True:
            game_state = 0
            r_pressed = False

    elif game_state == 4: # exit game
        pygame.quit()
        sys.exit()

    elif game_state == 5: # music select -> difficulty select
        pygame.draw.rect(screen, DISPLAY, pygame.Rect(80, 80, 740, 820))

        difficulties = ["Q_ EASY", "W_ NORMAL", "E_ HARD"]
        rendered_difficulties = [font.render(difficulty, True, BLACK) for difficulty in difficulties]
        for i, dif in enumerate(rendered_difficulties):
            screen.blit(dif, (300, 300 + i*150))
        pygame.display.flip()

        if q_pressed == True:
            difficulty = 1
            game_state = 6
        elif w_pressed == True:
            difficulty = 2
            game_state = 6
        elif e_pressed == True:
            difficulty = 3
            game_state = 6

    elif game_state == 6: # difficulty select -> game start
        # Create custom events
        if music == 1:
            pygame.time.set_timer(USEREVENT + 1, 2000)
            pygame.time.set_timer(USEREVENT + 2, music1_milliseconds)  
        elif music == 2:
            pygame.time.set_timer(USEREVENT + 1, 1000)
            pygame.time.set_timer(USEREVENT + 2, music2_milliseconds)

        BackgroundMusic.stop()

        if music == 1:
            if difficulty == 1:
                notes = m1_e_notes[:]
                speed = 5
            elif difficulty == 2:
                notes = m1_n_notes[:]
                speed = 10
            elif difficulty == 3:
                notes = m1_h_notes[:]
                speed = 15
        elif music == 2:
            if difficulty == 1:
                notes = m2_e_notes[:]
                speed = 6
            elif difficulty == 2:
                notes = m2_n_notes[:]
                speed = 12
            elif difficulty == 3:
                notes = m2_h_notes[:]
                speed = 18

        clear = False
        music_play = False
        note_line = []
        judgment = 0

        perfect = s_bold_font.render("PERFECT", True, BLACK)
        great = s_bold_font.render("GREAT", True, BLACK)
        miss = s_bold_font.render("MISS", True, BLACK)

        # Game loop
        while not clear:
            for event in pygame.event.get():
                if event.type == USEREVENT + 1:
                    if music_play == False:
                        if music == 1:
                            Music_1.play()
                        elif music == 2:
                            Music_2.play()
                        music_play = True
                
                # Create Notes
                if event.type == USEREVENT + 2:
                    if len(notes) > 0:
                        line = notes.pop(0)

                        for i in range(0, 4):
                            if line[0][i] == '1':
                                if i == 0:
                                    note_line.append(Note(250, 80, 100, 20, speed))
                                elif i == 1:
                                    note_line.append(Note(350, 80, 100, 20, speed))
                                elif i == 2:
                                    note_line.append(Note(450, 80, 100, 20, speed))
                                elif i == 3:
                                    note_line.append(Note(550, 80, 100, 20, speed))

                # Key Input Processing
                if event.type == KEYDOWN: 
                    if event.key == K_q:
                        q_pressed = True
                        screen.blit(pressed_Q, button_Q)
                        Button_click.play()
                        judgment = check_judgment(note_line, 0)
                    if event.key == K_w:
                        w_pressed = True
                        screen.blit(pressed_W, button_W)
                        Button_click.play()
                        judgment = check_judgment(note_line, 1)
                    if event.key == K_e:
                        e_pressed = True
                        screen.blit(pressed_E, button_E)
                        Button_click.play()
                        judgment = check_judgment(note_line, 2)
                    if event.key == K_r:
                        r_pressed = True
                        screen.blit(pressed_R, button_R)
                        Button_click.play()
                        judgment = check_judgment(note_line, 3)
                if event.type == KEYUP:
                    if event.key == K_q:
                        q_pressed = False
                        screen.blit(Q, button_Q)
                    if event.key == K_w:
                        w_pressed = False
                        screen.blit(W, button_W)
                    if event.key == K_e:
                        e_pressed = False
                        screen.blit(E, button_E)
                    if event.key == K_r:
                        r_pressed = False          
                        screen.blit(R, button_R)

            note_line = [note for note in note_line if note.y <= 860] # Delete Note Off Screen

            # Default Frame Settings
            pygame.draw.rect(screen, DISPLAY, pygame.Rect(80, 80, 740, 820))
            pygame.draw.line(screen, BLACK, (250, 80), (250, 900), 3)
            pygame.draw.line(screen, BLACK, (650, 80), (650, 900), 3)
            pygame.draw.line(screen, BLACK, (250, 800), (650, 800), 10)
            pygame.draw.line(screen, BLACK, (350, 80), (350, 900))
            pygame.draw.line(screen, BLACK, (450, 80), (450, 900))
            pygame.draw.line(screen, BLACK, (550, 80), (550, 900))
            # Show Key Location
            q_key_pos = s_bold_font.render("Q", True, BLACK)
            w_key_pos = s_bold_font.render("W", True, BLACK)
            e_key_pos = s_bold_font.render("E", True, BLACK)
            r_key_pos = s_bold_font.render("R", True, BLACK)
            screen.blit(q_key_pos, (295, 830))
            screen.blit(w_key_pos, (390, 830))
            screen.blit(e_key_pos, (495, 830))
            screen.blit(r_key_pos, (595, 830))
            # Print score, combo
            score_render = more_s_font.render(f"score: {score}", True, BLACK)
            com = more_s_font.render(f"combo: {combo}", True, BLACK)
            screen.blit(score_render, (85, 85))
            screen.blit(com, (85, 110))

            # Draw notes      
            for note in note_line:
                if note.y == 860:
                    judgment = 3
                note.y += note.speed
                pygame.draw.rect(screen, BLACK, (note.x, note.y, note.size_x, note.size_y))

            # score, combo update
            if judgment == 1:
                screen.blit(perfect, (680, 500))
                score += 5
                combo += 1
                per_count += 1
                judgment = 0
            if judgment == 2:
                screen.blit(great, (690, 500))
                score += 3
                combo += 1
                gre_count += 1
                judgment = 0
            if judgment == 3:
                screen.blit(miss, (700, 500))
                combo = 0
                judgment = 0  
                mis_count += 1        

            # max_combo update
            if combo >= max_combo:
                max_combo = combo

            # Check the end of music
            if music_play == True and not pygame.mixer.get_busy():
                clear = True
                game_state = 7          

            pygame.display.flip()

            clock.tick(FPS)
        
    elif game_state == 7:
        pygame.draw.rect(screen, DISPLAY, pygame.Rect(80, 80, 740, 820))       
        grade = pygame.Rect(250, 150, 400, 400)

        if difficulty == 1:
            max_score = easy_max
        elif difficulty == 2:
            max_score = normal_max
        elif difficulty == 3:
            max_score = hard_max
        
        if score >= int(max_score * 0.9):
            screen.blit(S, grade)
        elif score >= int(max_score * 0.7):
            screen.blit(A, grade)
        elif score >= int(max_score * 0.5):
            screen.blit(B, grade)
        else:
            screen.blit(F, grade)
        
        score_ren = s_bold_font.render(f"score  {score}", True, BLACK)
        screen.blit(score_ren, (300, 490))

        max_combo_ren = small_font.render(f"MAX COMBO  {max_combo}", True, BLACK)
        screen.blit(max_combo_ren, (300, 600))

        per_num = small_font.render(f"PERFECT  {per_count}", True, BLACK)
        gre_num = small_font.render(f"GREAT  {gre_count}", True, BLACK)
        mis_num = small_font.render(f"MISS  {mis_count}", True, BLACK)
        screen.blit(per_num, (300, 650))
        screen.blit(gre_num, (300, 700))
        screen.blit(mis_num, (300, 750))

        rect = pygame.draw.rect(screen, BLACK, (600, 830, 200, 50), 2)
        back = more_s_font.render("PRESS R TO EXIT", True, BLACK)
        screen.blit(back, (610, 842))
        pygame.display.flip()

        if r_pressed == True:
            pygame.quit()
            sys.exit()