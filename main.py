"""

Solution to Reply Challenge By Babichev Rinat
12.03.2020

"""

"""
developer 
• A string indicating the Reply company C i the Developer works for.
• An integer indicating the bonus potential B i this Developer contributes.
• An integer indicating the number of skills (the cardinality of the skill
set) |S i | of that Developer.
• |S i | text strings describing each skill of the Developer.

"""

"""
A string indicating the Reply company C i the Project Manager works
for.
• An integer indicating the bonus potential B i this Project Manager con-
tributes.
"""

common_skills = {

}

common_skills_idx = -1

company_names = {

}

company_idx = -1
game = None


def set_game(gg):
    global game
    game = gg


def bSearch(ind, index_list):
    Low = 0
    High = len(index_list) - 1
    while Low <= High:
        Mid = (High + Low) // 2
        if index_list[Mid] == ind:
            return Mid
        elif index_list[Mid] > ind:
            High = Mid - 1
        else:
            Low = Mid + 1
    return None


class Developer:
    __slots__ = ['company', 'skills', 'bonus', 'number']

    def __init__(self, company, skills, bonus, numbr=0):
        global common_skills_idx
        global company_idx
        if company not in company_names:
            company_idx += 1
            company_names[company] = company_idx
        self.company = company_names[company]
        skills_ = []
        self.number = numbr
        bin_skill = 0
        for skill in skills:
            if skill not in common_skills:
                common_skills_idx += 1
                common_skills[skill] = common_skills_idx
            skills_.append(common_skills[skill])
            # bin_skill += 2 ^ skills[-1]

        self.skills = sorted(skills_)
        self.bonus = bonus

    def profit(self, dev):
        cm_skills = 0
        for skill in self.skills:
            if bSearch(skill, dev.skills) is not None:
                cm_skills += 1
        return cm_skills * (len(self.skills) + len(dev.skills) - 2 * cm_skills)

    def __repr__(self):
        return f'{self.company} {self.bonus} {str(self.skills)}'

    def __str__(self):
        return self.__repr__()


class Manager:
    __slots__ = ['company', 'bonus', 'number']

    def __init__(self, company, bonus, numbr=0):
        global common_skills_idx
        global company_idx
        if company not in company_names:
            company_idx += 1
            company_names[company] = company_idx
        self.company = company_names[company]
        self.bonus = bonus
        self.number = numbr

    def __repr__(self):
        return f'{self.company} {self.bonus}'

    def __str__(self):
        return self.__repr__()


class Office:

    def __init__(self, managers, devs, office, man_pos, dev_pos, dev_neighbors, man_neighbors):
        self.managers = managers
        self.developers = devs
        self.office = office
        self.man_pos = man_pos
        self.dev_pos = dev_pos
        self.dev_neighbors, self.man_neighbors = dev_neighbors, man_neighbors

    @property
    def devs(self):
        return self.developers


def get_data(file):
    f = open(file, 'r')
    text = f.readlines()
    text = [t.strip() for t in text]
    n, m = list(map(int, text[0].split(' ')))
    office = ''
    for i in range(m):
        office += text[i + 1]
    cur = m + 1
    devs = int(text[cur])

    developers = []

    for i in range(devs):
        cur += 1
        descr = text[cur].split(' ')
        company = descr[0]
        bonus = int(descr[1])
        skill = int(descr[2])
        skills = []
        for i in range(3, len(descr)):
            skills.append(descr[i])
        developers.append(Developer(company, skills, bonus, len(developers) - 1))

    cur += 1
    managers = int(text[cur])
    mans = []
    for i in range(managers):
        cur += 1
        descr = text[cur].split(' ')
        company = descr[0]
        bonus = int(descr[1])
        mans.append(Manager(company, bonus, len(mans) - 1))
    return developers, office, mans, m, n


def get_score(game: Office, dev_nums, man_nums):
    score = 0

    for dev_num, values in game.dev_neighbors.items():
        cur: Developer = game.devs[dev_nums[dev_num]]
        for dn in values[0]:
            opp = game.devs[dev_nums[dn]]

            if cur.number == opp.number:
                score -= 100000

            if cur.company == opp.company:
                score += cur.bonus * opp.bonus

            ss = cur.profit(opp)
            score += ss

        for mn in values[1]:

            mopp = game.managers[man_nums[mn]]

            if mopp.company == cur.company:
                score += mopp.bonus * cur.bonus

    for man_num, values in game.man_neighbors.items():
        cur = game.managers[man_nums[man_num]]

        for mn in values:
            mopp = game.managers[man_nums[mn]]

            if mopp.number == cur.number:
                score -= 1000000

            if mopp.company == cur.company:
                score += mopp.bonus * cur.bonus

    return score


# Hromosom
class Individual:
    # genome - positions of developers and managers
    def __init__(self, genome=[[], []]):
        self.genome = genome

    # Score of this individual (number of unordered pairs in array )
    @property
    def fitness(self):
        return get_score(game, self.genome[0], self.genome[1])

    @property
    def devs(self):
        return self.genome[0]

    @property
    def mans(self):
        return self.genome[1]

    def __repr__(self):
        return str(self.genome)

    def __str__(self):
        return str(self.genome)


