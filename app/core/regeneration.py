from app.core.fitness import FitnessCalculator


class Regeneration:

    @staticmethod
    def replace_worst(
        population,
        offspring
    ):

        fitness_values = []

        for chromosome in population:

            fitness_values.append(
                FitnessCalculator.calculate(
                    chromosome
                )
            )

        worst_index = fitness_values.index(
            min(fitness_values)
        )

        old_chromosome = population[worst_index]

        population[worst_index] = offspring

        logs = {
            "worst_index": worst_index,
            "old_chromosome": old_chromosome,
            "new_chromosome": offspring
        }

        return population, logs