import os
import time

num_procs = [ 2, 3, 4, 5 6, 7]

if __name__ == "__main__":
    results_file = open("results.csv", "w")
    results_file.write("NumProcs, Time\n")
    for n in num_procs:
        for i in range(3):
            print "Trying with %d processes (%d)" % (n, i)
            start_time = time.time()
            os.system("python ../yd-batch.py -n %d ../test_batch_files/big_files.txt > out" % n)
            elapsed_time = time.time() - start_time
            results_file.write("%d, %.3f\n" % (n, elapsed_time))
