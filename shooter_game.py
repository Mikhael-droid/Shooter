from pygame import *
from random import randint
from time import time as timer

img_back = "galaxy.jpg" #Background Game
img_hero = "rocket.png" #Player
img_enemy = "ufo.png" #Enemy
img_bullet = "bullet.png" #Peluru
img_asteroid = "asteroid.png" #Enemy ke-2

#Layar Game
lebar = 700
tinggi = 500
display.set_caption("Shooter")
window = display.set_mode((lebar, tinggi))
background = transform.scale(image.load(img_back),(lebar, tinggi))

#Musik Latar
mixer.init()
mixer.music.load("otonoke.mp3")
mixer.music.play()

#Fire sound
fire_sound = mixer.Sound("fire.ogg")

#Font and Label
font.init()
font1 = font.SysFont("Calibri", 25)
font2 = font.SysFont("Arial", 80)
menang = font2.render("You Win!", True, (255, 255, 255))
kalah = font2.render("You Lose!", True, (180, 0, 0))

score = 0 #Menghitung jumlah UFO yang ditembak
lost = 0 #Menghitung jumlah UFO yang tembus
goal = 5 #Menghitung target
max_lost = 10 #Menghitung jumlah miss
life = 3 #Nyawa pesawat

#Class Sprite
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_w, size_h, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_w, size_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Class Player
class Player(GameSprite):
    def gerak(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < lebar -80:
            self.rect.x += self.speed   
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < tinggi - 100:
            self.rect.y += self.speed
    #Membuat metode menembak
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

#Class Enemy
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > tinggi:
            self.rect.x = randint(80, lebar-80)
            self.rect.y = 0
            lost = lost + 1

#Class Peluru
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #Menghilang jika mencapai tepi layar
        if self.rect.y < 0:
            self.kill()

#Fungsi Reset Game
def reset_game():
    global score, lost, finish, monsters, bullets, asteroids
    score = 0
    lost = 0
    finish = False
    monsters.empty()
    bullets.empty()
    asteroids.empty()
    for i in range(1, 6):
        monster = Enemy(img_enemy, randint(80, lebar-80), -40, 80, 50, randint(3, 7))
        monsters.add(monster)
    for i in range(1, 4):
        asteroid = Enemy(img_asteroid, randint(30, lebar-30), -40, 80, 50, randint(1, 5))
        asteroids.add(asteroid)
    Pesawat.rect.x = 5
    Pesawat.rect.y = tinggi-100

#Objek Game
Pesawat = Player(img_hero, 5, tinggi-100, 80, 100, 25)

#Membuat Group Enemy
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, lebar-80), -40, 80, 50, randint(3, 7))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Enemy(img_asteroid, randint(30, lebar-30), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

#Membuat Group Peluru
bullets = sprite.Group()


#Loop Game
finish = False
run = True

#Membuat variable reload dan waktu relaod
reload_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        #Menggunakan tombol untuk menembak
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 6 and reload_time == False:
                    num_fire += 1
                    fire_sound.play()
                    Pesawat.fire()
                #Memeriksa tembakan lebih dari 6 kali
                if num_fire >= 6 and reload_time == False:
                    last_time = timer()
                    reload_time = True
            #Menggunakan R untuk reset dan Q untuk keluar
            elif e.key == K_r and finish:
                reset_game()
            elif e.key == K_q and finish:
                run = False

    if not finish:
        window.blit(background,(0,0))
        Pesawat.gerak()
        monsters.update()
        bullets.update() 
        asteroids.update()

        Pesawat.draw()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        #membuat reload time
        if reload_time == True:
            now_time = timer() #membaca waktu
            if now_time - last_time < 3:
                reload = font1.render('wait, reload...reload...reload', True, (255,255,255))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                reload_time = False

        #Menulis lost
        text_lose = font1.render('Miss:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        #Memeriksa Tabrakan peluru dan ufo
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, lebar-80), -40, 80, 50, randint(3, 7))
            monsters.add(monster)

        #Memeriksa Tabrakan peluru dan asteroid
        collides = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides:
            score += 1
            asteroid = Enemy(img_asteroid, randint(30, lebar-30), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)

        #Memeriksa Tabrakan pesawat dan ufo
        if sprite.spritecollide(Pesawat, monsters, False) or sprite.spritecollide(Pesawat, asteroids, False) or lost >= max_lost:
            finish = True
            window.blit(kalah, (200, 200))

        #Memerikasa kondisi menang
        if score >= goal:
            finish = True
            window.blit(menang, (200, 200))

        #membuat warna untuk tampilan nyawa pesawat
        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)
        text_life = font2.render(str(life), True, life_color)
        window.blit(text_life, (650,10))

       #menulis score
        text_score = font1.render('Score: ' + str(score), 1, (255,255,255))
        window.blit(text_score, (10, 20))
    else:
        score = 0
        lost = 0
        num_fire = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        #Menampilkan R untuk reset dan Q untuk keluar
        reset_quit_label = font1.render("R untuk reset, Q untuk keluar", True, (255, 255, 255))
        window.blit(reset_quit_label, (200, 300))

    display.update()
    time.delay(60)