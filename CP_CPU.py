import matplotlib.pyplot as plt
from datetime import datetime

def extract_and_clean_show_clock_lines(file_path):
    """
    Extracts and cleans lines containing "show clock @" by removing specified substrings.

    :param file_path: Path to the file to be read.
    :return: A list containing cleaned lines with the string "show clock @".
    """
    cleaned_lines = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                if "show clock @" in line:
                    # Remove specified substrings
                    cleaned_line = line.replace("------------------ show clock @", "").replace("------------------", "").strip()
                    cleaned_lines.append(cleaned_line)

        return cleaned_lines

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def extract_and_clean_control_plane_lines(file_path):
    """
    Extracts lines that come after lines containing "Current control plane usage versus the control plane cores elapsed for:"
    and removes specified substrings.

    :param file_path: Path to the file to be read.
    :return: A list of cleaned lines following the specified string.
    """
    cleaned_lines = []

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if "Current control plane usage versus the control plane cores elapsed for:" in line:
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        # Remove "5 seconds =" and all data after "%;"
                        value_start = next_line.find("5 seconds =") + len("5 seconds =")
                        value_end = next_line.find("%;")
                        cleaned_line = next_line[value_start:value_end].strip()
                        cleaned_lines.append(cleaned_line)

        return cleaned_lines

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def calculate_average(values):
    """
    Calculates the average of a list of float values.

    :param values: List of float values.
    :return: The average value rounded to the nearest decimal number.
    """
    float_values = [float(value) for value in values]
    average = sum(float_values) / len(float_values) if float_values else 0
    return round(average, 1)

def plot_time_value_graph(times, values):
    """
    Plots a time-value graph using matplotlib.

    :param times: List of strings representing times.
    :param values: List of float values representing corresponding values.
    """
    # Convert time strings to datetime objects
    time_objects = [datetime.strptime(time, "%Y/%m/%d %H:%M:%S") for time in times]

    # Convert value strings to floats
    value_objects = [float(value) for value in values]

    plt.figure(figsize=(10, 6))
    plt.plot(time_objects, value_objects, marker='o', linestyle='-')
    plt.title("Time-Value Graph")
    plt.xlabel("Time")
    plt.ylabel("Value (%)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    file_path = input("Enter the file path: ")

    cleaned_show_clock_lines = extract_and_clean_show_clock_lines(file_path)
    cleaned_control_plane_lines = extract_and_clean_control_plane_lines(file_path)

    # Calculate and print the average of the values in the second list
    average_value = calculate_average(cleaned_control_plane_lines)
    print(f"Average of control plane values: {average_value}")

    # Plot the graph if both lists have the same length
    if len(cleaned_show_clock_lines) == len(cleaned_control_plane_lines):
        plot_time_value_graph(cleaned_show_clock_lines, cleaned_control_plane_lines)
    else:
        print("Error: The number of time entries does not match the number of value entries.")

if __name__ == "__main__":
    main()
