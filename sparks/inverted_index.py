from pyspark import SparkConf, SparkContext
import time
import os
import shutil
import psutil
import sys
print(sys.path)
sys.path.append('/home/developer/.local/lib/python3.10/site-packages')

def create_inverted_index(sc, input_path, output_path):
    abs_path = os.path.abspath(input_path)
    print(f"Attempting to read from: {abs_path}")

    # Check if the output directory exists and delete it if it does
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
        print(f"Deleted existing directory: {output_path}")

    # Read files and create RDD
    files_rdd = sc.parallelize([(root, filename) for root, _, filenames in os.walk(abs_path)
                                for filename in filenames if filename.endswith('.txt')])

    if files_rdd.isEmpty():
        print("No files found at specified path.")
        return
    else:
        print(f"Number of documents read: {files_rdd.count()}")

    # Create inverted index
    word_doc_pairs = files_rdd.flatMap(lambda x: [(word, os.path.join(x[0], x[1]))
                                                  for word in open(os.path.join(x[0], x[1]), 'r', encoding='utf-8').read().split()])
    inverted_index = word_doc_pairs.groupByKey().mapValues(list)
    inverted_index = inverted_index.map(lambda x: (x[0], list(set(x[1]))))

    # Save the readable index
    save_readable_index(inverted_index, output_path)

def save_readable_index(index_rdd, output_path):
    formatted_rdd = index_rdd.map(lambda x: f"{x[0]}: {', '.join(x[1])}")
    formatted_rdd.saveAsTextFile(output_path)

def run_spark_job(num_executors, input_path, output_path):
    conf = SparkConf().setAppName("InvertedIndex").setMaster(f"local[{num_executors}]")
    sc = SparkContext(conf=conf)

    # Start measuring CPU usage
    cpu_usage_start = psutil.cpu_percent(interval=1)

    start_time = time.time()
    create_inverted_index(sc, input_path, output_path)
    duration = time.time() - start_time

    # Measure CPU usage again
    cpu_usage_end = psutil.cpu_percent(interval=1)

    sc.stop()
    return duration, cpu_usage_start, cpu_usage_end

def main():
    if len(sys.argv) != 4:
        print("Usage: script.py <input_path> <output_path> <num_executors>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    num_executors_list = sys.argv[3].split('-')

    results = []
    for num_executors in num_executors_list:
        print(f"\n\nRunning with {num_executors} executors...")
        exec_time, cpu_start, cpu_end = run_spark_job(num_executors, input_path, output_path)
        results.append((num_executors, exec_time, cpu_start, cpu_end))
        print(f"Time taken with {num_executors} executors: {exec_time} seconds")

    # Save performance metrics
    with open(os.path.join(output_path, "performance_metrics.txt"), "w") as f:
        f.write("Executors,\t\tTime(s),\t\tInitial and final CPU(%),\tTime Change(%)\n")
        previous_time = None
        for idx, (num_executors, exec_time, cpu_start, cpu_end) in enumerate(results):
            time_change = ((exec_time - (results[idx-1][1] if idx > 0 else exec_time)) / (results[idx-1][1] if idx > 0 else 1)) * 100
            f.write(f"\n{num_executors} ==>\t\t{exec_time}\t\t{cpu_start}%\t\t{cpu_end}%,\t\t{time_change:.2f}%\n")

if __name__ == "__main__":
    main()
