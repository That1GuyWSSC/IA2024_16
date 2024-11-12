# FILE: teste.py
import re
from constraint import Problem
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint

def parse_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    
    sections = re.split(r'\*{72}', content)
    
    precedence_relations = sections[3]
    durations_resources = sections[4]
    resource_availability = sections[5]
    
    return precedence_relations, durations_resources, resource_availability

def parse_precedence_relations(precedence_relations):
    jobs = {}
    lines = precedence_relations.strip().split('\n')[2:]
    print("Precedence Relations Lines:", lines)  # Debugging line
    for line in lines:
        parts = line.split()
        print("Line Parts:", parts)  # Debugging line
        jobnr = int(parts[0])
        successors = list(map(int, parts[3:]))
        jobs[jobnr] = successors
    return jobs

def parse_durations_resources(durations_resources):
    durations = {}
    lines = durations_resources.strip().split('\n')[2:]
    print("Durations and Resources Lines:", lines)  # Debugging line
    for line in lines:
        parts = line.split()
        print("Line Parts:", parts)  # Debugging line
        jobnr = int(parts[0])
        duration = int(parts[2])
        durations[jobnr] = duration
    return durations

def parse_resource_availability(resource_availability):
    resources = {}
    lines = resource_availability.strip().split('\n')[2:]
    print("Resource Availability Lines:", lines)  # Debugging line
    for line in lines:
        parts = line.split()
        print("Line Parts:", parts)  # Debugging line
        resource = parts[0]
        qty = int(parts[1])
        resources[resource] = qty
    return resources

def main():
    filename = 'my_p01_dataset_8.txt'
    precedence_relations, durations_resources, resource_availability = parse_file(filename)
    
    jobs = parse_precedence_relations(precedence_relations)
    durations = parse_durations_resources(durations_resources)
    resources = parse_resource_availability(resource_availability)
    
    print("Jobs:", jobs)
    print("Durations:", durations)
    print("Resources:", resources)
    
    problem = Problem()
    
    # Add variables to the problem
    for job in jobs:
        if job in durations:
            problem.addVariable(job, range(1, max(durations.values()) + 1))
        else:
            print(f"Warning: Job {job} is mentioned in precedence relations but not defined in durations.")
    
    # Add constraints to the problem
    for job, successors in jobs.items():
        for successor in successors:
            if successor in durations:
                problem.addConstraint(lambda x, y: x < y, (job, successor))
            else:
                print(f"Warning: Successor {successor} is mentioned in precedence relations but not defined in durations.")
    
    # Ensure the first job starts on the first day
    first_job = list(jobs.keys())[0]
    problem.addConstraint(lambda x: x == 1, (first_job,))

    # Get the solution
    solution = problem.getSolution()
    print("Solution:", solution)
   

    # Create a graph to visualize the solution
    G = nx.DiGraph()

    # Add nodes with start times as labels
    for job, start_time in solution.items():
        G.add_node(job, label=f"{job}\nStart: {start_time}")

    # Add edges based on job dependencies
    for job, successors in jobs.items():
        for successor in successors:
            G.add_edge(job, successor)

    # Draw the graph
    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')
    plt.title("Job Scheduling Solution")
    plt.show()

if __name__ == "__main__":
    main()