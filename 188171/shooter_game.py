import pygame
from pygame import *
from random import randint
pygame.init()
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (1, 0, 0))
font2 = font.SysFont('Arial', 36)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
click_sound = mixer.Sound('button_click.mp3')
lose_sound = mixer.Sound('lose.mp3')
img_asteroid = "asteroid.png"
img_back = "galaxy.png"
img_bullet = "bullet.png"
img_hero = "rocket.png"
img_enemy = "ufo.png"
menu_img = (150, 150, 150)
score = 0
goal = 15
lost = 0
global max_lost
max_lost = 7
clock = pygame.time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 60, 75, -15)
        bullets.add(bullet)
        

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

def start_menu():
    import pygame  # Importing pygame within the function scope
    pygame.font.init()
    pygame.mixer.init()
    pygame.mixer.music.load('space.ogg')
    pygame.mixer.music.play()
    fire_sound = pygame.mixer.Sound('fire.ogg')
    
    menu_font = pygame.font.SysFont('Arial', 50)
    menu_text = menu_font.render('Space Defence', True, (255, 255, 255))
    start_text = pygame.font.SysFont('Arial', 36).render('Start', True, (255, 255, 255))
    exit_text = pygame.font.SysFont('Arial', 36).render('Exit', True, (255, 255, 255))
    hard_dif_text = pygame.font.SysFont('Arial', 36).render('Hardcore Mode', True, (255, 255, 255))
    menu_rect = menu_text.get_rect(center=(win_width // 2, win_height // 2 - 50))
    start_rect = start_text.get_rect(center=(win_width // 2, win_height // 2 + 50))
    exit_rect = exit_text.get_rect(center=(win_width // 2, win_height // 2 + 100))
    hard_dif_rect = hard_dif_text.get_rect(center=(win_width // 2, win_height // 2 + 150))
    global max_lost
    clock = pygame.time.Clock()  # Define the clock object
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    click_sound.play()
                    return True
                elif exit_rect.collidepoint(mouse_pos):
                    click_sound.play()
                    pygame.quit()
                    quit()
                elif hard_dif_rect.collidepoint(mouse_pos):
                    click_sound.play()
                    max_lost = 1
                    hard_dif_text = pygame.font.SysFont('Arial', 36).render('Hardcore Mode Enabled', True, (255, 0, 0))
                    pygame.display.update()

        window.blit(menu_text, menu_rect)
        window.blit(start_text, start_rect)
        window.blit(exit_text, exit_rect)
        window.blit(hard_dif_text, hard_dif_rect)
        pygame.display.update()
        clock.tick(45)



win_width = 1280
win_height = 720
display.set_caption("Space Defence")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height)) 
ship = Player(img_hero, 5, win_height - 100, 150, 130, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 100, 80, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

finish = False

while True:
    if start_menu():
        finish = False
        lost = 0
        score = 0
        
        while not finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        fire_sound.play()
                        ship.fire()
                        
            asteroids = sprite.Group()
            window.blit(background, (0, 0))
            ship.update()
            monsters.update()
            bullets.update()
            ship.reset()
            monsters.draw(window)
            bullets.draw(window)
            
            collides = pygame.sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                score += 1
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 100, 80, randint(1, 5))
                monsters.add(monster)
            
            if pygame.sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
                finish = True
                window.blit(lose, (200, 200))
                lose_sound.play()
                lost = 0
                pygame.display.update()
                pygame.time.delay(2000)  # Delay for 2 seconds before returning to the main menu
                break  # Exit the inner loop and return to the main menu
            if score >= goal:
                finish = True
                window.blit(win, (200, 200))
                pygame.display.update()
                pygame.time.delay(1000)  # Delay for 2 seconds before returning to the main menu
                break  # Exit the inner loop and return to the main menu

            text = font2.render("Score: " + str(score), 1, (255, 255, 255))
            window.blit(text, (10, 20))
            
            text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
            window.blit(text_lose, (10, 50))
            
            pygame.display.update()

            clock.tick(30)