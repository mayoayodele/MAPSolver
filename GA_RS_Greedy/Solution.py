import copy
import numpy as np
import random as r
from Parameters import *

class Solution:
    def __init__(self):
        self.job_permutation= []
        self.fe_allocation = []
        self.lifecyles = {}
        self.capacities = {}
        self.fitness = None
        self.schedule = {}
        self.schedules_per_fe = {}


    def set_ind(self, job_permutation, fe_allocation):
        self.job_permutation = job_permutation.copy()
        self.fe_allocation = fe_allocation.copy()


    def set_lifecyles(self, lifecyles):
        self.lifecyles = copy.deepcopy(lifecyles)
    
    def set_capacities(self, capacities):
        self.capacities = copy.deepcopy(capacities)
    

    def set_fe_schedule(self, schedules_per_fe):
        self.schedules_per_fe = copy.deepcopy(schedules_per_fe)

    def set_fitness(self, respective_job_day):
        
        tardiness = []
        for i in range(len(self.fe_allocation)):
            job_id = self.job_permutation[i]
            earliest_start = respective_job_day[job_id]
            schedule = self.schedules_per_fe[self.fe_allocation[i]]
            capacity = self.capacities[self.fe_allocation[i]]
            fe_finish_times = [f for s, f in schedule if f > earliest_start]
            fe_finish_times = sorted(list(set(fe_finish_times)))
            job_duration = self.lifecyles[job_id] 

            job_start = earliest_start

            can_do_work = False
            f_counter = 0
            while(can_do_work == False):
                temp_start = job_start
                for j in range(job_duration):
                    if(Solution.is_avaible(temp_start, schedule, capacity) == False):
                        job_start = fe_finish_times[f_counter]
                        f_counter = f_counter+ 1
                        can_do_work = False
                        break
                    temp_start = temp_start +1
                    can_do_work = True

            job_finish = job_start + job_duration
            lateness = job_start - earliest_start
            tardiness.append(lateness)

            self.schedule[job_id] = {'job_id': 'm' + str(job_id),
                                    'earliest_start_time': earliest_start,
                                    'scheduled_start_time': job_start,
                                    'duration': job_duration,
                                    'scheduled_finish_time': job_finish,
                                    'assigned_fe': self.fe_allocation[i] }
            self.schedules_per_fe[self.fe_allocation[i]].append([job_start,job_finish ])
        self.fitness = np.max(tardiness)


    def set_fitness_with_improvement(self, respective_job_day, init, improvement_rate):
        #print('Evaluation Started')
        tardiness = []
        for i in range(len(self.fe_allocation)):
            job_id = self.job_permutation[i]
            earliest_start = respective_job_day[job_id]
            schedule = self.schedules_per_fe[self.fe_allocation[i]]
            capacity = self.capacities[self.fe_allocation[i]]
            fe_finish_times = [f for s, f in schedule if f > earliest_start]
            fe_finish_times = sorted(list(set(fe_finish_times)))
            job_duration = self.lifecyles[job_id] 

            job_start = earliest_start

            can_do_work = False
            f_counter = 0
            while(can_do_work == False):
                temp_start = job_start
                for j in range(job_duration):
                    if(Solution.is_avaible(temp_start, schedule, capacity) == False):
                        job_start = fe_finish_times[f_counter]
                        f_counter = f_counter+ 1
                        can_do_work = False
                        break
                    temp_start = temp_start +1
                    can_do_work = True

            job_finish = job_start + job_duration
            temp_lateness = job_start - earliest_start

            min_lateness = temp_lateness
            
            selected_fe_finish = job_finish
            selected_fe_job_duration = job_duration
            selected_fe = self.fe_allocation[i]
            selected_fe_start = job_start
            min_finish = job_finish

            
            if ((r.random() <= Parameters.mutation_rate) and (min_lateness > 0)):
                possible_fes = list(init.client_fe_lifecyle[init.job_client[earliest_start][job_id]].keys())
                possible_fes.remove(self.fe_allocation[i])
                r.shuffle(possible_fes)
                for fe in possible_fes:
                    if(fe in self.schedules_per_fe.keys()):
                        schedule = self.schedules_per_fe[fe]
                    else:
                        schedule = init.schedules_per_fe[fe]
                    capacity = init.fe_capacity[fe]
                    fe_finish_times = [f for s, f in schedule if f > earliest_start]
                    fe_finish_times = sorted(list(set(fe_finish_times)))

                    client = init.job_client[earliest_start][job_id]
                    job_duration = init.client_fe_lifecyle[client][fe]
                    job_start = earliest_start
                    can_do_work = False
                    f_counter = 0
                    while(can_do_work == False):
                        temp_start = job_start
                        for j in range(job_duration):
                            if(Solution.is_avaible(temp_start, schedule, capacity) == False):
                                job_start = fe_finish_times[f_counter]
                                f_counter = f_counter+ 1
                                can_do_work = False
                                break
                            temp_start = temp_start +1
                            can_do_work = True

                    job_finish = job_start + job_duration
                    temp_lateness = job_start - earliest_start
                    temp_finish = job_finish
                    if((min_lateness > temp_lateness) and (min_finish >= temp_finish)):
                        min_lateness = temp_lateness
                        selected_fe_finish = job_finish
                        selected_fe_job_duration = job_duration
                        selected_fe = fe
                        selected_fe_start = job_start
                        min_finish = job_finish
                        break

            lateness = selected_fe_start - earliest_start
            tardiness.append(lateness)
                           
            self.schedule[job_id] = {'job_id': 'm' + str(job_id),
                                    'earliest_start_time': earliest_start,
                                    'scheduled_start_time': selected_fe_start,
                                    'duration': selected_fe_job_duration,
                                    'scheduled_finish_time': selected_fe_finish,
                                    'assigned_fe': selected_fe}
            if(selected_fe in self.schedules_per_fe.keys() ):
                self.schedules_per_fe[selected_fe].append([selected_fe_start,selected_fe_finish ])
            else:
                self.schedules_per_fe[selected_fe] = init.schedules_per_fe[fe]
                self.schedules_per_fe[selected_fe].append([selected_fe_start,selected_fe_finish ])

        #print('Evaluation Complete')
        self.fitness = np.max(tardiness)


    @staticmethod
    def is_avaible(start, schedule, capacity):
        count = 0
        for s, f in schedule:
            if (s <= start < f):
                count = count + 1
        if count < capacity:
            return True
        else:
            return False


    