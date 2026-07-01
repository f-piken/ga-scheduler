import random


class Crossover:

    @staticmethod
    def single_point(parent1, parent2):

        chromosome_length = len(parent1)

        cut_point = random.randint(
            1,
            chromosome_length - 1
        )

        offspring1 = (
            parent1[:cut_point] +
            parent2[cut_point:]
        )

        offspring2 = (
            parent2[:cut_point] +
            parent1[cut_point:]
        )

        logs = {
            "cut_point": cut_point,
            "parent1": parent1,
            "parent2": parent2,
            "offspring1": offspring1,
            "offspring2": offspring2
        }

        return offspring1, offspring2, logs