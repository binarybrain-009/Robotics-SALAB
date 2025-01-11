def aggregate_success(features, robot_type):
    """
    Compute the aggregate success rate for a robot handling a subtask with multiple features.
    """
    success_matrix = {
        'careful': {'light': 0.9, 'middle': 0.7, 'heavy': 0.5},
        'dexterous': {'light': 0.8, 'middle': 0.6, 'heavy': 0.4},
        'heavy': {'light': 0.5, 'middle': 0.7, 'heavy': 0.9}
    }
    # Compute the average success rate across all features
    # For tasks with multiple features: careful and heavy, we use the average success rate
    return sum(success_matrix[feature][robot_type] for feature in features) / len(features)


def allocate_subtasks(subtasks, robots):
    """
    Allocate subtasks to robots using dynamic programming.
    subtasks: List of subtasks with their features (e.g., [{'sub1': ['careful', 'dexterous']}, ...]).
    robots: List of robot types (e.g., ['light', 'middle', 'heavy']).
    We will need to plug in the features
    """
    num_subtasks = len(subtasks)
    num_robots = len(robots)
    
    # Initialize DP table
    dp = [[0] * num_robots for _ in range(num_subtasks)]
    
    # Base case: Assign the first subtask to each robot
    for j in range(num_robots):
        dp[0][j] = aggregate_success(subtasks[0], robots[j])
    
    # Fill DP table
    for i in range(1, num_subtasks):
        for j in range(num_robots):
            # Assign subtask i to robot j and maximize the cumulative success rate
            dp[i][j] = max(dp[i-1][k] + aggregate_success(subtasks[i], robots[j]) for k in range(num_robots))
    
    # Extract the optimal solution
    return max(dp[num_subtasks-1])

# Example Usage
#TODO: put the subtasks' features here, e.g. pick up -heavy, place - careful, heavy
subtasks = [
    ['careful', 'dexterous'],  # sub1
    ['heavy'],                 # sub2
    ['careful', 'heavy'],      # sub3
    ['dexterous'],             # sub4
    ['careful'],               # sub5
    ['heavy'],                 # sub6
    ['careful', 'dexterous'],  # sub7
    ['dexterous', 'heavy'],    # sub8
    ['careful'],               # sub9
    ['dexterous', 'heavy']     # sub10
]
#for now we are assuming we have three robots
robots = ['light', 'middle', 'heavy']

result = allocate_subtasks(subtasks, robots)
print("Maximum Success Rate:", result)
