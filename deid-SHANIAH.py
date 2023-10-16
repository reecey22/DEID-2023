# Import necessary libraries
import re  # Import the regular expressions library
import sys  # Import the system-specific library

# Define a regular expression pattern for identifying names that begin with titles (Mr., Ms., or Mrs.), case insensitive
name_pattern = r'(?:[Mm]r\.|[Mm]s\.|[Mm]rs\.) [A-Za-z][a-z][A-Za-z][a-z]+'

# Open and read the 'PTName.phi' file
with open('C:/Users/Shaniah Reece/OneDrive/Documents/BMI500/DEID-2023/python/PTName.phi') as file:
    for line in file:
        patient_note = line.strip()  # Remove leading and trailing whitespace
        # Apply the regular expression to the current line and find matched names
        matched_names = re.findall(name_pattern, patient_note, re.I)  # 're.I' makes the regex case insensitive
        
        # Print or save the matched names to verify correctness
        if matched_names:
            print(f"Matched names in '{patient_note}': {matched_names}")

# Compile the regular expression for better performance
name_reg = re.compile(name_pattern)

def check_for_name(patient, note, chunk, output_handle):
    """
    This function checks for names in a given text chunk and writes the results to an output file.

    Inputs:
        - patient: Patient Name, will be printed in each occurrence of personal information found.
        - note: Note Number, will be printed in each occurrence of personal information found.
        - chunk: One whole record of a patient.
        - output_handle: An opened file handle to write the results.
    """
    # Define an offset to adjust position due to differences from Perl code
    offset = 27

    # For each new note, write the "Patient X Note Y" line to the output file
    output_handle.write(f'Patient {patient}\tNote {note}\n')

    # Search the whole chunk for name occurrences and write results to the output file
    for match in name_reg.finditer(chunk):
        # Debug print on the screen (not written to the output file)
        print(f'{patient} {note}', end=' ')
        print((match.start() - offset), match.end() - offset, match.group())

        # Create a string to write to the output file in the format 'start start end'
        result = f'{match.start() - offset} {match.start() - offset} {match.end() - offset}'

        # Write the result to one line of the output file
        output_handle.write(result + '\n')

def deid_name(text_path = "C:/Users/Shaniah Reece/OneDrive/Documents/BMI500/DEID-2023/python/id.text", output_path = 'C:/Users/Shaniah Reece/OneDrive/Documents/BMI500/DEID-2023/python/PTName.phi'):
    """
    This function de-identifies personal information in patient records.

    Inputs:
        - text_path: Path to the file containing patient records.
        - output_path: Path to the output file.
    """
    # Define a regular expression pattern to match the start of each note
    start_of_record_pattern = '^start_of_record=(\d+)\|\|\|\|(\d+)\|\|\|\|$'
    # Define a regular expression pattern to match the end of each note
    end_of_record_pattern = '\|\|\|\|END_OF_RECORD$'

    # Open the output file just once to save time on the time-intensive I/O
    with open(output_path, 'w+') as output_file:
        with open(text_path) as text:
            # Initialize an empty chunk. Go through the input file line by line.
            # Whenever we see the start_of_record pattern, note patient and note numbers and start
            # adding everything to the 'chunk' until we see the end_of_record.
            chunk = ''
            for line in text:
                record_start = re.findall(start_of_record_pattern, line, flags=re.IGNORECASE)
                if len(record_start):
                    patient, note = record_start[0]
                chunk += line

                # Check to see if we have seen the end of one note
                record_end = re.findall(end_of_record_pattern, line, flags=re.IGNORECASE)

                if len(record_end):
                    # Now we have a full patient note stored in 'chunk', along with patient number and note number.
                    # Pass all to check_for_name to find any name numbers in the note.
                    check_for_name(patient, note, chunk.strip(), output_file)

                    # Initialize the chunk for the next note to be read
                    chunk = ''

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) == 1:
        deid_name()
    else:
        deid_name(sys.argv[1], sys.argv[2])
