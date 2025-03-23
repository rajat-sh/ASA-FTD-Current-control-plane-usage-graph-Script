import matplotlib.pyplot as plt
from datetime import datetime

def extract_show_clock_lines(file_path):
    """
    Extracts and converts lines containing "show clock @" to datetime objects,
    removing specified substrings.

    :param file_path: Path to the file to be read.
    :return: A list (T) containing cleaned lines as datetime objects.
    """
    list_t = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                if "show clock @" in line:
                    # Remove specified substrings and convert to datetime
                    cleaned_line = line.replace("------------------ show clock @", "").replace("------------------", "").strip()
                    time_obj = datetime.strptime(cleaned_line, "%Y/%m/%d %H:%M:%S")
                    list_t.append(time_obj)

        return list_t

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def extract_control_plane_lines(file_path):
    """
    Extracts lines after "Current control plane usage versus the control plane cores elapsed for:"
    and processes them into three lists based on specified substrings.

    :param file_path: Path to the file to be read.
    :return: Three lists (A, B, C) containing processed lines based on different time intervals.
    """
    list_a = []
    list_b = []
    list_c = []

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if "Current control plane usage versus the control plane cores elapsed for:" in line:
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()

                        # Extract data for list A
                        value_start = next_line.find("5 seconds =") + len("5 seconds =")
                        value_end = next_line.find("%;")
                        if value_start != -1 and value_end != -1:
                            list_a.append(float(next_line[value_start:value_end].strip()))

                        # Extract data for list B
                        value_start = next_line.find("1 minute:") + len("1 minute:")
                        value_end = next_line.find("%; 5 minutes")
                        if value_start != -1 and value_end != -1:
                            list_b.append(float(next_line[value_start:value_end].strip()))

                        # Extract data for list C
                        value_start = next_line.find("5 minutes:") + len("5 minutes:")
                        list_c_element = next_line[value_start:].replace("%", "").strip()
                        if value_start != -1:
                            list_c.append(float(list_c_element))

        return list_a, list_b, list_c

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return [], [], []
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], [], []

def calculate_average(values):
    """
    Calculates the average of a list of float values rounded to the nearest decimal.

    :param values: List of float values.
    :return: The average value rounded to the nearest decimal.
    """
    return round(sum(values) / len(values), 1) if values else 0

def plot_time_value_graph(times, values, title):
    """
    Plots a time-value graph using matplotlib.

    :param times: List of datetime objects representing times.
    :param values: List of float values representing corresponding values.
    :param title: Title of the graph.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(times, values, marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Usage (%)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    file_path = input("Enter the file path: ")

    list_t = extract_show_clock_lines(file_path)
    list_a, list_b, list_c = extract_control_plane_lines(file_path)

    # Calculate and print averages rounded to nearest decimal
    print("\nAverage of 5 seconds CP CPU Usage:")
    print(calculate_average(list_a))

    print("\nAverage of 1 minute CP CPU Usage:")
    print(calculate_average(list_b))

    print("\nAverage of 5 minute CP CPU Usage:")
    print(calculate_average(list_c))

    # Plot graphs for lists A, B, and C
    if len(list_t) == len(list_a):
        plot_time_value_graph(list_t, list_a, "5 seconds CP CPU Usage")
    if len(list_t) == len(list_b):
        plot_time_value_graph(list_t, list_b, "1 minute CP CPU Usage")
    if len(list_t) == len(list_c):
        plot_time_value_graph(list_t, list_c, "5 minute CP CPU Usage")

if __name__ == "__main__":
    main()
