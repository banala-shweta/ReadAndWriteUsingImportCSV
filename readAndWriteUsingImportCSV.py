# imported CSV to read and write 
import csv
# import date time to validate and format
import datetime
# import time to calculate time elapsed
import time

# The below code could be made to a single function, however for the re-usability, this has been split to multiple functions.


# Function to Validate Date Field
def validateDateAndConvertField(columnValue):
    try:
        # This below line of code helps to convert any field to date-time of required format. If any error, it throws exception
        return datetime.datetime.strptime(str(columnValue),"%Y%m%d").strftime("%Y-%m-%d"), ''
    except ValueError as err:
        # Caught exception is sent back to use it in error log
        return 'error', str(err)

# Function to Read CSV File and give two lists 
# 1. Output Result, 
# 2. Error if any
def readAndValidateDateFields(input_file_name):
    try:
        print('Reading {} file started'.format(input_file_name))

        # This below statement opens the file to read
        with open(input_file_name, 'r') as csvFile:

            # the open file read with a delimiter '\t'
            reader = csv.reader(csvFile, delimiter='\t')

            #Two lists for output and error if any
            output = []
            errorOutput = []

            #looping through each row with an index to remove header row
            for idx, row in enumerate(reader):
                rowResult = []
                error = []

                # header row added default 
                if idx == 0:
                    output.append(row)
                    errorOutput.append(row)
                # all rows except header
                else:
                #looping through each column with an index to exclusively target date fields
                    for index, colunmnValue in enumerate(row):                   
                       if index != 9 and index != 10:
                        rowResult.append(colunmnValue)
                       else:
                         convertedValue, errorMessage = validateDateAndConvertField(colunmnValue)

                         if len(errorMessage) == 0:
                             # only converted value is appended to the row
                            rowResult.append(convertedValue)
                         else:
                             rowResult.append(errorMessage)
                             #  All individual errors are added as a list to get error count
                             error.append(errorMessage)
                
                #if no error added to output
                if len(error) == 0:
                    output.append(rowResult)
                # else added to the error output
                else:
                    errorOutput.append(rowResult)

                # setting back error list to 0
                error = []

            print('Reading {} file completed'.format(input_file_name))
            # returns both output as well as error
            return output, error

    except IOError:
        print('An error occurred trying to read the file.')    
    except ImportError:
        print("No module found")    
    except :
        raise


# Function to Read and Write to CSV File just using CSV
def readandexporttocsv2(input_file_name):
    try:
        output, errorOutput = readAndValidateDateFields(input_file_name)  
        writeToCSV('output.csv', output)
        if len(errorOutput) > 1:
            writeToCSV('error.csv', errorOutput)

    except IOError:
        print('An error occurred trying to read the file.')    
    except ImportError:
        print("No module found")    
    except :
        raise



# Function to Write CSV File 
def writeToCSV(outputFileName, list):
    try:
        print('Writing {} file started'.format(outputFileName))
        with open(outputFileName, 'w', newline='') as f:
            csv_writer = csv.writer(f, delimiter='\t')
            for r in list:
                if len(r) > 0:
                    csv_writer.writerow(r)
        print('Writing {} file ended'.format(outputFileName))
        print('No.  of rows successfully exported to ' +  outputFileName + ' is ' + str(len(list)))
    except ImportError:
        print("No module found")    
    except :
        raise



input_file_name = 'sample_input.csv'


tic = time.process_time()
readandexporttocsv2(input_file_name)
toc = time.process_time()
print('Time Elapsed for Read, Validating and Writing using CSV is: ', str(toc - tic))