import random


# Population
class Population:
    def __init__(self):
        self.individuals = []

    # New individum in population
    def add(self, individ):
        self.individuals.append(individ)

    # Individual with highest score
    @property
    def best_individual(self):
        MAX = -999999999
        best = None
        for ind in self.individuals:
            a1 = ind.fitness
            if a1 > MAX:
                MAX = a1
                best = ind
        return best

    # Cross(скрещиваем) two individuals
    @staticmethod
    def crossover(father: Individual, mother: Individual):
        child_devs = []
        child_mans = []

        for dev1, dev2 in zip(father.devs, mother.devs):
            if random.uniform(0, 1) > 0.5:
                child_devs.append(dev1)
            else:
                child_devs.append(dev2)

            if random.uniform(0, 1) < 0.05:
                child_devs[-1] = random.randint(0, len(game.developers) - 1)

        for man1, man2 in zip(father.mans, mother.mans):
            if random.uniform(0, 1) > 0.5:
                child_mans.append(man1)
            else:
                child_mans.append(man2)

            if random.uniform(0, 1) < 0.05:
                child_mans[-1] = random.randint(0, len(game.managers) - 1)
        return Individual([child_devs, child_mans])

    @staticmethod
    def mutate(population, rate: float = 0.05):

        for ind in population.individuals:
            if random.uniform(0, 1) < rate:

                choices_ = random.sample(range(len(ind.devs)), round(0.2 * len(ind.devs)))
                for i in choices_:
                    ind.devs[i] = random.randint(0, len(game.devs) - 1)

                choices_ = random.sample(range(len(ind.mans)), round(0.2 * len(ind.mans)))
                for i in choices_:
                    ind.mans[i] = random.randint(0, len(game.managers) - 1)
        return population
        # One evolution iteration


def evolve(population, mutation_rate=0.1):
    new_population = Population()
    best = population.best_individual
    new_population.add(best)
    for i in range(len(population.individuals) - 1):
        a1 = random.choice(population.individuals)
        a2 = random.choice(population.individuals)
        baby = Population.crossover(a1, a2)

        if baby.fitness > a1.fitness and baby.fitness > a2.fitness:
            new_population.add(baby)
        else:
            new_population.add(a1)

        # Let some mutation
    return new_population


def run(population_size, mutation_rate, number_of_devs, number_of_mans):
    population = Population()
    for i in range(population_size):
        devs_, mans_ = random.sample(range(len(game.developers)), number_of_devs), \
                       random.sample(range(len(game.managers)), number_of_mans)
        population.add(Individual([devs_, mans_]))
    generation = 1
    i = 0
    while i < 10:
        i += 1
        best = population.best_individual
        print(best.fitness)
        population = evolve(population, mutation_rate)
        population.individuals[0] = best
        generation += 1

    return best


if __name__ == "__main__":

    developers, office, managers, m, n = get_data('in.txt')
    dev_pos = []
    man_pos = []

    dev_neighbors = {}
    man_neighbors = {}

    number_of_devs = 0
    number_of_mans = 0

    for i in range(len(office)):
        if office[i] == '_':
            number_of_devs += 1

            dev_pos.append(i)
            ind_ = len(dev_pos) - 1
            dev_neighbors[ind_] = [[], []]
            if i > 0 and i % n != 0:
                if office[i - 1] == '_':
                    dev_neighbors[ind_][0].append(bSearch(i - 1, dev_pos))
            if i > n and i % n != 0:
                if office[i - n] == '_':
                    dev_neighbors[ind_][0].append(bSearch(i - n, dev_pos))

        if office[i] == 'M':
            number_of_mans += 1

            man_pos.append(i)
            ind_ = len(man_pos) - 1
            man_neighbors[ind_] = []

            if i > 0 and i % n != 0:
                if office[i - 1] == 'M':
                    man_neighbors[ind_].append(bSearch(i - 1, man_pos))
            if i > n and i % n != 0:
                if office[i - n] == 'M':
                    man_neighbors[ind_].append(bSearch(i - n, man_pos))

    for i in range(len(office)):
        if office[i] == '_':
            for ost, ind in ((0, i - 1), (m - 1, i + 1), (100, i - n), (100, i + n)):
                if i % n != ost and ind >= 0 and ind < m * n and office[ind] == 'M':
                    dev_neighbors[dev_pos.index(i)][1].append(bSearch(ind, man_pos))
    g1 = Office(managers, developers, office, man_pos, dev_pos, dev_neighbors, man_neighbors)
    set_game(g1)
    best = run(10, 0.1, number_of_devs, number_of_mans)

    f = open('out.txt','w')
    res = ['X' for x in game.devs]
    for l in range(len(best.devs)):
        res[best.devs[l]] = f'{dev_pos[l] // m} {dev_pos[l] % n}'

    res2 = ['X' for x in game.managers]
    for l in range(len(best.mans)):
        res2[best.mans[l]] = f'{man_pos[l] // m} {man_pos[l] % n}'

    for line in res:
        f.write(line+'\n')

    for line in res2:
        f.write(line + '\n')

