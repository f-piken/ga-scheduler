import json

from app.core.population import PopulationGenerator
from app.core.selection import Selection
from app.core.crossover import Crossover
from app.core.mutation import Mutation
from app.core.regeneration import Regeneration
from app.core.fitness import FitnessCalculator
from app.core.repair import Repair


class GeneticAlgorithm:

    def __init__(
        self,
        jamaahs,
        team_leaders,
        muthowifs,
        departures,
        generations=50,
        population_size=20
    ):

        self.jamaahs = jamaahs
        self.team_leaders = team_leaders
        self.muthowifs = muthowifs
        self.departures = departures

        self.generations = generations
        self.population_size = population_size

        self.logs = []

    def run(self):

        population, population_logs = (
            PopulationGenerator.generate_population(
                self.population_size,
                self.jamaahs,
                self.team_leaders,
                self.muthowifs,
                self.departures
            )
        )

        self.logs.append({
            "phase": "population",
            "data": {
                "population": population_logs
            }
        })

        # Cari kromosom terbaik awal
        best_chromosome = max(
            population,
            key=lambda chromosome:
            FitnessCalculator.calculate(chromosome)
        )

        best_fitness = FitnessCalculator.calculate(
            best_chromosome
        )

        for generation in range(self.generations):

            (
                parent1,
                parent2,
                selection_logs

            ) = Selection.roulette_wheel(
                population
            )

            self.logs.append({

                "generation": generation + 1,

                "phase": "selection",

                "data": {

                    "population":
                    json.loads(
                        selection_logs["population"]
                    ),

                    "fitness_values":
                    json.loads(
                        selection_logs["fitness_values"]
                    ),

                    "probabilities":
                    json.loads(
                        selection_logs["probabilities"]
                    ),

                    "parent1": parent1,
                    "parent2": parent2
                }
            })

            (
                offspring1,
                offspring2,
                crossover_logs

            ) = Crossover.single_point(
                parent1,
                parent2
            )

            self.logs.append({

                "generation": generation + 1,

                "phase": "crossover",

                "data": crossover_logs

            })

            (
                offspring1,
                mutation_logs1
            ) = Mutation.random_gene_mutation(
                offspring1,
                self.team_leaders,
                self.muthowifs,
                self.departures
            )
            
            (
                offspring2,
                mutation_logs2
            ) = Mutation.random_gene_mutation(
                offspring2,
                self.team_leaders,
                self.muthowifs,
                self.departures
            )
            
            offspring1 = Repair.repair_schedule(
                offspring1,
                self.departures,
                self.team_leaders,
                self.muthowifs
            )
            
            offspring2 = Repair.repair_schedule(
                offspring2,
                self.departures,
                self.team_leaders,
                self.muthowifs
            )

            self.logs.append({

                "generation": generation + 1,

                "phase": "mutation",

                "data": [

                    mutation_logs1,
                    mutation_logs2

                ]
            })

            (
                population,
                regeneration_logs1

            ) = Regeneration.replace_worst(
                population,
                offspring1
            )

            (
                population,
                regeneration_logs2

            ) = Regeneration.replace_worst(
                population,
                offspring2
            )

            # ======================
            # ELITISM
            # ======================

            current_best = max(
                population,
                key=lambda chromosome:
                FitnessCalculator.calculate(
                    chromosome
                )
            )

            current_fitness = (
                FitnessCalculator.calculate(
                    current_best
                )
            )

            if current_fitness > best_fitness:

                best_fitness = current_fitness
                best_chromosome = current_best

            worst = min(
                population,
                key=lambda chromosome:
                FitnessCalculator.calculate(
                    chromosome
                )
            )

            population.remove(worst)

            population.append(
                best_chromosome
            )

            self.logs.append({

                "generation": generation + 1,

                "phase": "regeneration",

                "data": [

                    regeneration_logs1,
                    regeneration_logs2

                ]
            })

        return {

            "best_fitness":
            best_fitness,

            "best_chromosome":
            best_chromosome,

            "logs":
            self.logs

        }