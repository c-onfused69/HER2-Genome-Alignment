import os

def preprocess_data(genome_sequence):
    return ''.join([char for char in genome_sequence if char in 'ATCG'])

def smith_waterman(seq1, seq2, match=2, mismatch=-1, gap=-1):
    m, n = len(seq1), len(seq2)
    
    score_matrix = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match_score = score_matrix[i - 1][j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch)
            delete_score = score_matrix[i - 1][j] + gap
            insert_score = score_matrix[i][j - 1] + gap
            score_matrix[i][j] = max(0, match_score, delete_score, insert_score)

    # Find the maximum score and its position
    max_score = 0
    max_position = (0, 0)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if score_matrix[i][j] > max_score:
                max_score = score_matrix[i][j]
                max_position = (i, j)

    # Reconstruct the alignment
    alignment1 = ""
    alignment2 = ""
    i, j = max_position
    while score_matrix[i][j] > 0:
        if seq1[i - 1] == seq2[j - 1]:
            alignment1 = seq1[i - 1] + alignment1
            alignment2 = seq2[j - 1] + alignment2
        elif score_matrix[i - 1][j - 1] + match == score_matrix[i][j]:
            alignment1 = seq1[i - 1] + alignment1
            alignment2 = seq2[j - 1] + alignment2
        elif score_matrix[i - 1][j] + gap == score_matrix[i][j]:
            alignment1 = seq1[i - 1] + alignment1
            alignment2 = "-" + alignment2
        else:
            alignment1 = "-" + alignment1
            alignment2 = seq2[j - 1] + alignment2
        if i > 1 and j > 1:
            i -= 1
            j -= 1
        else:
            break

    return max_score, alignment1, alignment2

def main():
    # Specify the directory containing the genome dataset files
    directory = "C:\\Users\\DELL\\Desktop\\exam\\HER2_datasets\\ncbi_dataset\\data"

    # Check if the directory exists
    if not os.path.exists(directory):
        print("Error: The directory does not exist.")
        return

    # Read the genome sequence from the file
    with open(os.path.join(directory, "gene.fna"), 'r') as file:
        genome_sequence = file.read()

    print("Selected Genome Sequence:")
    print(genome_sequence)

    # Preprocess the data
    preprocessed_sequence = preprocess_data(genome_sequence)
    print("Preprocessed Genome Sequence:")
    print(preprocessed_sequence)

    # Use the Smith-Waterman algorithm
    seq1 = preprocessed_sequence[:100]
    seq2 = preprocessed_sequence[100:200]
    max_score, alignment1, alignment2 = smith_waterman(seq1, seq2)
    print("Smith-Waterman Alignment:")
    print("Score:", max_score)
    print("Alignment 1:", alignment1)
    print("Alignment 2:", alignment2)

if __name__ == "__main__":
    main()