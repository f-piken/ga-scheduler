# ============================================
# app/core/selection.py
# ============================================

import json
import random

from app.core.fitness import FitnessCalculator


class Selection:

    @staticmethod
    def roulette_wheel(population):

        # ====================================
        # FITNESS CALCULATION
        # ====================================

        fitness_values = []

        for chromosome in population:

            fitness = (
                FitnessCalculator.calculate(
                    chromosome
                )
            )

            fitness_values.append(fitness)

        # ====================================
        # TOTAL FITNESS
        # ====================================

        total_fitness = sum(
            fitness_values
        )

        # ====================================
        # PROBABILITIES
        # ====================================

        probabilities = []

        for fitness in fitness_values:

            if total_fitness == 0:

                probability = 0

            else:

                probability = (
                    fitness / total_fitness
                )

            probabilities.append(
                probability
            )

        # ====================================
        # SELECT PARENTS
        # ====================================

        selected = random.choices(
            population,
            weights=probabilities,
            k=2
        )

        parent1 = selected[0]
        parent2 = selected[1]

        # ====================================
        # POPULATION LOGS
        # ====================================

        population_logs = []

        for index, chromosome in enumerate(population):

            is_selected = False
            selected_as = None

            if chromosome == parent1:

                is_selected = True
                selected_as = "Parent 1"

            elif chromosome == parent2:

                is_selected = True
                selected_as = "Parent 2"

            population_logs.append({

                "chromosome_index": index + 1,

                "chromosome": chromosome,

                "fitness": fitness_values[index],

                "probability": round(
                    probabilities[index],
                    4
                ),

                "is_selected": is_selected,

                "selected_as": selected_as

            })

        # ====================================
        # LOGS
        # ====================================

        logs = {

            "population": json.dumps(
                population_logs
            ),

            "fitness_values": json.dumps(
                fitness_values
            ),

            "probabilities": json.dumps(
                probabilities
            ),

            "selected_parents": {

                "parent1": parent1,

                "parent2": parent2

            }

        }

        # ====================================
        # RETURN
        # ====================================

        return parent1, parent2, logs