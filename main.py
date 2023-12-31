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
import NN
import torch


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
        self.population_right = [agent.Agent(600, 300, 800, 600) for _ in range(population_size)]
        self.population_left = [agent.Agent(200, 300, 800, 600) for _ in range(population_size)]
        self.history = {'generation': [], 'population': [], 'best': [], 'worst': [], 'average': []}
        
        plt.ion()
        self.fig, self.ax = plt.subplots()
    
    def selection(self, population):
        # Tournament selection
        parent1 = max(random.sample(population, k=5), key=lambda agent: (agent.agentHits-agent.timesHit))
        parent2 = max(random.sample(population, k=5), key=lambda agent: (agent.agentHits-agent.timesHit))
        return parent1, parent2

    def replacement(self,population):
        # Replace the worst individuals in the population with the newly created individuals
        population.sort(key=lambda agent: (agent.agentHits-agent.timesHit))
        population[:2] = self.new_individuals

    def run_generation(self,generation,numberofgenerations):
        # Run the game for each pair of agents
        count = 0

       
        for agent_right in self.population_right:
            for agent_left in self.population_left:
                run_simulation(agent_left, agent_right, 40, count)
                count += 1

        whichPop = 0        
        for pop in [self.population_right, self.population_left]:
            # Selection
            parent1, parent2 = self.selection(pop)
            
            # Crossover
            self.new_individuals = [parent1.crossover(parent2) for _ in range(2)]
            
            # Mutation
            for individual in self.new_individuals:
                individual.mutate()
            

            self.print_stats(generation,pop,whichPop)
            # Replacement

            self.replacement(pop)

            
            # Reset the scores for the next generation
            for agent in pop:
                agent.agentHits=0
                agent.timesHit=0

            whichPop = 1
        
        
        # Replacement
        if numberofgenerations -1  == generation :
            self.runSim()
            self.save_agents()   

            return

        self.update_graph()
        

    def print_stats(self, generation, population, whichPop):

        name =""

        if whichPop == 0:
            name = "right"
        else:
            name = "left"

        best_agent = max(population, key=lambda agent: (agent.agentHits-agent.timesHit))
        worst_agent = min(population, key=lambda agent: (agent.agentHits-agent.timesHit))
        scores = [agent.agentHits - agent.timesHit for agent in population]
        

        print(f'Generation: {generation}')
        print(f'Population: {name}')
        print(f'Best Score: {best_agent.agentHits - best_agent.timesHit}')
        print(f'Worst Score: {worst_agent.agentHits - worst_agent.timesHit}')
        print(f'Average Score: {sum(scores) / len(population)}')

        print()

        
        self.history['generation'].append(generation)
        self.history['population'].append(name)
        self.history['best'].append(best_agent.agentHits - best_agent.timesHit)
        self.history['worst'].append(worst_agent.agentHits - worst_agent.timesHit)
        self.history['average'].append(sum(scores) / len(population))

        
        
        
    def runSim(self):   

        
        self.population_right.sort(key=lambda agent: (agent.agentHits-agent.timesHit))
        right = self.population_right[6]
        self.population_left.sort(key=lambda agent: (agent.agentHits-agent.timesHit))
        left = self.population_left[6]
        run_simulation_withGraphics(left, right, 20)


    def save_agents(self):
        try:
            with open('rightpop.pkl', 'wb') as f:
                pickle.dump(self.population_right, f)
                print("Right Agents saved successfully.")
            with open('leftpop.pkl', 'wb') as f:
                pickle.dump(self.population_left, f)
                print("Left Agents saved successfully.")
        except Exception as e:
            print(f"Error occurred while saving agent: {e}")

    def load_agents(self):
        with open('rightpop.pkl', 'rb') as f:
            self.population_right = pickle.load(f)
        with open('leftpop.pkl', 'rb') as f:
            self.population_left = pickle.load(f)
    
    def update_graph(self):
        
        self.ax.clear()  # clear the current plot
        populations = set(self.history['population'])  # get all unique population names
        line_styles = ['-', '--']  # solid and dashed lines

        for style, pop in zip(line_styles, populations):
            # get the data for this population
            indices = [i for i, x in enumerate(self.history['population']) if x == pop]
            generations = [self.history['generation'][i] for i in indices]
            best_scores = [self.history['best'][i] for i in indices]
            worst_scores = [self.history['worst'][i] for i in indices]
            average_scores = [self.history['average'][i] for i in indices]

            # plot the data for this population
            self.ax.plot(generations, best_scores, style, label=f'{pop} best')
            self.ax.plot(generations, worst_scores, style, label=f'{pop} worst')
            self.ax.plot(generations, average_scores, style, label=f'{pop} average')

        self.ax.set_ylim(-200, 200)  # set the y-axis limits
        self.ax.legend()  # add a legend
        plt.draw()  # draw the plot
        plt.show(block=False)
        plt.pause(1)  # pause to allow the plot to update




'''
ga = GeneticAlgorithm(population_size)


numberofgenerations = 30
for _ in range(numberofgenerations):
      #Run the genetic algorithm for 100 generations
    ga.run_generation(_,numberofgenerations)
    



ga.load_agents()
ga.runSim()
'''


