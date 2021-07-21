#!/usr/bin/env python3

import re

nodes = []
cells = []
unique_paths = []
path_list = []
pruned_clusters = []
pruned_cells = []
store_newick = ""
cell_dict = {}
cluster_dict = {}

newick_file = input('Please input the path to your newick file (no quotes, absolute or relative to current path)\nPath_to_newick_file= ')

# open Newick file and store cell IDs in a list and 
for line in open(newick_file):
#for line in open('casper_dendro'):
	store_newick += line
	# regular expression to extract individual cell IDs
	cell_ids = re.findall(r'[(),]+\'([^;:]+)\b',line)
	for ID in cell_ids:
		cells.append(ID)
	if len(cells) == 0:
		cell_ids = re.sub(r':0','',line)
		if cell_ids:
			cell_ids = re.findall(r'[^:(,\d.](\w+)',cell_ids)
			for ID in cell_ids:
				cells.append(ID)

# Parse through Newick Structure and generates codified tree structure for desiired clusters
path_lengths = []
for ID in cells:
	node = [1]
	for x, i in enumerate(store_newick):
		if i == "(":
			node.append(1)
			closed = False
		if i == ")":
			node.pop(len(node)-1)
			node[-1] += 1
			closed = True
		if i == ",":
			if closed != True:
				node[-1] += 1
		if store_newick[x:(x+len(ID))] == ID:
			# Adds to list of starting nodes for each leaf
			nodes.append(node)
			# Stores the length of each node
			path_lengths.append(len(node))
			# The leaf/cell ID is used as a key for node values
			cell_dict[ID] = node
			break

# Process unrooted trees
for k,v in cell_dict.items():
	for i in v:
		if i > 2:
			print('Unrooted tree detected!')
			v = '.'.join(str(i) for i in v)
			pruned = k+': '+v
			pruned_clusters.append(pruned)
			pruned_cells.append(k)

for cell in pruned_cells:
	if cell in cell_dict.keys():
		print('PRUNING')
		cell_dict.pop(cell)

# Store the length of the longest branch
try:
	longest_branch = max(path_lengths)
except ValueError:
	print('Your input Newick file does not contain distance values!')
# Store the number of individual leafs represented in the sample
if len(pruned_clusters) > 0 :
	leaf_count = len(cells) - len(pruned_clusters)
else:
	leaf_count = len(cells)


print('###########################################################')
print('###########################################################')
print('#################   USER_INPUT    #########################')
print('###########################################################\n')
# The following inputs allow the user to stack leaves into manageable clusters
print('Your tree currently has {} individual leaves'.format(leaf_count))
try:
	print('The longest branch in your tree is forked {} times'.format(longest_branch))
except NameError:
	pass
cut_length = input("How long do you want your tree? (input an integer)\n> Length = ")
print('\n')
output_file = input("Name your output file:\n> File = ")
print('###########################################################')
print('###########################################################')
print('###########################################################')
print('###########################################################\n')


new_nodes = []
for node in nodes:
	cap_newnodes = []
	# try: catch trees that are smaller
	cap_newnodes.append(node[:int(cut_length)])
	new_nodes.append(cap_newnodes)

if len(cells) == len(new_nodes):
	# cell_groupings = j for i, j in list(zip(cells,new_nodes))
	with open('Inputs/'+output_file+'.cell_groupings','w') as out:
		cell_groupings = list(zip(cells,new_nodes))
		for x in cell_groupings:
			cell = x[0]
			path = x[1][0]
			cell_address = '.'.join(str(i) for i in path)
			out.write('all_observations.all_observations.'+cell_address+'\t'+cell+'\n')
			path = ''.join(str(i) for i in path)
			path = int(path)
			path_list.append(path)
			if path not in unique_paths:
				unique_paths.append(path)
		out.close()
	cluster_num = len(unique_paths)
	for element in unique_paths:
		count = path_list.count(element)
		cluster_dict[element] = count

print('This configuration will stack the leaves of your tree into {} clusters'.format(cluster_num))
small_clusters = 0
not_plotted =[]
for k,v in cluster_dict.items():
		if (v/leaf_count*100) < 5:
			small_clusters += 1
			not_plotted.append(k)
if small_clusters > 1:
	print('There are {} clusters that are smaller than 5% of the total cell population, these will not be plotted.'.format(small_clusters))
	print("Not Plotted Clusters: ",not_plotted)
elif small_clusters == 0:
	print('There are 0 clusters that are smaller than 5% of the total cell population, your entire tree will be plotted')
elif small_clusters == 1:
	print('There is 1 cluster that is smaller than 5% of the total cell population, it will not be plotted')
