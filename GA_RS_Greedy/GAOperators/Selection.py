import random as r
from GAOperators.Crossover import *
from GAOperators.Mutation import *
from Parameters import *
from Solution import *
import copy


class Selection:
    def __init__(self, init, job_batch):
        self.init = init
        self.job_batch = job_batch
        self.job_client = init.job_client
        self.job_schedule_batch = init.job_schedule_batch
        self.solution_indexes = init.get_solution_indexes(job_batch)
        client_fe_lifecyle = init.client_fe_lifecyle 
        self.respective_job_day = init.get_respective_job_day(job_batch)
        self.Mutation = Mutation(self.job_client, client_fe_lifecyle, self.job_schedule_batch, job_batch, self.respective_job_day)
        problem_size = len(self.solution_indexes)
        self.mutation_rate = Parameters.mutation_rate
        self.respecitive_job_day = init.get_respective_job_day(job_batch)
        



  
    def tournament_selection(self, population):
        parent_population = copy.deepcopy(population)
        offspring_population = []
        for p in range(len(population)):
            parents = []
            for i in range(Parameters.tournament_size):
                temp_population = []
                for j in range(Parameters.tournament_size):
                    temp_population.append(r.choice(parent_population))
                #sort solutions by fitness
                temp_population.sort(key=lambda x: x.fitness, reverse=False)
                parents.append({'job_permutation': temp_population[0].job_permutation.copy(),
                        'fe_allocation':temp_population[0].fe_allocation.copy()})
        
            
            #perform crossover
            if(r.random() < Parameters.crossover_prob): 
                if(Parameters.crossover_type==1):
                    child = Crossover.one_point_crossover(parents)
                elif(Parameters.crossover_type==2):
                    child = Crossover.pmx_crossover(parents)
                else:
                    break
            else:
                if(r.random() < 0.5):
                    child = copy.deepcopy(parents[0])
                else:
                    child = copy.deepcopy(parents[1])

            
            child = self.Mutation.controlled_mutation_job_permutation_swap(child.copy())
                
                #child = self.Mutation.controlled_mutation_job_permutation_insert(child.copy())

            child = self.Mutation.controlled_mutation_fe_allocation(child.copy())


            #estimate solution
            solution = Solution()
            solution.set_ind(child['job_permutation'].copy(), child['fe_allocation'].copy())
            solution.set_lifecyles(self.init.estimate_lifecycles(child['job_permutation'].copy(), child['fe_allocation'].copy(), self.job_batch) )
            solution.set_capacities(self.init.get_capacities(child['fe_allocation'].copy()))
            solution.set_fe_schedule(self.init.get_schedules_per_fe(child['fe_allocation'].copy()))
            solution.set_fitness(self.respecitive_job_day)

            offspring_population.append(solution)
        offspring_population.sort(key=lambda x: x.fitness, reverse=False)
        return offspring_population



    def tournament_selection_greedy(self, population, improvement_rate):
        parent_population = copy.deepcopy(population)
        offspring_population = []
        for p in range(len(population)):
            parents = []
            for i in range(Parameters.tournament_size):
                temp_population = []
                for j in range(Parameters.tournament_size):
                    temp_population.append(r.choice(parent_population))
                #sort solutions by fitness
                temp_population.sort(key=lambda x: x.fitness, reverse=False)
                parents.append({'job_permutation': temp_population[0].job_permutation.copy(),
                        'fe_allocation':temp_population[0].fe_allocation.copy()})
        
            
            #perform crossover
            if(r.random() < Parameters.crossover_prob): 
                if(Parameters.crossover_type==1):
                    child = Crossover.one_point_crossover(parents)
                elif(Parameters.crossover_type==2):
                    child = Crossover.pmx_crossover(parents)
                else:
                    print("Invalid Crossover Type")
                    break
            else:
                if(r.random() < 0.5):
                    child = copy.deepcopy(parents[0])
                else:
                    child = copy.deepcopy(parents[1])


            child = self.Mutation.controlled_mutation_job_permutation_swap(child.copy())
                
                #child = self.Mutation.controlled_mutation_job_permutation_insert(child.copy())

            child = self.Mutation.controlled_mutation_fe_allocation(child.copy())


            #estimate solution
            solution = Solution()
            solution.set_ind(child['job_permutation'].copy(), child['fe_allocation'].copy())
            solution.set_lifecyles(self.init.estimate_lifecycles(child['job_permutation'].copy(), child['fe_allocation'].copy(), self.job_batch) )
            solution.set_capacities(self.init.get_capacities(child['fe_allocation'].copy()))
            solution.set_fe_schedule(self.init.get_schedules_per_fe(child['fe_allocation'].copy()))
            solution.set_fitness_with_improvement(self.respecitive_job_day, self.init, improvement_rate)

          

            offspring_population.append(solution)
        offspring_population.sort(key=lambda x: x.fitness, reverse=False)
        return offspring_population

    @staticmethod
    def select_best_individuals(offspring_population, parent_population):
        temp_population = []
        temp_population.extend(offspring_population)
        temp_population.extend(parent_population)
        temp_population.sort(key=lambda x: x.fitness, reverse=False)
        new_population = []
        new_population.extend(temp_population[:len(offspring_population)])
        return(new_population)










