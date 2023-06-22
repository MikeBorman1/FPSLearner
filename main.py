import pygame
import agent
import math
import itertools
import random
import matplotlib.pyplot as plt 
import pickle
import pygame
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
population_size = 10



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
        

         # Update game state here
        agent1.move()
        agent2.move()

        
        for projectile in agent1.projectiles:
            projectile.move()
            

            # Collision with Agent2
            dist = math.sqrt((projectile.x - agent2.x)**2 + (projectile.y - agent2.y)**2)
            if dist < agent2.radius + 5:  # 5 is the radius of the projectile
                agent1.delProjectile(projectile)

                agent1.hit()
                
                

            if (projectile.x < 0 or projectile.x > WINDOW_WIDTH or
            projectile.y < 0 or projectile.y > WINDOW_HEIGHT):
                agent1.delProjectile(projectile)
                
        for projectile in agent2.projectiles:
            projectile.move()
           

            dist = math.sqrt((projectile.x - agent1.x)**2 + (projectile.y - agent1.y)**2)
            if dist < agent1.radius + 5:  # 5 is the radius of the projectile
                agent2.delProjectile(projectile)

                agent2.hit()
                
                

            if (projectile.x < 0 or projectile.x > WINDOW_WIDTH or
            projectile.y < 0 or projectile.y > WINDOW_HEIGHT):
                agent2.delProjectile(projectile)

        
        ticks += 1
        if sec > seconds:
            running = False

def run_simulation_withGraphics(agent1, agent2, seconds):
  # Initialize Pygame

  WINDOW_WIDTH = 800
  WINDOW_HEIGHT = 600
  pygame.init()
  game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  pygame.time.Clock().tick(2000)

  agent1.x = 200
  agent1.y = 300 
  agent2.x = 600
  agent2.y = 300
  agent1.set_opponent(agent2)
  agent2.set_opponent(agent1)

  pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
  my_font = pygame.font.SysFont('Comic Sans MS', 20)
  
  start_ticks=pygame.time.get_ticks()
  blue= 0 
  red = 0
  running = True
  while running:

      
      
      
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False


      # Update game state here
      agent1.move()
      agent2.move()
      sec=(pygame.time.get_ticks()-start_ticks)/1000

      game_window.fill((0, 0, 0))

      
      
      
      for projectile in agent1.projectiles:
          projectile.move()
          projectile.draw(game_window)

          # Collision with Agent2
          dist = math.sqrt((projectile.x - agent2.x)**2 + (projectile.y - agent2.y)**2)
          if dist < agent2.radius + 5:  # 5 is the radius of the projectile
              agent1.delProjectile(projectile)
              blue-=1
              red+=1
              agent1.hit()
              
              

          if (projectile.x < 0 or projectile.x > WINDOW_WIDTH or
          projectile.y < 0 or projectile.y > WINDOW_HEIGHT):
              agent1.delProjectile(projectile)
              
      for projectile in agent2.projectiles:
          projectile.move()
          projectile.draw(game_window)

          dist = math.sqrt((projectile.x - agent1.x)**2 + (projectile.y - agent1.y)**2)
          if dist < agent1.radius + 5:  # 5 is the radius of the projectile
              agent2.delProjectile(projectile)
              red-=1
              blue+=1
              agent2.hit()
              
              

          if (projectile.x < 0 or projectile.x > WINDOW_WIDTH or
          projectile.y < 0 or projectile.y > WINDOW_HEIGHT):
              agent2.delProjectile(projectile)

      # Render graphics here
      
      pygame.draw.circle(game_window, (255, 0, 0), (int(agent1.x), int(agent1.y)), agent1.radius)
      pygame.draw.circle(game_window, (0, 0, 255), (int(agent2.x), int(agent2.y)), agent2.radius)

      pygame.draw.line(game_window, (255, 0, 0), (agent1.x, agent1.y), (agent1.front[0], agent1.front[1]))
      pygame.draw.line(game_window, (0, 0, 255), (agent2.x, agent2.y), (agent2.front[0], agent2.front[1]))
      text_surface = my_font.render('Blue Score: '+ str(blue), False, (0, 0, 255))
      text_surface1 = my_font.render('Red Score: '+ str(red), False, (255, 0, 0))
      game_window.blit(text_surface, (600,10))
      game_window.blit(text_surface1, (10,10))
      pygame.display.flip()
      
      
      if sec > seconds:
        running = False







