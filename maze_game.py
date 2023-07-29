from pygame import *
display.set_caption('Maze game')

GREEN = (0, 255, 0)

window_width = 700
window_length = 500

window  = display.set_mode((window_width,window_length))
picture = transform.scale(image.load('wall.jpg'),(80,180))
lose = transform.scale(image.load('lose.jpg'),(700,500))
win = transform.scale(image.load('win.jpg'),(700,500))

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w,h,x,y):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        
        if player1.rect.x <= window_width - 100 and player1.x_speed >0 or player1.rect.x >= 0 and player1.x_speed < 0:
            self.rect.x += self.x_speed
         
        
        platforms_touched = sprite.spritecollide(self, barriers, False)
        
        if self.x_speed >0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed <0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
                
        if player1.rect.y <= window_length-100 and player1.y_speed > 0 or player1.rect.y >= 0 and player1.y_speed < 0:
            self.rect.y += self.y_speed
            
        platforms_touched = sprite.spritecollide(self, barriers, False)
                
        if self.y_speed >0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed <0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
        
    def fire(self):
        bullet = Bullet('bullet.png', 15, 20, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image , player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= window_width - 100:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
            
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, bullet_speed):
        GameSprite.__init__(self, player_image , player_x, player_y, size_x, size_y)
        self.speed = bullet_speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > window_width + 10:
            self.kill()


wall_1 = GameSprite('wall.jpg',80,180,200,250)
wall_2 = GameSprite('wall.jpg',80,150,200,250)
wall_3 = GameSprite('wall.jpg',80, 100,350,30)

player1 = player('skull.png', 100,100, 50,50,0,0)
final = GameSprite('cherry2.jpg',100,100,650, 175)
enemy = Enemy('ghost.jpg',100,100,650,50, 5)

barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)
barriers.add(wall_3)  

bullets = sprite.Group()
monsters = sprite.Group()
monsters.add(enemy)


run = True
finish = False
while run:
    time.delay(50)
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_a:
                player1.x_speed -= 5
            if e.key == K_d:
                player1.x_speed += 5
            if e.key == K_w:
                player1.y_speed -= 8
            if e.key == K_s:
                player1.y_speed += 8
            if e.key == K_SPACE:
                player1.fire()
        
        if e.type == KEYUP:
            if e.key == K_a:
                player1.x_speed = 0
            if e.key == K_d:
                player1.x_speed = 0
            if e.key == K_w:
                player1.y_speed = 0
            if e.key == K_s:
                player1.y_speed = 0
        
        if e.type == QUIT:
            run = False
    
    if finish != True:
        window.blit(picture, (0,0))
        window.fill((0,0,0))
        barriers.draw(window)
        player1.reset()
        player1.update()
        enemy.reset()
        enemy.update()
        final.reset()
        bullets.update()
        bullets.draw(window)       
        
    sprite.groupcollide(bullets, barriers, True, False)
    sprite.groupcollide(bullets, monsters, True, True)
    if sprite.collide_rect(player1, final):
        finish = True
        window.blit(win,(0,0))
    if sprite.collide_rect(player1, enemy):
        finish = True
        window.blit(lose,(0,0))
            
        
                
    display.update()