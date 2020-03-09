import random

from ursina import *
from typing import Any, Tuple, Dict, List

from collections import OrderedDict

WIDTH = 50
HEIGHT = 50
TICKER = 0

POPULATION_SIZE = 25
FOOD_SIZE = round(1.5 * POPULATION_SIZE)

app = Ursina()
grid = Entity(model=Grid(50, 50), scale=50, color=color.color(0, 0, 0.8, lerp(0.8, 0, 0.2)),
              rotation_x=90, position=(-25, 0.01, -25))


class Genome:

    @staticmethod
    def generate_random_genome(speed_range: Tuple=(0.05, 0.75),
                               size_range: Tuple=(0.5, 3), sense_range: Tuple=(1, 10)) -> "Genome":
        speed = random.uniform(*speed_range)
        size = random.uniform(*size_range)
        sense = random.uniform(*sense_range)

        return Genome(speed=speed, size=size, sense=sense)

    def __init__(self, speed: float=None, size: float=None, sense: float=None):
        self._speed = speed
        self._size = size
        self._sense = sense

    def set_speed(self, speed: [float, int]) -> None:
        if isinstance(speed, float) or isinstance(speed, int):
            self._speed = speed
            return None
        raise TypeError('speed must be of type float or int')

    @property
    def speed(self) -> [float, int]:
        return self._speed

    def set_size(self, size: [float, int]) -> None:
        if isinstance(size, float) or isinstance(size, int):
            self._size = size
            return None
        raise TypeError('size must be of type float or int')

    @property
    def size(self) -> [float, int]:
        return self._size

    def set_sense(self, sense: [float, int]) -> None:
        if isinstance(sense, float) or isinstance(sense, int):
            self._sense = sense
            return None
        raise TypeError('sense must be of type float or int')

    @property
    def sense(self) -> [float, int]:
        return self._sense


class Individual(Entity):

    @staticmethod
    def _calculate_hunger_cost(speed: float, size: float, sense: float) -> float:
        return (pow(speed, 2) * pow(size, 3)) + (sense/10)

    def check_collision(self, ent2: Entity):
        self_box = [self.x - self.scale_x / 2,
                    self.x + self.scale_x / 2,

                    self.z + self.scale_z / 2,
                    self.z - self.scale_z / 2]

        ent2_box = [ent2.x - ent2.scale_x / 2,
                    ent2.x + ent2.scale_x / 2,

                    ent2.z + ent2.scale_z / 2,
                    ent2.z - ent2.scale_z / 2]
        if self_box[3] <= ent2_box[3] <= self_box[2] or self_box[3] <= ent2_box[2] <= self_box[2] or self_box[3] <= ent2.z <= self_box[2]:
            if self_box[0] <= ent2_box[0] <= self_box[1] or self_box[0] <= ent2_box[1] <= self_box[1] or self_box[0] <= ent2.x <= self_box[1] or self_box[0] <= ent2.x <= self_box[1]:
                return True
        return False

    def __init__(self, add_to_scene_entities: bool=True, genome: Genome=None, **kwargs: Any):
        super().__init__(add_to_scene_entities=add_to_scene_entities, **kwargs)
        self.model = Cube()
        self.color = color.orange
        self.age = 0

        # self.hunger = 10000
        self.hunger = 250
        self.genome = genome
        if self.genome is None:
            self.genome = Genome.generate_random_genome()

        self.scale = self.genome.size
        self.speed = self.genome.speed
        self.sense = self.genome.sense

        # self.sense = 50
        self.sense_box = Entity(moel=Cube(), scale=self.sense, color=color.clear)

        self.energy_cost = self._calculate_hunger_cost(self.speed, self.genome.size, self.sense)

        self.target = None
        self.random_target_x, self.random_target_z = random.randrange(-25, 25), random.randrange(-25, 25)

    def wander(self, clock):
        if self.target is None:
            if clock % 100 == 0:
                self.random_target_x, self.random_target_z = random.randrange(-25, 25), random.randrange(-25, 25)

            if self.random_target_x - 5 < self.x < self.random_target_x + 5 and self.random_target_z - 5 < self.z < self.random_target_z + 5:
                self.random_target_x, self.random_target_z = random.randrange(-25, 25), random.randrange(-25, 25)
        else:
            if clock % 100 == 0:
                self.random_target_x, self.random_target_z = self.target[0], self.target[1]
            if self.random_target_x - 0.5 < self.x < self.random_target_x + 0.5 and self.random_target_z - 0.5 < self.z < self.random_target_z + 0.5:
                self.random_target_x, self.random_target_z = random.randrange(-25, 25), random.randrange(-25, 25)

        dx, dy = self.random_target_x - self.x, self.random_target_z - self.z

        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist

        self.x += dx * self.speed
        self.z += dy * self.speed

    def sense_test(self, clock):  # Needs Fixing
        """
        if self.target is None:
            sensed = []
            for food in foods:
                if self.sense_entity(food):
                    sensed.append((food, self._calc_distance(self, food)))

            if len(sensed) > 1:
                sensed.sort()
                self.target = sensed[0][0].x, sensed[0][0].z
                self.random_target_x, self.random_target_z = self.target
            else:
                if clock % 100 == 0:
                    self.random_target_x, self.random_target_z = random.randrange(-25, 25), random.randrange(-25, 25)

                    if self.random_target_x - 5 < self.x < self.random_target_x + 5 and self.random_target_z - 5 < self.z < self.random_target_z + 5:
                        self.random_target_x, self.random_target_z = random.randrange(-25, 25), random.randrange(-25,
                                                                                                                 25)
        """

    def run_hunger_cycle(self):
        self.hunger -= self._calculate_hunger_cost(self.speed, self.genome.size, self.sense)
        if self.hunger < 0:
            self.color = color.clear
            population.remove(self)
            dead.append(self)

    def feed(self, food: ["Food", "Individual"]):

        if isinstance(food, Food):
            food.color = color.clear
            self.hunger += food.hunger_restoration_value

            foods.remove(food)

        if isinstance(food, Individual):
            food.color = color.clear
            self.hunger += food.hunger

            population.remove(food)
            dead.append(food)

    def sense_entity(self, ent2: Entity):
        self.sense_box.x = self.x
        self.sense_box.z = self.z
        return self.check_collision(ent2)

    @staticmethod
    def _calc_distance(ent1: Entity, ent2: Entity):
        return math.sqrt((ent2.x - ent1.x) ** 2 + (ent2.z - ent1.z) ** 2)

    def sense_all(self, population_list: List[Entity], food_list: List[Entity]):  # Needs Fixing
        closest = []
        for individual, food in zip(population_list, food_list):
            if len(closest) < 1:
                if self.sense_entity(individual):
                    closest.append((individual, self._calc_distance(self, individual)))
                elif self.sense_entity(food):
                    closest.append((food, self._calc_distance(self, food)))
            else:
                if self.sense_entity(individual) and self._calc_distance(self, individual) <= closest[-1][1]:
                    closest[0] = (individual, self._calc_distance(self, individual))
                if self.sense_entity(food) and self._calc_distance(self, food) <= closest[-1][1]:
                    closest[0] = (food, self._calc_distance(self, food))
        print(closest)
        if len(closest) >= 1:
            if isinstance(closest[-1][0], Food):
                self.target = closest[-1][0].x, closest[-1][0].z
            elif isinstance(closest[-1][0], Individual):
                if self.scale_x > closest[-1][0].scale_x + (0.2 * closest[-1][0].scale_x):
                    self.target = closest[-1][0].x, closest[-1][0].z
                elif self.scale_x < closest[-1][0].scale_x + (0.2 * closest[-1][0].scale_x):
                    self.target = closest[-1][0].z, closest[-1][0].x
            else:
                self.target = None

    def reset_hunger(self):
        self.hunger = 500


