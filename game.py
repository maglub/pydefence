import pygame
import random

from setup import *
from tower import Tower
from enemy import *
from projectile import Projectile

# Initialize Pygame
pygame.init()


# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Tower Defense")



# Define the path for enemies
path = [(100, 100), (700, 100), (700, 500), (1024, 800)]

waves = [
    {
        "num_enemies": 10,
        "path": [(100, 100), (700, 100), (700, 500), (1024, 800)]
    },
    {
        "num_enemies": 40,
        "path": [(100, 100), (800, 100), (100, 400), (800, 400), (100, 800), (1024, 800)]
    },
    {
        "num_enemies": 40,
        "path": [(100, 100), (200, 100), (200, 400), (400, 400), (1024, 800)]
    }
]

def wait_for_space():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def run_wave(wave):
    clock = pygame.time.Clock()
    towers = [Tower(400, 300, name = "Master tower")]
    main_tower = towers[0]
    enemies = []
    game_frame = 0
    game_round = 1
    enemy_num = 1
    score = 0
    total_enemies = 0
    max_enemies = 50
    killed_enemies = 0
    
    running = True
    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            towers[0].y -= 3
        if keys[pygame.K_DOWN]:
            towers[0].y += 3
        if keys[pygame.K_LEFT]:
            towers[0].x -= 3
        if keys[pygame.K_RIGHT]:
            towers[0].x += 3
        if keys[pygame.K_d]:
            #--- check if you can spawn 
            main_tower.spawnable = main_tower.can_spawn(towers)
        
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_q:
                running = False
              if event.key == pygame.K_r:
                main_tower.draw_range = not main_tower.draw_range
                if len(towers)>1:
                   for tower in towers[1:]:
                      tower.draw_range = main_tower.draw_range
              if event.key == pygame.K_d:
                main_tower.draw_perimeter = True
                
          if event.type == pygame.KEYUP:
              #--- d => Drop
              if event.key == pygame.K_d:
                main_tower.draw_perimeter = False
                print("Key 'd' is pressed")
                if towers[0].health > HEALTH_SPAWN:
                  #--- only allow to spawn a tower if is actually allowed (spawnable)
                  if main_tower.spawnable:
                    towers.append(Tower(main_tower.x, main_tower.y, health = HEALTH_SPAWN, name = "T" + str(len(towers)), draw_range = main_tower.draw_range ))
                    main_tower.reduce_health(HEALTH_SPAWN)

        #--- magic contant 100 is setting the pace. Drop new enemies every 100 frames
        if game_frame % 100 == 0:
            game_round += 1
            if total_enemies < waves[wave]['num_enemies']:
                enemy_class = random.choice([Mario, EnemyTank, Beast])
                enemies.append(enemy_class(waves[wave]["path"], int(0 + min(10 * game_round, 200)), 30 + random.randint(0, 100)))
                total_enemies += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        #--- blit the dashboard
        screen.fill(SAND)


        score_text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, (200,20))
        round_text = font.render("Round: " + str(game_round) + " (" + str(game_frame) + ")", True, BLACK)
        screen.blit(round_text, (20,20))
        total_enemies_text = font.render("Enemies: " + str(total_enemies) + " / killed: " + str(killed_enemies), True, BLACK)
        screen.blit(total_enemies_text, (300,20))
        health_text = font.render("Health: " + str(towers[0].health), True, BLACK)
        screen.blit(health_text, (500,20))


        for tower in reversed(towers):
            tower.draw_range_frame(screen)

        for tower in reversed(towers):
            tower.draw_range_background(screen)

        for tower in reversed(towers):
            tower.update(enemies)
            tower.draw(screen)
            if tower.health < 0:
                towers.remove(tower)

        #--- draw the gamefield track
        pygame.draw.lines(screen, LIGHT_GRAY, False, waves[wave]['path'], 20)
        for point in waves[wave]['path']:
            pygame.draw.circle(screen, LIGHT_GRAY, point, 20)

        for enemy in enemies[:]:
#            if enemy.get_rect().colliderect(main_tower.get_rect()):
#                print(f"  * MAIN: Enemy {enemy} collided with tower {main_tower} with health {main_tower.health}, hit with {enemy.health}")
#                #--- remove the health of the Tower by the health of the enemy
#                towers[0].hit_health(enemy)
#                enemies.remove(enemy)
#                killed_enemies += 1
            if enemy.update(towers):
                score += 10
                #--- if an enemy dies, no matter how, the main_tower inherits the power of the enemy
                main_tower.inherit_health(enemy)
                print("  - Increase health")
                enemies.remove(enemy)
                killed_enemies += 1

            enemy.draw(screen)

        if main_tower.health <= 0:
          running = False
          game_over_text = font.render("Game over!", True, BLACK)
          screen.blit(game_over_text, (500,500))
          pygame.display.flip()
          # Sleep for 2 seconds
          pygame.time.delay(3000)
          return False

        if len(enemies) == 0:
            running = False

        pygame.display.flip()
        clock.tick(FPS)
        game_frame += 1

    return True

#==============================================================
# MAIN
#==============================================================
def main():
    wave = 0

    while wave < len(waves) and run_wave(wave):
      wave += 1

    pygame.quit()

if __name__ == "__main__":
    main()
