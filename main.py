import pygame
import agent
import math
import itertools
from multiprocessing import Pool


# Set the dimensions of the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
pygame.font.init()
pygame.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
#game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.time.Clock().tick(2000)
population_size = 20
agents = [agent.Agent(200, 300, 800, 600) for _ in range(population_size)]


def run_simulation(agent1, agent2, seconds, x):
    # Initialize Pygame
    agent1.x = 200
    agent1.y = 300 
    agent2.x = 600
    agent2.y = 300
    agent1.set_opponent(agent2)
    agent2.set_opponent(agent1)

    #text_surface = my_font.render('Simulation '+ str(x) , False, (255, 0, 0))
    
    ticks = 0  # Initialize tick counter
    ticks_per_second = 1000
    #start_ticks=pygame.time.get_ticks()
    
    running = True
    while running:

        sec = ticks / ticks_per_second
        
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False'''


         # Update game state here
        agent1.move()
        agent2.move()


        #game_window.fill((0, 0, 0))

        
        #game_window.blit(text_surface, (10,10))
        
        for projectile in agent1.projectiles:
            projectile.move()
            #projectile.draw(game_window)

            # Collision with Agent2
            dist = math.sqrt((projectile.x - agent2.x)**2 + (projectile.y - agent2.y)**2)
            if dist < agent2.radius + 5:  # 5 is the radius of the projectile
                agent1.delProjectile(projectile)
                print("Agent1's bullet hit Agent2!")
                agent1.times_Hit()
                agent2.agent_Hits()
                

            if (projectile.x < 0 or projectile.x > WINDOW_WIDTH or
            projectile.y < 0 or projectile.y > WINDOW_HEIGHT):
                agent1.delProjectile(projectile)
                
        for projectile in agent2.projectiles:
            projectile.move()
            #projectile.draw(game_window)

            dist = math.sqrt((projectile.x - agent1.x)**2 + (projectile.y - agent1.y)**2)
            if dist < agent1.radius + 5:  # 5 is the radius of the projectile
                agent2.delProjectile(projectile)
                print("Agent2's bullet hit Agent1!")
                agent2.times_Hit()
                agent1.agent_Hits()
                

            if (projectile.x < 0 or projectile.x > WINDOW_WIDTH or
            projectile.y < 0 or projectile.y > WINDOW_HEIGHT):
                agent2.delProjectile(projectile)

        # Render graphics here
        '''
        pygame.draw.circle(game_window, (255, 0, 0), (int(agent1.x), int(agent1.y)), agent1.radius)
        pygame.draw.circle(game_window, (0, 0, 255), (int(agent2.x), int(agent2.y)), agent2.radius)

        pygame.draw.line(game_window, (255, 0, 0), (agent1.x, agent1.y), (agent1.front[0], agent1.front[1]))
        pygame.draw.line(game_window, (0, 0, 255), (agent2.x, agent2.y), (agent2.front[0], agent2.front[1]))
        pygame.display.flip()
        '''
        ticks += 1
        if sec > seconds:
            running = False

    
count =0 
for agent1, agent2 in itertools.combinations(agents, 2):
    print(count)
    run_simulation(agent1,agent2,10,count)
    count+=1

for ag in agents:
    print(ag.agentHits-ag.timesHit)


pygame.quit()