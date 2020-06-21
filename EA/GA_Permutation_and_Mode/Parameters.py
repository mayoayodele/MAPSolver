class Parameters:

    pop_size = None

    number_of_generations = None

    tournament_size = None

    #crossover type 1 and 2  are respectively one-point and  partially matched crossover types
    crossover_type = None
    
    crossover_prob = None

    mutation_rate = None

    mutation_type = None


    elitism = None

    
    improvement_rate = 0.3


    numnber_of_run = None

    problem_names = { 'Jobs': 'Day_Job_Client.txt',
    'Lifecycles': 'Client_FE_Lifecyle.txt',
    'Capacities': 'FE_Capacity.txt',
    'Uncompleted_Jobs': 'FE_Schedule.txt'}

    

    schedule_approach = None #'Daily: 1', 'Weekly: 7' ,'4Weeks': 28'
    
    problem_folder_path = None
    
    problem = None
    
    results_path = None

    result_name = None