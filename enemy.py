import pygame
import math

from setup import *
from projectile import Projectile
from tower import Tower


class Enemy:
    def __init__(self, path, health = 30, range = 80, name = "noname enemy", enemy_image = "sprites/enemy.png", own_speed=2 ):
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print(path)
        self.path = path
        self.x, self.y = self.path[0]
        self.path_index = 0
        self.speed = own_speed
        self.health = health
        self.initial_health = health
        self.hits_taken = 0
        self.projectiles = []
        self.range = range
        self.cooldown = 0
        self.cooldown_rate = 5
        self.name = name
        self.enemy_image = pygame.image.load(enemy_image)
        self.enemy_image = pygame.transform.scale(self.enemy_image, (40, 40))  # Resize the image if necessary


    def in_range(self, enemy):
        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
        return dist <= self.range

    def draw(self, surface):
        pygame.draw.circle(surface, BLUE, (self.x, self.y), self.range, 1)
        surface.blit(self.enemy_image, (self.x - 20, self.y - 20))
        health_text = font.render("h: " + str(self.health), True, BLACK)
        range_text = font.render("r: " + str(self.range), True, BLACK)
        surface.blit(health_text, (self.x + 25, self.y - 20))
        surface.blit(range_text, (self.x + 25, self.y))

        for projectile in self.projectiles:
            projectile.draw(surface)

    def update(self, towers):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.path_index += 1
            else:
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed
        else:
            self.path_index = 0

        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            #--- check the towers in the order of the list, pick the first tower in rangne
            for tower in towers:
                if self.in_range(tower):
                    self.shoot_back(tower)
                    self.cooldown = self.cooldown_rate  # cooldown period
                    break

        #--- check if you collided with a tower
        for tower in towers:
            if self.get_rect().colliderect(tower.get_rect()):
                print(f"  - Enemy object check: Enemy \"{self.name}\" collided with tower \"{tower.name}\" with health {tower.health}, hit with {self.health}")
                acc = tower.health
                tower.health -= self.health
                self.health -=  acc


        for projectile in self.projectiles[:]:
            if projectile.update():
                print("  - YYY: Removing projectile directed towards: " + projectile.target.name)
                self.projectiles.remove(projectile)

        if self.health <= 0:
            return True
        return False

    def take_hit(self):
        self.hits_taken += 1

    def get_rect(self):
        return pygame.Rect(self.x - 20, self.y - 20, 40, 40)

    def get_health(self):
        return self.health


    def shoot_back(self, tower):
        print("  - YYY: Shooting against tower: " + tower.name)
        tower_x, tower_y = tower.x, tower.y
        projectile = Projectile(self.x, self.y, tower, speed=5, is_enemy=True)
#        projectile.target = Tower(tower_x, tower_y)
        self.projectiles.append(projectile)


class EnemyTank(Enemy):
    def __init__(self, path, health=30, range=80, name = "noname enemy", enemy_image = "sprites/enemy.png", own_speed=2 ):
        super().__init__(path, health, range, name, enemy_image, own_speed)

class Mario(Enemy):
    def __init__(self, path, health=5, range=80, name="noname enemy", enemy_image="sprites/mario.png", own_speed=4):
        super().__init__(path, health, range, name, enemy_image, own_speed)