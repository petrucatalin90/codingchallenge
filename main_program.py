import csv, os, glob, random, time
#from datetime 
import datetime
from datetime import timedelta

# define folder path 
path = r"C:/workspace/files"
  
# move to working directory 
os.chdir(path)

#function to change date format to DD/MM/YYYY (when reading line from csv )
def format_date(input_value):
    dt_format = datetime.datetime.strptime(input_value, "%d-%m-%Y")
    return datetime.date.strftime(dt_format, "%d/%m/%Y")

#function to calculate random date    
def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))

def get_random_date(start, end, prop):
    return str_time_prop(start, end, "%d/%m/%Y", prop)

#function to generate .csv files
def export_csv(input_file_dir, output_file, my_random_date): 
    with open(input_file_dir, 'r') as input_file:
        csv_reader = csv.reader(input_file)
        with open(output_file, 'w', newline='') as result:
            csv_writer = csv.writer(result)
            for line in csv_reader:
                if(format_date(line[1]) == my_random_date): #format_date("02-12-2023") => 02/12/2023
                    newlines = [next(csv_reader) for line in range(10)]
            for i in newlines:
                csv_writer.writerow(i)

#function to get the next day 
def get_next_day(input_date, date_format="%d-%m-%Y"):
    input_date_format = datetime.datetime.strptime(input_date, date_format)
    next_day = input_date_format + timedelta(days=1)
    return next_day.strftime(date_format)

#function to clean working directory
def clean_directory(file_type):
    for filename in glob.glob(os.path.join(path,'*',file_type)):
        if os.path.exists(filename):
            print("Remove old file: " + filename)
            os.remove(filename)


#########Main program###########
#get any random date
my_random_date = get_random_date("01/09/2023", "15/12/2023", random.random())

#clean previuos results and predictions from directories
clean_directory('*_result.csv')
clean_directory('*_prediction.csv')

#check user input
while True:
    user_input = int(input("\nEnter number of files to be processed (1 or 2) : \n"))
    if user_input == 1 or user_input == 2:
        print("User entered " + str(user_input) + ".")
        print("The random date is " + str(my_random_date) + ".\n")
        break
    else:
        print("You made an error. Please choose 1 or 2")

#1. Parse each Stock Exchange and generate result files
list_subdirectories = next(os.walk(path))[1]
#print(list_subdirectories)

for i in list_subdirectories:
    subdir= (path + "/" + i)   
    nbFiles = sum([len(files) for r, d, files in os.walk(subdir)])   #number of files in each subdirectory
    #print("Directory " + subdir + " contains " + str(nbFiles) + " files")
    listFiles = os.listdir(subdir)  #list files in subdirectory
    for filename in listFiles:
        filename_import = subdir + "/" + filename
        filename_export = (filename_import[:-len(".csv")] + "_result.csv") #extract string until .csv and concatenate with _result.csv to get the filename_export
        if user_input == 1:
            #print("1: " + filename_import +  " " + filename_export)
            #generate .csv file for a given random date
            export_csv(filename_import, filename_export, my_random_date)
            break
        else:
            #print("2: " + filename_import +  " " + filename_export)
            #generate .csv file for a given random date
            export_csv(filename_import, filename_export, my_random_date)

#2. Predict next values
for filename in glob.glob(os.path.join(path,'*','*_result.csv')):
    if os.path.exists(filename):
        #extract string until .csv and concatenate with _prediction.csv to get the filename_prediction
        filename_prediction = (filename[:-len("_result.csv")] + "_prediction.csv").replace("\\","/") 
        #print("\nfilename_prediction: " + filename_prediction)
        
        list_stock_date = []
        list_stock_value = []
        with open(filename, 'r') as input_file:
            csv_reader = csv.reader(input_file)
            for line in csv_reader:
                stock_name = line[0]
                list_stock_date.append(line[1])
                list_stock_value.append(line[2])

        #n value
        reference_stock_value = float(max(list_stock_value))    
    
        # second highest stock value = n+1
        second_stock_date = get_next_day(max(list_stock_date))
        second_stock_value = float(sorted(set(list_stock_value))[-2]) 
        #print("\t>>>second_stock_date: " + str(second_stock_date))
        #print("\t>>>second_stock_value: " + str(second_stock_value))
        
        #n+2
        third_stock_date = get_next_day(second_stock_date)
        third_stock_value =  round((reference_stock_value + (abs(reference_stock_value-second_stock_value)/2)),2) 
        #print("\t>>>third_stock_date: " + str(third_stock_date))
        #print("\t>>>third_stock_value: " + str(third_stock_value))
        
        # n+3
        fourth_stock_date = get_next_day(third_stock_date)
        fourth_stock_value = round((reference_stock_value + (abs(third_stock_value-second_stock_value)/4)), 2)  
        #print("\t>>>fourth_stock_date: " + str(fourth_stock_date))
        #print("\t>>>fourth_stock_value: " + str(fourth_stock_value))
        
        list_prediction = []
        list_prediction.append([stock_name, second_stock_date, second_stock_value])
        list_prediction.append([stock_name, third_stock_date, third_stock_value])
        list_prediction.append([stock_name, fourth_stock_date, fourth_stock_value])

        with open(filename_prediction, 'w', newline='') as prediction_file:
            csv_writer = csv.writer(prediction_file)
            for i in range(len(list_prediction)):
                csv_writer.writerow(list_prediction[i])
                #print("Write line " + str(i) + ": " + str(list_prediction[i]))
