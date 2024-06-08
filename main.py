import pygame
from random import choice
pygame.init()

WIDTH, HEIGHT = 800, 800
BG = (48, 128, 255)
sc = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()

fps = 1000
running = True

btn_w = 50
btn_h = 50
btn_r = 15
btn_m = 15
btn_bg = 'blue'
btn_fg = 'white'
btn_abg = 'lime'
btn_font = pygame.font.SysFont('Arial', 30, bold=True)

pygame.display.set_caption('Hangman Game')
pygame.display.set_icon(pygame.image.load('icon/icon.png'))

def get_indexes_of_letter(word, letter):
    indexes = []
    for i in range(len(word)):
        if word[i] == letter:
            indexes.append(i)
    return indexes

def on_key_down(key):
    global finded, errors, game_over, game_won
    if key != 'reset':
        if key in word:
            if not key in finded:
                indexes = get_indexes_of_letter(word, key)
                for i in indexes:
                    finded[i] = key
                if '_' not in finded:
                    game_won = True
        else:
            errors += 1
            if errors > 8:
                game_over = True
    else:
        restart()

def restart():
    global finded, errors, game_over, game_won, word
    errors = 0
    word = get_random_word()
    finded = ['_' for _ in range(len(word))]
    game_over = False
    game_won = False
    for key in keyboard:
        key.enable = True

class Button:
    def __init__(self, x, y, w, h, r, bg, fg, abg, onclick, args, text, font = pygame.font.SysFont('Arial', 14, bold=True)) -> None:
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.r = r
        self.bg = bg
        self.fg = fg
        self.abg = abg
        self.dbg = bg
        self.text = text
        self.font = font
        self.onclick = onclick
        self.args = args
        self.can_run = True
        self.enable = True

    def draw(self, surface):
        self.check_onclick()
        pygame.draw.rect(surface, self.bg, (self.x, self.y, self.w, self.h), border_radius=self.r)
        render_font = self.font.render(self.text, False, self.fg)
        fw, fh = self.font.size(self.text)
        if fw > self.w:
            x = 5
        else:
            x = round((self.w-fw)/2)

        if fh > self.h:
            y = 5
        else:
            y = round((self.h-fh)/2)

        surface.blit(render_font, (self.x+x, self.y+y))

    def check_onclick(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.enable:
            if self.x <= mouse_x <= self.x+self.w and self.y <= mouse_y <= self.y+self.h:
                self.bg = self.abg
                if self.can_run:
                    if self.onclick != restart:
                        self.enable = False
                    self.onclick(*self.args)
                self.can_run = False
                return
        if not self.enable:
            self.bg = self.abg
            return
        self.bg = self.dbg
        self.can_run = True

words_file = open('dict/words.txt', 'r')
words = words_file.read().split('\n')

def get_random_word():
    return choice(words)

word = get_random_word()
finded = ['_' for _ in range(len(word))]
font4word = pygame.font.SysFont('Arial', 60, bold=True)
game_over = False
game_won = False

errors = 0

font4lose = pygame.font.SysFont('Arial', 70, bold=True)
lose_title = "You Lose!"
won_title = "You Won!"

keys = [['q','w','e','r','t','y','u','i','o','p'],
        ['a','s','d','f','g','h','j','k','l'],
        ['z','x','c','v','b','n','m', 'reset']]

kb_s_x = 80
kb_s_y = 550

keyboard = []

for i, line in enumerate(keys):
    for j, key in enumerate(line):
        if i != 1:
            btn_x = kb_s_x + btn_w*j+btn_m*j
        else:
            btn_x = kb_s_x + btn_w // 2 + btn_w*j+btn_m*j
        btn_y = kb_s_y + btn_h*i+btn_m*i
        if key == 'reset':
            btn = Button(btn_x, btn_y, 3*btn_w+2*btn_m, btn_h, btn_r, btn_bg, btn_fg, btn_abg, on_key_down, args=(key, ), text=key.upper(), font=btn_font)
        else:
            btn = Button(btn_x, btn_y, btn_w, btn_h, btn_r, btn_bg, btn_fg, btn_abg, on_key_down, args=(key, ), text=key.upper(), font=btn_font)
        keyboard.append(btn)

restart_button = Button(round((WIDTH - 200)/2), 720, 200, 70, 20, btn_bg, btn_fg, btn_abg,restart, args=(), text="RESTART", font=btn_font)

hm_head_r = 50
drawings = [
    ['circle', (sc, (0, 0, 0), (200+round((400-2*hm_head_r+2*hm_head_r)/2), 40+50+hm_head_r), hm_head_r, 5)],
    ['line', (sc, (0, 0, 0), (WIDTH//2, 185), (WIDTH//2, 320), 5)],
    ['line', (sc, (0, 0, 0), (WIDTH//2, 220), (WIDTH//2-80, 300), 5)],
    ['line', (sc, (0, 0, 0), (WIDTH//2, 220), (WIDTH//2+80, 300), 5)],
    ['line', (sc, (0, 0, 0), (WIDTH//2, 320), (WIDTH//2-80, 400), 5)],
    ['line', (sc, (0, 0, 0), (WIDTH//2, 320), (WIDTH//2+80, 400), 5)],
    ['line', (sc, (0, 0, 0), (WIDTH//2-20, 120), (WIDTH//2-10, 140), 5)],
    ['line', (sc, (0, 0, 0), (WIDTH//2+10, 120), (WIDTH//2+20, 140), 5)],
    ['line', (sc, (0, 0, 0), (WIDTH//2-20, 160), (WIDTH//2+20, 160), 5)],
]


while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False

    sc.fill(BG)

    pygame.draw.rect(sc, (255, 255, 255), (200, 40, 400, 400))
    pygame.draw.line(sc, (0, 0, 0), (220, 60), (220, 420), 5)
    pygame.draw.line(sc, (0, 0, 0), (220, 60), (400, 60), 5)
    pygame.draw.line(sc, (0, 0, 0), (400, 60), (400, 90), 5)

    if not game_over:
        if game_won:
            clr = (16, 255, 16)
            losefx, losefy = font4lose.size(won_title)
            losex = round((WIDTH - losefx) / 2)
            losey = kb_s_y
            rlosef = font4lose.render(won_title, False, clr)
            sc.blit(rlosef, (losex, losey))
            restart_button.draw(sc)
            showed_word = word
        else:
            for button in keyboard:
                button.draw(sc)
            showed_word = ''.join(finded)
            clr = (16, 16, 16)
    else:
        clr = (255, 16, 16)
        losefx, losefy = font4lose.size(lose_title)
        losex = round((WIDTH - losefx) / 2)
        losey = kb_s_y
        rlosef = font4lose.render(lose_title, False, clr)
        sc.blit(rlosef, (losex, losey))
        restart_button.draw(sc)
        showed_word = word

    f4w_w, f4w_h = font4word.size(showed_word)
    rf = font4word.render(showed_word, False, clr)
    fx, fy = round((WIDTH - f4w_w)/2), 460
    sc.blit(rf, (fx, fy))

    for _type, params in drawings[:errors]:
        if _type == 'line':
            pygame.draw.line(*params)
        else:
            pygame.draw.circle(*params)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
