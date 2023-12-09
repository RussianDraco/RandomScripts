import pygame
import random
import math
import time
import numpy as np

# Initialize pygame
pygame.init()

# Create the screen
WIDTH = 1400
HEIGHT = 900

MUTATION_RATE = 0.6

ASEXUAL_FOOD_THRESHOLD = 200

SYNTHESIS_DELAY = 250 #ms

RESPAWN_FROM_BEST = True
RESPAWN_POP = 50
MAX_POP = 100

FPS = 999 #999 for max


screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and Icon
pygame.display.set_caption("Life Simulator")

"""
Body parts:
0 - Body
1 - Eater
2 - Mover
3 - Photosynthesizer
4 - Fat Storage
"""

body_partNum = 5

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize weights with random values
        self.weights_ih = np.random.rand(self.hidden_nodes, self.input_nodes)
        self.weights_ho = np.random.rand(self.output_nodes, self.hidden_nodes)

    def add_input_nodes(self, num_nodes):
        self.input_nodes += num_nodes

    def add_hidden_nodes(self, num_nodes):
        self.hidden_nodes += num_nodes

    def remove_hidden_nodes(self):
        self.hidden_nodes -= 1
        self.hidden_nodes = max(self.hidden_nodes, 1)

        # Resize weights matrices
        self.weights_ih.resize((int(self.hidden_nodes), self.input_nodes))
        self.weights_ho.resize((self.output_nodes, self.hidden_nodes))

    def add_output_nodes(self, num_nodes):
        self.output_nodes += num_nodes

        # Resize weights matrices
        self.weights_ih.resize((self.hidden_nodes, self.input_nodes))
        self.weights_ho.resize((self.output_nodes, self.hidden_nodes))

    def weight_shuffle(self):
        self.weights_ih = np.random.rand(self.hidden_nodes, self.input_nodes)
        self.weights_ho = np.random.rand(self.output_nodes, self.hidden_nodes)

    def tanh(self, x):
        return np.tanh(x)

    def feedforward(self, inputs):
        # Convert inputs list to 2d array and transpose it
        inputs = np.array(inputs, ndmin=2).T

        # Calculate signals into hidden layer
        hidden_inputs = np.dot(self.weights_ih, inputs)
        # Calculate the signals emerging from hidden layer
        hidden_outputs = self.tanh(hidden_inputs)

        # Calculate signals into final output layer
        final_inputs = np.dot(self.weights_ho, hidden_outputs)
        # Calculate the signals emerging from final output layer
        final_outputs = self.tanh(final_inputs)

        return final_outputs
    
def choose_adjacent_coord(coords):
    if len(coords) == 0:
        return (0, 0)

    adjacent_coords = []
    for coord in coords:
        x, y = coord
        adjacent_coords.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

    available_coords = [coord for coord in adjacent_coords if coord not in coords and coord[0] >= 0 and coord[1] >= 0]
    if available_coords:
        return random.choice(available_coords)
    else:
        return None

