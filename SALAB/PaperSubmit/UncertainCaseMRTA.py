import numpy as np

# Initialize robots
robots = {
    "light": {"workload": "light", "dexterity": "high"},
    "middle": {"workload": "medium", "dexterity": "medium"},
    "heavy": {"workload": "heavy", "dexterity": "low"}
}

# Create a sequence of 10 subtasks
#TODO: this "10 subtasks" are assumed, we need to change this section to adapt to the TEACH dataset
tasks = [
    {"id": i + 1, "feature": feature}
    for i, feature in enumerate(
        np.random.choice(["careful", "dexterous", "heavy"], 10, replace=True)
    )
]

# Success probability ranges for each robot-task feature combination
# I am assuming that we do not have an accurate estimation of it but we have some historical data on the success rate
success_probabilities = {
    "careful": {
        "light": [0.7, 0.9],
        "middle": [0.5, 0.7],
        "heavy": [0.4, 0.5]
    },
    "dexterous": {
        "light": [0.8, 0.9],
        "middle": [0.6, 0.8],
        "heavy": [0.3, 0.5]
    },
    "heavy": {
        "light": [0.2, 0.3],
        "middle": [0.5, 0.7],
        "heavy": [0.7, 0.9]
    }
}

# Monte Carlo simulation for success probabilities
#TODO: tune the parameter of num_samples
def monte_carlo_simulation(robot, task, num_samples=100):
    """Simulate task success based on sampled probabilities."""
    #TODO: I have not add the subtask and features, you migh need to change this part slightly 
    task_feature = task["feature"]
    success_range = success_probabilities[task_feature][robot]
    success_samples = np.random.uniform(success_range[0], success_range[1], num_samples)
    return success_samples.mean(), success_samples.var()

# MPC function for sequential tasks
#TODO: tune parameters of num_samples, might need to change horizon in the future if needed
def mpc_task_allocation(robots, tasks, horizon=3, num_samples=100):
    """Perform MPC-based task allocation with Monte Carlo approximations."""
    allocation = []
    remaining_tasks = tasks.copy()
    
    while remaining_tasks:
        # Look ahead for the finite horizon
        horizon_tasks = remaining_tasks[:horizon]
        best_allocation = None
        best_cost = float("inf")
        
        for robot in robots:
            for task in horizon_tasks:
                # Simulate success probabilities using Monte Carlo
                mean_success, variance = monte_carlo_simulation(robot, task, num_samples)
                
                # Define a cost function (maximize success, minimize variance)
                #TODO: improve the cost function if needed
                cost = 1 - mean_success + 0.5 * variance
                
                # Update best allocation
                if cost < best_cost:
                    best_cost = cost
                    best_allocation = (robot, task, mean_success)
        
        # Allocate the best task and update the system
        if best_allocation:
            robot, task, success = best_allocation
            allocation.append((robot, task, success))
            remaining_tasks.remove(task)
            print(f"Assigned task {task['id']} ({task['feature']}) to robot {robot} "
                  f"with success probability {success:.2f}")
        else:
            print("No feasible allocation found for remaining tasks.")
            break
    
    return allocation

# Run the MPC task allocation
print("Task Sequence:", [(task["id"], task["feature"]) for task in tasks])
allocations = mpc_task_allocation(robots, tasks)

# Final allocations summary
print("\nFinal Allocations:")
for allocation in allocations:
    print(f"Robot {allocation[0]} -> Task {allocation[1]['id']} ({allocation[1]['feature']}) "
          f"(Success: {allocation[2]:.2f})")
