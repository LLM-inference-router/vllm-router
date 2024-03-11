import os
from requests import post
import threading
import random
import datetime

directory = "test-data"

# Router URL
url = "http://10.102.7.189:8000/v1/completions"
model = "meta-llama/Llama-2-7b-chat-hf"
num_threads = 5

# List to store the lines
lines = []

# Read files from the directory
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath):
        with open(filepath, "r") as file:
            # Read lines from the file
            file_lines = file.readlines()
            # Strip empty lines and add to the list
            lines.extend([line.strip() for line in file_lines if line.strip()])

# Send each line as a POST request
def send_post(lines):
    # Prepare the data for the POST request
    for line in lines:
        data = {
            "prompt": line,
            "model": model,
            "max_tokens": 1000,
            "temperature": 1
        }
        
        # Send the POST request
        response = post(url, json=data, headers={"Content-Type": "application/json"})

    #print(response.text)

def random_send_post(lines):
    # randomly chooose a line from lines and send it, do it over len(lines) times
    for i in range(len(lines)):
        random_line = random.choice(lines)
        data = {
            "prompt": random_line,
            "model": model,
            "max_tokens": 1000,
            "temperature": 1
        }
        response = post(url, json=data, headers={"Content-Type": "application/json"})

    #print(response.text)
# Create a list to store the threads
def run_threads(func):
    threads = []

    # print the start time of the program and end time of the program
    print("Start time")
    start_time = datetime.datetime.now()
    print(start_time)
    # Create and start 5 threads
    for i in range(num_threads):
        thread = threading.Thread(target=func, args=(lines,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("End time")
    end_time = datetime.datetime.now()
    print(end_time)
    # print the difference between the start time and end time
    print("Difference")
    print(end_time - start_time)


# Run the threads
print("Sending POST requests")
run_threads(send_post)
print("Sending Random POST requests")
run_threads(random_send_post)