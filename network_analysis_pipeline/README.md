# Network analysis pipeline

The graphs directory contains a directory called format_scy in which I have put a directory called test_examples which has a few very simple, small graphs written in a file format that can be read by the saucy program. Within the format_scy folder I imagine having directories of graphs that are related in some way. Within the graphs directory, I imagine we could have graphs in different formats.

The gaut directory contains the python code that runs saucy for individual files (run_saucy.py) and batches (run_batch_saucy.py). (This uses a binary called "saucy" that runs the saucy code, which would need to be produced on a given machine.) There is a directory test_examples that contains the results of running run_batch_saucy.py.

The gap directory contains python code that converts the output of saucy into a format that is readable by gap for an individual file (run_gaut2gap.py) and for batches (run_batch_gaut2gap.py). There is a directory test_examples that contains the results of running run_batch_gaut2gap.py.

