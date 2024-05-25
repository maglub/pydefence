import math

from setup import *

projectile_image = pygame.Surface((10, 10))
projectile_image.fill(BLUE)

enemy_projectile_image = pygame.Surface((10, 10))
enemy_projectile_image.fill(BLACK)


class Projectile:
    def __init__(self, x, y, target, speed=15, is_enemy=False, power = 1):
        self.x = x
        self.y = y
        self.target = target
        self.speed = speed
        self.is_enemy = is_enemy
        self.power = 5 if target.name == "Master tower" else 1

        if is_enemy:
          print(f"  - ZZZ: Creating new projectile targeting: {self.target.name} with power {self.power}")

    def update(self):
        if self.target is not None:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy)
            if dist > self.speed:
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed
            else:
                print("  - ZZZ Hit: " + self.target.name)
                if self.is_enemy:
                    self.target.health -= self.power
                else:
                    self.target.health -= self.power
                return True
        return False

    def draw(self, surface):
        surface.blit(projectile_image if not self.is_enemy else enemy_projectile_image, (self.x - 5, self.y - 5))