class GeneticAlgorithm:
    def __init__(self, population_size):
        self.population_size = population_size
        self.population = [agent.Agent(200, 300, 800, 600) for _ in range(population_size)]
        self.history = {'generation': [], 'best': [], 'worst': [], 'average': []}
        #plt.ion()
        #self.fig, self.ax = plt.subplots()
    
    def selection(self):
        # Tournament selection
        parent1 = max(random.sample(self.population, k=5), key=lambda agent: (agent.agentHits-agent.timesHit))
        parent2 = max(random.sample(self.population, k=5), key=lambda agent: (agent.agentHits-agent.timesHit))
        return parent1, parent2

    def replacement(self):
        # Replace the worst individuals in the population with the newly created individuals
        self.population.sort(key=lambda agent: (agent.agentHits-agent.timesHit))
        self.population[:3] = self.new_individuals

    def run_generation(self,generation,numberofgenerations):
        # Run the game for each pair of agents
        count = 0

       
        for agent1, agent2 in itertools.combinations(self.population, 2):

            run_simulation(agent1, agent2, 40, count)
            count += 1
            run_simulation(agent2, agent1, 40, count)
        
        # Selection
        parent1, parent2 = self.selection()
        
        # Crossover
        self.new_individuals = [parent1.crossover(parent2) for _ in range(3)]
        
        # Mutation
        for individual in self.new_individuals:
            individual.mutate()
        
        ga.print_stats(generation)
        # Replacement
        if numberofgenerations -1  == generation :
            self.runSim()
            ga.save_agents('agents2.pkl')   

            return

        self.replacement() 

        for agent in self.population:
            agent.agentHits=0
            agent.timesHit=0 

    def print_stats(self, generation):

        best_agent = max(self.population, key=lambda agent: (agent.agentHits-agent.timesHit))
        worst_agent = min(self.population, key=lambda agent: (agent.agentHits-agent.timesHit))
        scores = [agent.agentHits - agent.timesHit for agent in self.population]
        

        print(f'Generation: {generation}')
        print(f'Best Score: {best_agent.agentHits - best_agent.timesHit}')
        print(f'Worst Score: {worst_agent.agentHits - worst_agent.timesHit}')
        print(f'Average Score: {sum(scores) / len(self.population)}')

        print()

        self.history['generation'].append(generation)
        self.history['best'].append(best_agent.agentHits - best_agent.timesHit)
        self.history['worst'].append(worst_agent.agentHits - worst_agent.timesHit)
        self.history['average'].append(sum(scores) / len(self.population))

        
        
        
    def runSim(self):   

        pop = self.population[:]
        pop.sort(key=lambda agent: (agent.agentHits-agent.timesHit))
        best_agent = pop[9]
        
        worst_agent = pop[8]
        run_simulation_withGraphics(best_agent, worst_agent, 20)


    def save_agents(self, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self.population, f)
                print("Agent saved successfully.")
        except Exception as e:
            print(f"Error occurred while saving agent: {e}")

    def load_agents(self, filename):
        with open(filename, 'rb') as f:
            self.population = pickle.load(f)


ga = GeneticAlgorithm(population_size)


numberofgenerations = 20
for _ in range(numberofgenerations):
      #Run the genetic algorithm for 100 generations
    ga.run_generation(_,numberofgenerations)
    



ga.load_agents('agents2.pkl')
ga.runSim()