class DNA:
    def __init__(self):
        self.parts = {} # (x, y) -> body_part_type
        self.brain = NeuralNetwork(1, 2, 2) #modify later to add other potential inputs (eyes, ears, etc.) and outputs (movement, etc.)
        self.synthesis_delay = SYNTHESIS_DELAY

    @staticmethod
    def breed_dna(parent1, parent2):
        child_dna = DNA()

        # Inherit body parts from parents
        for coord, body_part_type in parent1.parts.items():
            child_dna.parts[coord] = body_part_type

        for coord, body_part_type in parent2.parts.items():
            if coord not in child_dna.parts:
                child_dna.parts[coord] = body_part_type

        # Inherit brain from parents
        child_dna.brain.input_nodes = max(parent1.brain.input_nodes, parent2.brain.input_nodes)
        child_dna.brain.hidden_nodes = max(parent1.brain.hidden_nodes, parent2.brain.hidden_nodes)
        child_dna.brain.output_nodes = max(parent1.brain.output_nodes, parent2.brain.output_nodes)

        child_dna.brain.weights_ih = np.maximum(parent1.brain.weights_ih, parent2.brain.weights_ih)
        child_dna.brain.weights_ho = np.maximum(parent1.brain.weights_ho, parent2.brain.weights_ho)

        return child_dna

    @staticmethod
    def random_dna():
        dna = DNA()
        for _ in range(random.randint(3, 15)):
            dna.parts[choose_adjacent_coord(dna.parts.keys())] = random.randint(0, body_partNum-1)
        dna.brain = NeuralNetwork(random.randint(1, 3), random.randint(1, 5), random.randint(1, 3))
        return dna

    def mutate(self):
        if random.random() < MUTATION_RATE:
            if random.random() < 0.5: # Modify body
                if random.random() < 0.5:
                    self.parts[list(self.parts.keys())[random.randint(0, len(self.parts.keys()) - 2)]] = random.randint(0, body_partNum-1)
                else:
                    if random.random() < 0.5:
                        self.parts[choose_adjacent_coord(list(self.parts.keys()))] = random.randint(0, body_partNum-1)
                    else:
                        self.parts.pop(list(self.parts.keys())[random.randint(0, len(list(self.parts.keys())) - 2)])
            else:
                r = random.random()
                if r < 0.25:
                    self.brain.add_hidden_nodes(1)
                elif r < 0.5:
                    self.brain.remove_hidden_nodes()
                elif r < 0.75:
                    self.synthesis_delay += random.randint(-500, 500)
                    self.synthesis_delay = max(self.synthesis_delay, 0)
                else:
                    self.brain.weight_shuffle()

class Organism:
    def __init__(self, dna=None):
        self.dna = dna if dna else DNA.random_dna()
        self.x = 0
        self.y = 0
        self.food = 100
        self.max_food = 100 + 50 * [x for x in self.dna.parts.items()].count(4)
        self.extra_food = 0

        self.width = 20 * (max([x for (x, y) in self.dna.parts.keys()]) + 1)
        self.height = 20 * (max([y for (x, y) in self.dna.parts.keys()]) + 1)

        self.speed = [x for x in self.dna.parts.values()].count(2) * 3

        self.isProducer = 3 in self.dna.parts.values()

        if self.isProducer: self.last_synthesis = pygame.time.get_ticks()

    def move(self):
        movement_outputs = self.dna.brain.feedforward([10*random.random()-5 for x in range(self.dna.brain.input_nodes)])

        self.x += round(int(movement_outputs[0] * self.speed))
        try:
            self.y += round(int(movement_outputs[1] * self.speed))
        except IndexError:
            self.y += round(int(movement_outputs[0] * self.speed))

        self.x = max(0, min(self.x, WIDTH - self.width))
        self.y = max(0, min(self.y, HEIGHT - self.height))

    def update(self):
        body_cells = list(self.dna.parts.values()).count(0)
        incr = 0.1 * body_cells + (len(self.dna.parts.values()) - body_cells) * 0.27
        self.food -= incr
        self.extra_food -= incr

        if len(self.dna.parts.values()) in [0, 1, 2] or not (1 in self.dna.parts.values() or 3 in self.dna.parts.values()):
            self.die()

        if self.food <= 0:
            self.die()
        if self.speed != 0 and not self.isProducer:
            self.move()

        for (x, y), body_part_type in self.dna.parts.items():
            if body_part_type == 0:  # Body
                color = (255, 255, 255)  # White
            elif body_part_type == 1:  # Eater
                color = (255, 0, 0)  # Red
                if self.isProducer:
                    break

                i = 0
                for f in world.foods:
                    fx, fy = f
                    if math.sqrt(((self.x + x * 20) - fx)**2 + ((self.y + y * 20) - fy)**2) <= 35:
                        self.food += 30
                        self.extra_food += 30
                        self.food = min(self.food, self.max_food)
                        world.foods.pop(i)
                        world.nutrients.append((random.randint(self.x - 40, self.x + 40), random.randint(self.y - 40, self.y + 40)))

                        if self.extra_food >= ASEXUAL_FOOD_THRESHOLD:
                            self.asexual_reproduction()
                            self.extra_food = self.food // 2

                        break
                    i+=1
            elif body_part_type == 2:  # Mover
                color = (0, 0, 255)  # Blue
            elif body_part_type == 3:  # Photosynthesizer
                color = (0, 255, 0) # Green

                if self.last_synthesis + self.dna.synthesis_delay > pygame.time.get_ticks():
                    break

                i = 0
                for n in world.nutrients:
                    nx, ny = n
                    if math.sqrt(((self.x + x * 20) - nx)**2 + ((self.y + y * 20) - ny)**2) <= 75:
                        incr = list(self.dna.parts.values()).count(3) * 10
                        self.food += incr
                        self.extra_food += incr
                        self.food = min(self.food, self.max_food)
                        world.nutrients.pop(i)
                        world.foods.append((random.randint(self.x - 40, self.x + 40), random.randint(self.y - 40, self.y + 40)))

                        if self.extra_food >= ASEXUAL_FOOD_THRESHOLD:
                            self.asexual_reproduction()
                            self.extra_food = self.food // 2

                        break
                    i+=1

            elif body_part_type == 4:  # Fat Storage
                color = (255, 255, 0) # Yellow
            else:
                color = (10, 10, 10)  # Grey (error)

            pygame.draw.rect(screen, color, (self.x + x * 20, self.y + y * 20, 20, 20))

    def asexual_reproduction(self):
        if len(world.organisms) > MAX_POP:
            return
        child_dna = DNA.breed_dna(self.dna, self.dna)
        child_dna.mutate()
        child = Organism(child_dna)
        child.x = random.randint(0, WIDTH - child.width)
        child.y = random.randint(0, HEIGHT - child.height)
        world.organisms.append(child)

    def die(self):
        world.organisms.remove(self)
        world.generate_nutrients(self)
        world.record_death_time(self.dna)
        del self


