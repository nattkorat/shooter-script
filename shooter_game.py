"""This is the code script """
from time import time as time_counter
from pygame import *
from random import randint

font.init()

# ! global variables
score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 10:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < 700 - 80:
            self.rect.x += self.speed

    def fire(self):
        new_bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 50, 15)
        bullets.add(new_bullet)
        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost # TODO: call the global variable

        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player("rocket.png", 350, 400, 65, 65, 10)

enemies = sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png", randint(80, 620), 50, 65, 65, randint(1, 3))
    enemies.add(enemy)

# asteriod obstacle
asteriods = sprite.Group()
for i in range(3):
    asteriod = Enemy("asteroid.png", randint(80, 620), 50, 65, 65, randint(1, 2))
    asteriods.add(asteriod)

# group of the bullets
bullets = sprite.Group()

window = display.set_mode((700, 500))
background = transform.scale(
    image.load("galaxy.jpg"),
    (700, 500)
)

# TODO: music backgrond
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play(-1)

fire_sound = mixer.Sound("fire.ogg")

clock = time.Clock()
game = True
finish = False
life = 3
reload = False
num_bullets = 0

while game:
    if not finish:
        window.blit(background, (0, 0))
        player.reset()
        player.update()

        # handle with the enemies
        enemies.draw(window)
        asteriods.draw(window)
        enemies.update()
        asteriods.update()


        # handle with bullets
        bullets.draw(window)
        bullets.update()

        # statistics
        score_stat = font.SysFont("Arail", 30).render("Score: " + str(score), 1, (255, 255, 255))
        lost_stat = font.SysFont("Arail", 30).render("Missed: " + str(lost), 1, (255, 255, 255))
        life_stat = font.SysFont("Arail", 30).render("Lives: " + str(life), 1, (255, 255, 255))
        window.blit(score_stat, (10, 10))
        window.blit(lost_stat, (10, 40))
        window.blit(life_stat, (10, 70))

        if not reload:
            collides_en = sprite.spritecollide(player, enemies, True)
            collides_as = sprite.spritecollide(player, asteriods, True)

            if collides_en:
                life -= 1
                reload = True
                event_time = time_counter()
                new_enemy = Enemy("ufo.png", randint(80, 620), 50, 65, 65, randint(1, 3))
                enemies.add(new_enemy)
            
            if collides_as:
                life -= 1
                reload = True
                event_time = time_counter()
                new_enemy = Enemy("asteroid.png", randint(80, 620), 50, 65, 65, randint(1, 3))
                enemies.add(new_enemy)
        
        # draw the word reload to the screen
        if reload:
            reload_text = font.SysFont("Arail", 20).render(
                "Wait!, Reloading!.....",
                1,
                (255, 30, 50)
            )
            window.blit(reload_text, (300, 400))
            new_time = time_counter()
            if new_time - event_time >= 1:
                reload = False


        # lost/win condtion
        if lost > 5 or life <= 0: # lose
            finish = True
            lost_text = font.SysFont(None, 60).render("YOU LOSE!", 1, (255, 0, 0))
            window.blit(lost_text, (220, 200))
            mixer.music.stop()
        
        if score >= 10: # win
            finish = True
            lost_text = font.SysFont(None, 60).render("YOU WIN!", 1, (20, 50, 250))
            window.blit(lost_text, (220, 200))
            mixer.music.stop()
        
        collides = sprite.groupcollide(enemies, bullets, True, True)
        for collide in collides:
            score += 1
            new_enemy = Enemy("ufo.png", randint(80, 620), 50, 65, 65, randint(1, 3))
            # add the new enemy to the group
            enemies.add(new_enemy)


    for e in event.get():
        if e.type == QUIT:
            game = False
            
        if e.type == KEYDOWN:
            if e.key == K_SPACE and not finish and not reload:
                player.fire()
                num_bullets += 1
                fire_sound.play()
                if num_bullets >= 5:
                    event_time = time_counter()
                    num_bullets = 0
                    reload = True # need to reload the bullets
    clock.tick(60)
    display.update()