class Food(Entity):

    def __init__(self, add_to_scene_entities: bool=True, hunger_restoration_value: [float, int]=500, **kwargs):
        super().__init__(add_to_scene_entities=add_to_scene_entities, **kwargs)
        self.model = Sphere()
        self.position = Vec3(random.randrange(-25, 25), 0, random.randrange(-25, 25))
        self.color = color.green
        self.hunger_restoration_value = hunger_restoration_value


def generate_new_population():
    global population

    population = []
    for _ in range(POPULATION_SIZE):
        population.append(Individual())


def generate_new_food():
    global foods

    for food in foods:
        food.color = color.clear
        foods.remove(food)

    for _ in range(FOOD_SIZE):
        foods.append(Food())


def purge_dead():
    global dead

    for corpse in dead:
        corpse.color = color.clear
        dead.remove(corpse)


def update():
    global TICKER

    TICKER += 1
    if len(population) < 1:
        generate_new_population()

    for individual in population:
        # individual.sense_all(population, foods)
        individual.wander(clock=TICKER)
        # individual.sense_test(clock=TICKER)
        individual.run_hunger_cycle()
        if TICKER % 25 == 0:
            individual.color = color.orange

        for other_individual in population:
            if individual is not other_individual and individual.check_collision(other_individual):
                individual.color = color.green
                if TICKER > 100 and individual.scale_x > other_individual.scale_x + (0.2 * other_individual.scale_x):
                    individual.feed(other_individual)

            for food in foods:
                if individual.check_collision(food):
                    individual.feed(food=food)
    if TICKER > 500:
        purge_dead()
        generate_new_food()

        pop_len = len(population)
        for index in range(pop_len):
            survivor = population[index]
            if survivor.hunger >= survivor.hunger - (survivor.hunger * 0.25):
                offspring = Individual(genome=survivor.genome)
                offspring.age = 0

                population.append(offspring)
            survivor.reset_hunger()
        TICKER = 0


if __name__ == '__main__':
    dead = []
    population = []
    for i in range(POPULATION_SIZE):
        population.append(Individual())

    foods = []
    for i in range(FOOD_SIZE):
        foods.append(Food())

    EditorCamera()
    app.run()
