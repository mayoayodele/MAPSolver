import numpy as np
import pandas as pd
from Initialise import *
from GAOperators.Selection import *
from Parameters import *
from Utils import *
import copy
from os import walk
import os
import sys


Parameters.pop_size = 50
Parameters.number_of_generations = 560
Parameters.tournament_size = 2
Parameters.crossover_type = 1
Parameters.crossover_prob = 1.0
Parameters.elitism = 50

Parameters.mutation_rate = 'default'


Parameters.mutation_type = 1

Parameters.numnber_of_run = 20
Parameters.results_path = './ResultsLaptop'
Parameters.schedule_approach = 1
 
 

folders = ['SmallFE_Per_Client'] #, 'Actual']

for folder in folders:
    Parameters.problem_folder_path = './Data/' + folder

    problems = ['Problem2', 'Problem4']

    for prob in problems:
        Parameters.problem = prob
        problem_path = Parameters.problem_folder_path + "/" + Parameters.problem
        print(problem_path)



        name_of_saved_file = Parameters.problem_folder_path.split('/')[-1] + prob +  'ps'+ str(Parameters.pop_size ) + 'g'+\
                                    str(Parameters.number_of_generations) + 'ts' + str(Parameters.tournament_size ) + 'ct'+ str(Parameters.crossover_type) + 'cr'+\
                                    str(Parameters.crossover_prob) + 'e' + str(Parameters.elitism) +  'm' + str(Parameters.mutation_rate)  + 'n'+\
                                    str(Parameters.numnber_of_run) + 'per' + str(Parameters.schedule_approach) + 'dayschedule'

        Parameters.result_name = name_of_saved_file
        overall_results = None
        overall_best_schedule= None
        overall_best_schedule_temp= None
        overall_best_fitness = None

        for run in range(Parameters.numnber_of_run):
            results_dict = {}
            init = Initialise(problem_path)
            dict_batch_fitness = {}
            batches = sorted(list(init.job_schedule_batch))
            number_of_generations_dict = Utils.get_number_of_gens_per_batch(Parameters.number_of_generations, len(batches))
            gen_count = 0
            
            for job_batch in batches:
                
                population = []
                for i in range(Parameters.pop_size):
                    solution =init.get_random_solution(job_batch)
                    problem_size = len(solution.fe_allocation)
                    if('default' in str(Parameters.mutation_rate)):
                        Parameters.mutation_rate = 1/problem_size
                    population.append(solution)
                    
                population.sort(key=lambda x: x.fitness, reverse=False)
                best_solution = population[0]
                gen_count = gen_count + 1

                best_fitness = best_solution.fitness
                if(job_batch > 0):
                    max_batch_fitness = max(list(dict_batch_fitness.values()))
                    if(best_fitness < max_batch_fitness):
                        best_fitness =  max_batch_fitness

                results_dict[gen_count] = [[best_solution.job_permutation.copy(), best_solution.fe_allocation.copy()], best_fitness, Utils.get_average_fitness(population)]

                selection = Selection(init, job_batch)

                number_of_generations = number_of_generations_dict[job_batch]
                
                for j in range(number_of_generations-1):
                    #perform selection, crossover and mutation
                    gen_count = gen_count+1
                    offspring_population = []
                    offspring_population.extend(selection.tournament_selection(population))

                        

                    #perform elitism of offspring and parent population
                    temp_population = []
                    temp_population.extend(selection.select_best_individuals(offspring_population, population[:Parameters.elitism]))

                    population = []
                    population.extend(temp_population)
                    best_solution = population[0]
                    # print(best_solution.fitness)
                    # print(Utils.get_average_fitness(population))

                    best_fitness = best_solution.fitness
                    if(job_batch > 0):
                        max_batch_fitness = max(list(dict_batch_fitness.values()))
                        if(best_fitness < max_batch_fitness):
                            best_fitness =  max_batch_fitness

                    results_dict[gen_count] = [[best_solution.job_permutation.copy(), best_solution.fe_allocation.copy()], best_fitness, Utils.get_average_fitness(population)]
                dict_batch_fitness[job_batch] = best_solution.fitness
                print(best_solution.schedule)
                print(dict_batch_fitness)
                init.set_schedules_per_fe(best_solution.schedules_per_fe)

                if(job_batch == 0):
                    overall_best_schedule_temp = copy.deepcopy(best_solution.schedule)
                else:
                    overall_best_schedule_temp.update(copy.deepcopy(best_solution.schedule))
                
                #init.set_availabilities(best_solution.availabilities)
            

            results = pd.DataFrame.from_dict(results_dict, orient='index',  columns=['Best Solution','Best Fitness', 'Average Fitness'])
            print('run ' + str(run))
            #print(init.availabilities)
            #results.to_excel('./Results/best_results.xlsx')
            if(run==0):
                overall_results = results[['Best Fitness', 'Average Fitness']]
                overall_results.columns = ['Best Fitness Run 1', 'Avg Fitness Run 1']
                overall_best_schedule = copy.deepcopy(overall_best_schedule_temp)
                overall_best_fitness  = best_fitness
            else:
                overall_results['Best Fitness Run ' + str(run+1)] = results['Best Fitness']
                overall_results['Avg Fitness Run ' + str(run+1)] = results['Average Fitness']
                if(best_fitness < overall_best_fitness):
                    overall_best_schedule = copy.deepcopy(overall_best_schedule_temp)
                    overall_best_fitness  = best_fitness

        best_schedule = pd.DataFrame.from_dict(overall_best_schedule, orient='index')
        best_schedule = best_schedule.reset_index()


        columns = []
        for counter in range(Parameters.numnber_of_run):
            columns.append('Best Fitness Run ' + str(counter+1))
        print(columns)

        overall_results['Overall Average of Best Fitness']  = overall_results[columns].mean(axis=1)
        overall_results['Overall Standard Deviation of Best Fitness']  = overall_results[columns].std(axis=1)




        file_name = Parameters.result_name
        file_path = Parameters.results_path + '/' + Parameters.problem 
        try:
            os.mkdir(file_path)
        except:
            print(file_path + ' already exists')

        print(file_name)


        overall_results.to_excel(file_path + '/'  +  file_name + 'best_results.xlsx')
        best_schedule.to_excel(file_path + '/'  +  file_name +  'best_schedule.xlsx')