class World:
    def __init__(self):
        self.organisms = []
        self.foods = [] # (x, y)
        self.nutrients = [] # (x, y)
        self.last_2deaths = [None]
    
    def generate_nutrients(self, o):
        if len(self.nutrients) > 200:
            return

        for _ in range(len(o.dna.parts.values()) * 2):
            nx = random.randint(o.x - 70, o.x + 70)
            ny = random.randint(o.y - 70, o.y + 70)
            self.nutrients.append((nx, ny))

    def record_death_time(self, org_dna):
        self.last_2deaths = [org_dna, self.last_2deaths[0]]

    def update(self):
        [organism.update() for organism in self.organisms]

        if len(world.organisms) == 0:
            if RESPAWN_FROM_BEST and self.last_2deaths[0] != None:
                O1 = Organism(self.last_2deaths[0])
                O2 = Organism(self.last_2deaths[1])
                for _ in range(RESPAWN_POP // 2):
                    O1.asexual_reproduction()
                    O2.asexual_reproduction()
                del O1; del O2
            else:
                for _ in range(RESPAWN_POP):
                    o = Organism()
                    o.x = random.randint(0, WIDTH - o.width)
                    o.y = random.randint(0, HEIGHT - o.height)
                    self.organisms.append(o)

        for f in self.foods:
            fx, fy = f
            pygame.draw.circle(screen, (0, 153, 0), (fx, fy), 5)

        for n in self.nutrients:
            nx, ny = n
            pygame.draw.circle(screen, (102, 204, 255), (nx, ny), 5)


world = World()

for _ in range(50):
    world.nutrients.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))

for _ in range(350):
    world.foods.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    if FPS != 999: time.sleep(1/FPS)
    world.update()

    pygame.display.update()