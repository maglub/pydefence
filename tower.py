import pygame
import math

from setup import *
from projectile import Projectile


# Load images

class Tower:
    def __init__(self, x, y, health = 100, name = "Noname tower", draw_range = True):
        self.x = x
        self.y = y
        self.range = 150
        self.cooldown = 0
        self.projectiles = []
        self.health = health
        self.name = name
        self.draw_perimeter = False
        self.draw_range = draw_range
        self.spawnable = False
        self.angle = 0
        self.tower_image = pygame.image.load("sprites/gun_turret2.png")
        self.tower_image = pygame.transform.scale(self.tower_image, (80, 80))  # Resize the image if necessary


    def draw_range_background(self, surface):
        if self.draw_range:
          pygame.draw.circle(surface, RANGE_COLOR, (self.x + 15, self.y + 15), self.range - 1)

    def draw_range_frame(self, surface):
        if self.draw_range:
          pygame.draw.circle(surface, MID_GREEN, (self.x + 15, self.y + 15), self.range , 1)

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.tower_image, self.angle)
        new_rect = rotated_image.get_rect(center=self.tower_image.get_rect(topleft=(self.x - 25, self.y - 25)).center)
        surface.blit(rotated_image, new_rect.topleft)

        #surface.blit(tower_image, (self.x - 25, self.y - 25))
        health_text = font.render(str(self.health), True, BLACK)
        surface.blit(health_text, (self.x + 50, self.y - 20))
        for projectile in self.projectiles:
            projectile.draw(surface)
        if self.draw_perimeter:
          pygame.draw.circle(surface, GREEN if self.spawnable else RED, (self.x + 15, self.y + 15 ), 40, 2)


    def update(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            for enemy in enemies:
                if self.in_range(enemy):
                    self.shoot(enemy)
                    self.cooldown = 3  # cooldown period
                    break

        for projectile in self.projectiles[:]:
            if projectile.update():
                self.projectiles.remove(projectile)

    def can_spawn(self, towers):
        #--- you can't place a tower too close to another tower
        ret_can_spawn = True
        if len(towers)>1:
          for tower in towers[1:]:
            dist = math.hypot(tower.x - self.x, tower.y - self.y)
            if dist<=60:
              ret_can_spawn = False

        return ret_can_spawn

        
    def in_range(self, enemy):
        dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
        return dist <= self.range

    def shoot(self, enemy):
        # Calculate the angle to the enemy
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        self.angle = math.degrees(math.atan2(-dy, dx))  # Calculate the angle in degrees

        projectile = Projectile(self.x, self.y, enemy)
        self.projectiles.append(projectile)

    def get_rect(self):
        return pygame.Rect(self.x - 20, self.y - 20, 40, 40)

    def reduce_health(self, health):
        self.health -= health

    def hit_health(self, enemy):
        self.health -= enemy.health

    def inherit_health(self, enemy):
        if self.health <= HEALTH_MAX:
          self.health += enemy.initial_health
        if self.health > HEALTH_MAX:
           self.health = HEALTH_MAX



