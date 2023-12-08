import argparse
import matplotlib.pyplot as plt
from collections import Counter


"""
    This script conducts an analysis of a text file comprising randomly sampled labels sourced from the TPME dataset,
    with a particular focus on paraphrases generated by GPT. The emphasis is on evaluating the frequency of the 'correct' label
    in various positions across sets of 10 consecutive lines.
    These positions correspond to lists of 10 paraphrases generated by GPT for each seed utterance.


    Usage:
        python analyze_labels.py -f/--file_path <path_to_text_file>

    Command-line Arguments:
        -f/--file_path: Path to the text file containing the sampled labels. (required)

    Script Flow:
    1. Reads the content of the specified text file.
    2. Validates that the total number of rows in the file is a multiple of 10.
    3. Processes the file data, counting the frequency of 'correct' labels for each position in sets of 10 consecutive lines.
    4. Displays a bar graph illustrating the distribution of 'correct' labels in each position.
"""


def read_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def count_correct_labels(lines):
    correct_frequency = Counter()
    line_count = 0

    for line in lines:
        correct_labels = line.strip().split(',')
        if correct_labels[0].find('correct') != -1:
            correct_frequency[line_count] += 1
        line_count = (line_count + 1) % 10

    return correct_frequency

def plot_bar_graph(correct_frequency):
    positions = list(correct_frequency.keys())
    frequencies = list(correct_frequency.values())
    
    plt.bar(positions, frequencies, color='#2e7bab')
    plt.xlabel('Position of the generated paraphrase')
    plt.ylabel('Frequency of "correct" label')
    plt.title('Frequency of "correct" label in each position generated by GPT')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Analyze a file with randomly sampled labels, counting error rates in positions over each set of 10 consecutive lines.")
    parser.add_argument('-f', '--file_path', help='Path to the text file.', required=True)
    args = parser.parse_args()

    lines = read_lines(args.file_path)

    if len(lines) % 10 != 0:
        print("The total number of rows in the file must be a multiple of 10.")
    else:
        correct_frequency = count_correct_labels(lines)
        plot_bar_graph(correct_frequency)

if __name__ == "__main__":
    main()