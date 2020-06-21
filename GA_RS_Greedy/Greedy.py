from Initialise import *
from Utils import *
import os

main_folder = './Data'

    #subfolder = 'Actual'
# for subfolder in ['Actual', 'LargeCapacity_Per_FE', 'LargeClient', 'LargeFE',
#             'LargeFE_Per_Client', 'LargeJobs_Per_Client', 'LargeLifecycle',
#             'LargeUtilisation', 'SmallCapacity_Per_FE', 'SmallClient', 'SmallFE',
#             'SmallFE_Per_Client', 'SmallJobs_Per_Client', 'SmallLifecycle', 'SmallUtilisation']:

subfolder = 'SmallUtilisation'
folder_path = main_folder + '/' +subfolder
results = {}
for sched in [1]:

    Parameters.schedule_approach = sched
    problem_results = {}
    for problem in ['Problem1','Problem2', 'Problem3', 'Problem4', 'Problem5',
                            'Problem6','Problem7','Problem8','Problem9','Problem10',
                            'Problem11','Problem12','Problem13','Problem14','Problem15',
                            'Problem16','Problem17','Problem18','Problem19','Problem20']:
        problem_path = folder_path + "/" + problem
        print(problem_path)

        init = Initialise(problem_path)
        schedules_per_fe = init.schedules_per_fe
        
        batches = sorted(list(init.job_schedule_batch))
        gen_count = 0

        scheduled_jobs = {}
        
        tardiness = []
        for job_batch in batches:
            job_permutation = init.get_solution_indexes(job_batch).copy()
            

            
            for i in range(len(job_permutation)):
                job_id = job_permutation[i]
                earliest_start = init.get_respective_job_day(job_batch)[job_id]

                job_day = init.job_arrival_day[job_id]
                possible_fes = list(init.client_fe_lifecyle[init.job_client[job_day][job_id]].keys())

                print('Job:', job_id)
                first_fe = True
                for fe in possible_fes:
                    schedule = schedules_per_fe[fe]
                    capacity = init.fe_capacity[fe]
                    fe_finish_times = [f for s, f in schedule if f > earliest_start]
                    fe_finish_times = sorted(list(set(fe_finish_times)))

                    client = init.job_client[earliest_start][job_id]
                    job_duration = init.client_fe_lifecyle[client][fe]


                
                    job_start = earliest_start

                    can_do_work = False
                    f_counter = 0
                    while(can_do_work == False):
                        temp_count = 0
                        temp_start = job_start
                        for j in range(job_duration):
                            if(Utils.is_avaible(temp_start, schedule, capacity) == False):
                                job_start = fe_finish_times[f_counter]
                                f_counter = f_counter+ 1
                                can_do_work = False
                                break
                            temp_start = temp_start +1
                            can_do_work = True

                    job_finish = job_start + job_duration
                    temp_lateness = job_start - earliest_start
                    if(first_fe):
                        min_lateness = temp_lateness
                        selected_fe_finish = job_finish
                        selected_fe_job_duration = job_duration
                        selected_fe = fe
                        selected_fe_start = job_start
                        first_fe = False
                    else:
                        if(min_lateness > temp_lateness):
                            min_lateness = temp_lateness
                            selected_fe_finish = job_finish
                            selected_fe_job_duration = job_duration
                            selected_fe = fe
                            selected_fe_start = job_start

                    print('fe:', fe, ', start: ', job_start)
                print('Selected fe:', selected_fe, ', start: ', selected_fe_start)

                lateness = selected_fe_start - earliest_start
                tardiness.append(lateness)
                
                scheduled_jobs[job_id] = {'job_id': 'm' + str(job_id),
                                        'earliest_start_time': earliest_start,
                                        'scheduled_start_time': selected_fe_start,
                                        'duration': selected_fe_job_duration,
                                        'scheduled_finish_time': selected_fe_finish,
                                        'assigned_fe': selected_fe }

                schedules_per_fe[selected_fe].append([selected_fe_start,selected_fe_finish ])
            fitness = np.max(tardiness)

            best_schedule = pd.DataFrame.from_dict(scheduled_jobs, orient='index')
            best_schedule = best_schedule.reset_index()


            file_path = './ResultsGreedyTest' + '/'  + subfolder 
            try:
                os.mkdir(file_path)
            except:
                print(file_path + ' already exists')

            best_schedule.to_excel(file_path+ '/' + problem +  'best_schedule.xlsx')

            
            problem_results[problem] = fitness
            print(problem_results[problem])
    results[sched] = problem_results
    print(results)

all_results = pd.DataFrame.from_dict(results, orient='index')
all_results = all_results.reset_index()

all_results.to_excel(file_path+ '/fitness.xlsx')
