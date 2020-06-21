import random as r
import copy 
from Parameters import *

class Mutation:
    def __init__(self, job_client, client_fe_lifecyle, job_schedule_batch, job_batch, respective_job_day):
        self.job_client = job_client
        self.client_fe_lifecyle = client_fe_lifecyle
        self.job_schedule_batch = job_schedule_batch
        self.job_batch = job_batch
        self.respective_job_day = respective_job_day
        self.mutation_rate = Parameters.mutation_rate 

      

    def controlled_mutation_job_permutation_insert(self, ind):
        job_permutation = ind['job_permutation'].copy()
        fe_allocation = ind['fe_allocation'].copy()
        for rand1 in range(len(job_permutation)):
            if(r.random() <  self.mutation_rate):
                gene_length = len(job_permutation)

                rand2 = 0
                while rand1 == rand2:
                    rand2 = r.randint(0, gene_length-1)
                

                temp_job = job_permutation[rand1]
                temp_fe = fe_allocation[rand1]
                del job_permutation[rand1]
                del fe_allocation[rand1] 
                #below does not work well with duplicates in fe_allocation
                # job_permutation.remove(temp_job)
                # fe_allocation.remove(temp_fe)
                job_permutation.insert(rand2, temp_job) 
                fe_allocation.insert(rand2,temp_fe)

        new_solution = {'job_permutation': job_permutation.copy(),
                        'fe_allocation':fe_allocation.copy()}

            
        return copy.deepcopy(new_solution)

    def controlled_mutation_job_permutation_swap(self, ind):
        job_permutation = ind['job_permutation'].copy()
        fe_allocation = ind['fe_allocation'].copy()
        for rand1 in range(len(job_permutation)):
            if(r.random() <  self.mutation_rate):
                gene_length = len(job_permutation)
                rand2 = 0
                if(gene_length > 1):
                    while rand1 == rand2:
                        rand2 = r.randint(0, gene_length-1)

                    temp_job = job_permutation[rand1]
                    temp_fe = fe_allocation[rand1]
                    job_permutation[rand1] = job_permutation[rand2]
                    job_permutation[rand2] = temp_job
                    fe_allocation[rand1] = fe_allocation[rand2]
                    fe_allocation[rand2] = temp_fe

        new_solution = {'job_permutation': job_permutation.copy(),
                        'fe_allocation':fe_allocation.copy()}
        return copy.deepcopy(new_solution)




    def controlled_mutation_fe_allocation(self, ind):
        job_permutation = ind['job_permutation'].copy()
        fe_allocation = ind['fe_allocation'].copy()
        for mutation_point in range(len(job_permutation)):
            if(r.random() <  self.mutation_rate):
                job_id = job_permutation[mutation_point]
                client = self.job_client[self.respective_job_day[job_id]][job_id]
                possible_fes_temp = list(self.client_fe_lifecyle[client].keys())
                current_fe = fe_allocation[mutation_point]
                possible_fes_temp.remove(current_fe)
                if(len(possible_fes_temp) > 0):
                    fe_allocation[mutation_point] = r.choice(possible_fes_temp)
            
        new_solution = {'job_permutation': ind['job_permutation'].copy(),
                        'fe_allocation':fe_allocation.copy()}
        return copy.deepcopy(new_solution)
    


