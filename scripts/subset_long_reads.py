import argparse
import numpy as np
import os
# Functions
def parse_args():
	parser = argparse.ArgumentParser(description = """
	Tool to remove short reads from nanopore fastq and convert to fasta format
	""")
	parser.add_argument("file", type=str, \
		help="Path to concatenated fastq file")
	parser.add_argument("out", type=str, \
		help="Path to subsetted fasta file")
	parser.add_argument("--median", type=int, \
		help="Remove reads until the median read length is this value")
	parser.add_argument("--min", type=int, \
		help="Remove all reads shorter than this length")
	return parser.parse_args()

def get_lengths(filename):
	lines = [line.rstrip() for line in open(filename, 'r')]
	lengths = []

	for seq in lines[1::4]:
		lengths.append(len(seq))
	return lengths

def get_median(lengths:int):
	return np.median(lengths)

def count_seqs(lengths, n:int, greater = True):
	count = 0

	for s in lengths:
		if greater:
			if s >= n:
				count += 1
		else:
			if s <= n:
				count += 1
	return count

def set_median(median:int, lengths):
	lengths.sort()
	m = get_median(lengths)

	if  m > median:
		n = count_seqs(lengths, median, True) - count_seqs(lengths, m, True)
		return (n, "max")
	elif m < median:
		n = count_seqs(lengths, median, False) - count_seqs(lengths, m, False)
		return (n, "min")

def main():
	args = parse_args()
	filename = args.file
	output = os.path.abspath(args.out)
	median = args.median
	min_length = args.min

	if not median and not min_length:
		raise Exception("You need to specify a minimum or median read length!")
	if median and min_length:
		raise Exception("Please choose either a minimum or median read length!")


	if min_length is None:
		l = get_lengths(filename)
		cutoff = set_median(median, l)
	else:
		cutoff = (min_length, "min")

	count = 0

	with open(filename, "r") as f:
		lines = f.readlines()
		names = lines[0::4]
		seqs = lines[1::4]

	with open(output, "w+") as out:
		for i in range(0, len(seqs)):
			if cutoff[1] == "min":
				if len(seqs[i]) >= cutoff[0]:
					count += 1
					out.write(">" + names[i][1:] + seqs[i])
			elif cutoff[1] == "max":
				if len(seqs[i]) <= cutoff[0]:
					count += 1
					out.write(">" + names[i][1:] + seqs[i])

	print(f"{count} sequences written to {output}")


if __name__ == '__main__':
	main()
