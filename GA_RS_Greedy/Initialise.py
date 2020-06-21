import pandas as pd
from Solution import * 
import random
import numpy as np
import json
import copy
from Parameters import *


class Initialise:
    def __init__(self, problem_path):
        self.no_of_batches= Parameters.schedule_approach
        with open(problem_path + '/' + Parameters.problem_names['Jobs']) as json_file:
            job_client = json.load(json_file)
        
        self.job_client = {int(outer_k):{int(k):int(v) for k,v in job_client[outer_k].items()} for outer_k in job_client.keys() if (len(job_client[outer_k]) > 0)}
        print(self.job_client)
        self.job_arrival_day = {int(job):int(batch) for batch in job_client.keys() 
                            for job, client in job_client[batch].items() if (len(job_client[batch]) > 0)}
        print('job arrival')
        print(self.job_arrival_day.values())
        self.job_schedule_batch = {}
        all_start_days = list(job_client.keys())
        no_of_schedules = len(all_start_days)//self.no_of_batches
        temp_batch = [self.no_of_batches]*no_of_schedules
        #set the remainder as the last batch
        leftover = len(all_start_days)%self.no_of_batches
        if(leftover > 0):
            temp_batch.append(leftover)
        
        k=0
        for i in range(len(temp_batch)):
            days_collection = []
            for j in range(temp_batch[i]):
                start_day = all_start_days[k]
                days_collection.append(int(start_day))
                k = k+ 1
            if( i in self.job_arrival_day.values()):
                self.job_schedule_batch[i] = days_collection
        #print(self.job_schedule_batch)
        
        

        self.client_fe_lifecyle = {}
        with open(problem_path + '/' + Parameters.problem_names['Lifecycles']) as json_file:
            client_fe_lifecyle = json.load(json_file)
        for client in client_fe_lifecyle.keys():
            fe_lifecyles = {int(k):int(v) for k,v in client_fe_lifecyle[client].items()}
            self.client_fe_lifecyle[int(client)] = fe_lifecyles


        with open(problem_path + '/' +  Parameters.problem_names['Capacities']) as json_file:
            fe_capacity = json.load(json_file)
        self.fe_capacity = {int(k):int(v) for k,v in fe_capacity.items()}


        with open(problem_path + '/' + Parameters.problem_names['Uncompleted_Jobs']) as json_file:
            availabilities = json.load(json_file)

        self.availabilities = {}
        for fe in availabilities.keys():
            availability = {k:int(v) for k,v in availabilities[fe].items()}
            self.availabilities[int(fe)] = availability


        self.schedules_per_fe = {}
        for key in self.availabilities.keys():
           self.schedules_per_fe[key] =[[0, value] for value in self.availabilities[key].values()]

             


    def set_availabilities(self, availabilities):
        for i in availabilities.keys():
            self.availabilities[i] = availabilities[i].copy()
        #self.availabilities = copy.deepcopy(availabilities)
    
    def set_schedules_per_fe(self, schedules_per_fe):
        for i in schedules_per_fe.keys():
            self.schedules_per_fe[i] = schedules_per_fe[i].copy()

    def get_respective_job_day(self, job_batch):
        respective_job_day = {}
        job_days = self.job_schedule_batch[job_batch]
        for job_day in job_days:
            for job in self.job_client[job_day].keys():
                respective_job_day[job] = job_day
        return respective_job_day

    def get_solution_indexes(self, job_batch):
        solution_indexes = []
        job_days = self.job_schedule_batch[job_batch]
        for job_day in job_days:
            for job in self.job_client[job_day].keys():
                solution_indexes.append(job)
        return solution_indexes
        
    
    def get_random_solution(self, job_batch):
        solution = Solution()
        job_permutation = self.get_solution_indexes(job_batch).copy()
        random.shuffle(job_permutation)
        fe_allocation = []
        for job in job_permutation:
            job_day = self.job_arrival_day[job]
            possible_fes = list(self.client_fe_lifecyle[self.job_client[job_day][job]].keys())
            fe = random.choice(possible_fes)
            fe_allocation.append(fe)



        solution.set_ind(job_permutation, fe_allocation)
        
        solution.set_lifecyles(self.estimate_lifecycles(job_permutation, fe_allocation, job_batch))
        solution.set_capacities(self.get_capacities(fe_allocation))
        solution.set_fe_schedule(self.get_schedules_per_fe(fe_allocation))
        solution.set_fitness(self.get_respective_job_day(job_batch))
        return solution

    def get_random_solution_rs(self, job_batch):
        solution = Solution()
        job_permutation = self.get_solution_indexes(job_batch).copy()
        fe_allocation = []
        for job in job_permutation:
            job_day = self.job_arrival_day[job]
            possible_fes = list(self.client_fe_lifecyle[self.job_client[job_day][job]].keys())
            fe = random.choice(possible_fes)
            fe_allocation.append(fe)



        solution.set_ind(job_permutation, fe_allocation)
        
        solution.set_lifecyles(self.estimate_lifecycles(job_permutation, fe_allocation, job_batch))
        solution.set_capacities(self.get_capacities(fe_allocation))
        solution.set_fe_schedule(self.get_schedules_per_fe(fe_allocation))
        solution.set_fitness(self.get_respective_job_day(job_batch))
        return solution


    def estimate_lifecycles(self, job_permutation, fe_allocation, job_batch):
        respective_job_day = self.get_respective_job_day(job_batch)
        ind_lifecycles = {}
        for i in range(len(job_permutation)):
            job_id = job_permutation[i]
            client = self.job_client[respective_job_day[job_id]][job_id]
            try:
                temp_lifecycle = self.client_fe_lifecyle[client][fe_allocation[i]]
            except:
                temp_lifecycle = self.client_fe_lifecyle[client][fe_allocation[i]]
            ind_lifecycles[job_id] = temp_lifecycle
        return ind_lifecycles

    
  
        

    def get_capacities(self, ind):
        capacity = {}
        for i in ind:
            capacity_level = self.fe_capacity[i]
            capacity[i] = capacity_level
        return capacity


    def get_availabilities(self, ind):
        availability = {}
        for i in ind:
            availability[i] = self.availabilities[i]
        return availability

    def get_schedules_per_fe(self, ind):
        schedules_per_fe = {}
        for i in ind:
            schedules_per_fe[i] = self.schedules_per_fe[i]
        return schedules_per_fe

    
