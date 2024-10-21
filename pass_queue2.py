import json
import random
import os

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    print(f"Successfully loaded file at {file_path}")

def save_json(data, file_path):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Successfully saved to {file_path}")


def split_guests(guest_data):
    """Split guests into individual units based on their color and number."""
    passengers = []
    for guest in guest_data:
        passengers.extend([guest['eColor']] * guest['number'])
    return passengers

def group_passengers(passengers):
    """Group consecutive passengers of the same color."""
    grouped = []
    if not passengers:
        return grouped

    current_color = passengers[0]
    count = 1
    for passenger in passengers[1:]:
        if passenger == current_color:
            count += 1
        else:
            grouped.append({"eColor": current_color, "number": count})
            current_color = passenger
            count = 1
    grouped.append({"eColor": current_color, "number": count})
    return grouped

def create_clusters(passengers, cluster_size):
    """Create clusters based on the number of different colors."""
    clusters = []
    cluster = []
    colors_in_cluster = set()
    for passenger in passengers:
        if len(colors_in_cluster) < cluster_size or passenger in colors_in_cluster:
            cluster.append(passenger)
            colors_in_cluster.add(passenger)
        else:
            clusters.append(cluster)
            cluster = [passenger]
            colors_in_cluster = {passenger}
    if cluster:
        clusters.append(cluster)
    return clusters

def randomize_cluster(cluster, min_split):
    """Randomly shuffle passengers in a cluster after splitting based on min_split."""
    # Split groups larger than min_split
    split_cluster = []
    for group in group_passengers(cluster):
        eColor = group['eColor']
        number = group['number']
        while number > 0:
            split_size = min(min_split, number)
            split_cluster.extend([eColor] * split_size)
            number -= split_size
    random.shuffle(split_cluster)
    return split_cluster

def process_guests(guest_data):
    passengers = split_guests(guest_data)
    total_passengers = len(passengers)
    print(f"Total passengers: {total_passengers}")
    print("Non-clustered passengers:", passengers)

    clusters = []
    while passengers:
        cluster_size = int(input("Enter the number of colors to group into this cluster: "))
        cluster = create_clusters(passengers, cluster_size)[0]  # Take the first cluster formed
        clusters.append(cluster)
        passengers = passengers[len(cluster):]  # Reduce passengers by the cluster size
        print(f"{len(passengers)} passengers remaining.")

    print(f"\nTotal clusters formed: {len(clusters)}")
    for i, cluster in enumerate(clusters):
        print(f"Cluster {i+1}: {len(set(cluster))} colors, {len(cluster)} passengers")

    # Process each cluster
    for i, cluster in enumerate(clusters):
        randomize = input(f"Do you want to randomize Cluster {i+1}? (1/0): ")
        if randomize == '1':
            min_split = int(input("Enter the minimum number to split each group: "))
            randomized_cluster = randomize_cluster(cluster, min_split)
            grouped_cluster = group_passengers(randomized_cluster)
            clusters[i] = grouped_cluster

    # Flatten the clusters back into a list of passengers (no nested structure)
    flattened_passengers = [p for cluster in clusters for p in cluster]
    
    return flattened_passengers  # Return the correct list of grouped passengers

def modify_json(file_path, fail_safe):
    data = load_json(file_path)
    save_json(data, fail_safe)
    # Process the guest data with manual clustering and randomization
    data['guestDatas'] = process_guests(data['guestDatas'])

    # Save the modified data back to the JSON file
    save_json(data, file_path)
    print()

# All the functions you defined remain the same above...
# file_path = "D:/Downloads/GD_works/Bus_frenzy/ToolBusOut (6)/ToolBusOut/TestLevelBusOut/Bus Out_Data/Levels/20081.json"
file_path = "C:/Users/ADMIN/Downloads/2002.json"
fail_safe = "D:/Downloads/GD_works/Bus_frenzy/ToolBusOut (6)/ToolBusOut/TestLevelBusOut/Bus Out_Data/Levels/fail_safe/fail_safe.json"

# To ensure the function will only be call when run the main file:
if __name__ == "__main__":
    modify_json(file_path, fail_safe)

# file_path = "D:/Downloads/GD_works/Bus_frenzy/ToolBusOut (6)/ToolBusOut/TestLevelBusOut/Bus Out_Data/Levels/10008.json"
# fail_safe = "D:/Downloads/GD_works/Bus_frenzy/ToolBusOut (6)/ToolBusOut/TestLevelBusOut/Bus Out_Data/Levels/fail_safe/fail_safe.json"
# modify_json(file_path, fail_safe)
