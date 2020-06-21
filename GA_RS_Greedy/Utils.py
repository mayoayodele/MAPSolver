import numpy as np

class Utils:

    @staticmethod
    def get_average_fitness(population):
        fitnesses = []
        for solution in population:
            fitnesses.append(solution.fitness)
        return np.mean(fitnesses)

    @staticmethod
    def are_equal(ind1, ind2):
        for i in range(len(ind1)):
            if(ind1[i] != ind2[i]):
                return False
        return True

    @staticmethod
    def get_number_of_gens_per_batch(number_of_gens, no_of_job_batches):
        each_gen = number_of_gens//no_of_job_batches
        remainder = number_of_gens - (each_gen * no_of_job_batches)
        gens = {}
        for i in range(no_of_job_batches):
            gens[i] = each_gen
        gens[no_of_job_batches-1] = gens[no_of_job_batches-1] + remainder
        return gens
    
    @staticmethod
    def get_number_of_gens_per_batch_new(number_of_gens, batches):
        no_of_job_batches = len(batches)

        each_gen = number_of_gens//no_of_job_batches
        remainder = number_of_gens - (each_gen * no_of_job_batches)
        gens = {}
        for i in batches:
            gens[i] = each_gen
        gens[batches[-1]] = gens[batches[-1]] + remainder
        return gens


        Utils.get_number_of_gens_per_batch(Parameters.number_of_generations, len(batches))

    # @staticmethod
    # def get_makespan(availabilities):
    #     makespan = 0
    #     for fe in availabilities.keys():
    #         max_finish = max(list(availabilities[fe].values()))
    #         if(makespan < max_finish):
    #             makespan = max_finish
    #     return makespan

    @staticmethod
    def get_makespan(availabilities, best_solution_availabilities, job_client, job_batch):
        temp_availabilities = {}
        all_jobs = []
        for i in range(job_batch):
            all_jobs.extend(list(job_client[i].keys()))
     
        all_jobs = ['m' + str(i) for i in all_jobs]

        best_sol_dict = {k:v for key, value in best_solution_availabilities.items()
                        for k, v in value.items()}

        #get finish times for jobs in  job_client
        all_dict = {k:v for key, value in availabilities.items()
                        for k, v in value.items()
                        if k in all_jobs }
        
        best_sol_dict.update(all_dict)   
            
        return max(list(best_sol_dict.values()))

    
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


    

