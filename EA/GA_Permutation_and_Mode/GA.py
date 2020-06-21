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




Parameters.problem_folder_path = sys.argv[2] 
Parameters.problem = sys.argv[3] 
problem_path = Parameters.problem_folder_path + "/" + Parameters.problem
Parameters.pop_size = int(sys.argv[4])
Parameters.number_of_generations = int(sys.argv[5])
Parameters.tournament_size = int(sys.argv[6])
Parameters.crossover_type = int(sys.argv[7])
Parameters.crossover_prob = float(sys.argv[8])
Parameters.elitism = int(sys.argv[9])

temp_mutation_rate = sys.argv[10]
if(isinstance(temp_mutation_rate,float)):
    Parameters.mutation_rate = temp_mutation_rate
#else mutation rate is set later in the code as 1/problem size

Parameters.mutation_type = 1

Parameters.numnber_of_run = int(sys.argv[11])
Parameters.results_path = sys.argv[12]
Parameters.schedule_approach = int(sys.argv[13])
 
Parameters.result_name = sys.argv[14]  

print(problem_path)


overall_results = None
overall_best_schedule= None
overall_best_schedule_temp= None
overall_best_fitness = None

for run in range(Parameters.numnber_of_run):
    results_dict = {}
    init = Initialise(problem_path)
    dict_batch_fitness = {}
    batches = sorted(list(init.job_schedule_batch))
    #number_of_generations_dict = Utils.get_number_of_gens_per_batch(Parameters.number_of_generations, len(batches))
    number_of_generations_dict = Utils.get_number_of_gens_per_batch_new(Parameters.number_of_generations, batches)
    gen_count = 0
    print(batches)
    print('run ',run)
    
    for job_batch in batches:
        print('batch ', job_batch)
        population = []
        for i in range(Parameters.pop_size):
            solution =init.get_random_solution(job_batch)
            problem_size = len(solution.fe_allocation)
            if('default' in temp_mutation_rate):
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
            print('gen: ', j)
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
