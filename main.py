import subprocess
import time
import datetime

# Start time
st = time.time()
if __name__=='__main__':

    # 0. Preprocessing raw data and metadata
    print("Now running: preprocess.py...")
    subprocess.run(["python", "preprocess.py"])
    time.sleep(1)
    print("Done.")

    # 1. Parsing
    print("Now running: parse.py...")
    subprocess.run(["python", "parse.py"])
    time.sleep(1)
    print("Done.")

    # 2. Cleaning and training
    print("Now running: clean_and_train.py...")
    subprocess.run(["python", "clean_and_train.py"])
    time.sleep(1)
    print("Done.")

    # 3. Creating dictionary
    print("Now running: create_dict.py...")
    subprocess.run(["python", "create_dict.py"])
    time.sleep(1)
    print("Done.")

    # 4. Scoring
    print("Now running: score.py...")
    subprocess.run(["python", "score.py"]) 
    time.sleep(1)
    print("Done.")

    # 5. Aggregating firms
    print("Now running: aggregate_firms.py...")
    subprocess.run(["python", "aggregate_firms.py"])
    time.sleep(1)
    print("Done.")

    # End time
    et = time.time()

    # Execution time
    elapsed_time = et - st
    elapsed_time = datetime.timedelta(seconds = round(elapsed_time, 2))
    print("\nAll done!") 
    print('Execution time:', elapsed_time)

 