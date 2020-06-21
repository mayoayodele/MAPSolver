import random as r
import copy


class Crossover:
    @staticmethod
    def pmx_crossover(parents):
        parent_list1 = parents[0]['job_permutation'].copy()
        parent_list2 = parents[1]['job_permutation'].copy()
        parent_mode1 = parents[0]['fe_allocation'].copy()
        parent_mode2 = parents[1]['fe_allocation'].copy()
        
        gene_length = len(parent_mode1)
        child = []
        crossedList = []
        crossedMode = []

        rand1 = 0
        rand2 = 0
        while rand1 == rand2:
            rand1 = r.randint(1, gene_length-1)
            rand2 = r.randint(1, gene_length-2)


        crossoverpoint1 = min(rand1, rand2)
        crossoverpoint2 = max(rand1, rand2)


        count = 0
        for i in range(len(parent_list1)):
            job = parent_list1[i]
            if(count == crossoverpoint1):
                break
            if(job not in parent_list2[crossoverpoint1:crossoverpoint2]):
                crossedList.append(job)
                crossedMode.append(parent_mode1[i])
                count= count+1


        crossedList.extend(parent_list2[crossoverpoint1:crossoverpoint2])
        crossedMode.extend(parent_mode2[crossoverpoint1:crossoverpoint2])

        for j in range(len(parent_list1)):
            job = parent_list1[j]
            if(job not in crossedList):
                crossedList.append(job)
                crossedMode.append(parent_mode1[j])


        new_solution = {'job_permutation': crossedList.copy(),
                        'fe_allocation':crossedMode.copy()}
        return copy.deepcopy(new_solution)




    @staticmethod
    def one_point_crossover(parents):
        parent_list1 = parents[0]['job_permutation'].copy()
        parent_list2 = parents[1]['job_permutation'].copy()
        parent_mode1 = parents[0]['fe_allocation'].copy()
        parent_mode2 = parents[1]['fe_allocation'].copy()

        gene_length = len(parent_mode1)

        crossedList = []
        crossedMode = []
        if(gene_length > 2):
            crossover_point = r.randint(1, gene_length-2)
        else:
            crossover_point = 1

        for i in range(crossover_point):
            crossedList.append(parent_list1[i])
            crossedMode.append(parent_mode1[i])

        for j in range(len(parent_mode2)):
            if parent_list2[j] not in crossedList:
                crossedList.append(parent_list2[j])
                crossedMode.append(parent_mode2[j])

        new_solution = {'job_permutation': crossedList,
                        'fe_allocation': crossedMode}

        
        return copy.deepcopy(new_solution)
  


   
  

