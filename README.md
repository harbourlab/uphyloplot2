# uphyloplot2 version 2.3
If you encounter any issues or to request features please open an issue on this github page, and state the version you are running.

Please cite  uphyloplot2: Visualizing Phylogenetic Trees from Single-Cell RNA-seq Data, Stefan Kurtenbach, Daniel A. Rodriguez, Michael A. Durante, J. William Harbour, bioRxiv 2020.05.25.115550; doi: https://doi.org/10.1101/2020.05.25.115550 

Draw phylogenetic trees of tumor evolution, as seen in our Nature communications paper (Nature Communications volume 11, Article number: 496 (2020). 


<img src="https://github.com/harbourlab/uphyloplot2/blob/master/Screen%20Shot%202019-06-26%20at%2010.43.48%20AM.png" width="300">


Uphyloplot2 takes input from CaSpER, HoneyBADGER, and InferCNV to generate evolutionary plots. Please follow the guide below to visualize your tree using inputs from all three programs. You can download example data from this github page to test the program.

1. Download uphyloplot2 and recreate the following directory structure:
   ../Uphyloplot2/
    - uphyloplot2.py
    - newick_input.py
    - Inputs/
          - infercnv.cell_groupings 

You must populate the "Inputs" folder with ".cell_groupings" files from your respective pipeline. Files can have any name as long as it ends in  ".cell_groupings".  
 
 2. Follow the appropriate guide below to pre-process your data:

INFERCNV:
To generate the necessary files, inferCNV needs to be run with HMM, which will produce the "HMM_CNV_predictions.HMMi6.rand_trees.hmm_mode-subclusters.Pnorm_0.5.cell_groupings” files used for plotting. cluster_by_groups should be set to FALSE when calling infercnv::run: 

<pre>
> infercnv_obj = infercnv::run(infercnv_obj,cutoff=1,out_dir="output_dir",cluster_by_groups=FALSE,plot_steps=T,scale_data=T,denoise=T,noise_filter=0.12,analysis_mode='subclusters',HMM_type='i6')
</pre>

The '.cell_groupings' file will be located in your R working directory under the path you specify with the 'out_dir=' parameter.
It is important that you remove the reference and/or control cells in the ".cell_groupings" file. For instance, if you followed the inferCNV tutorial on the test data provided, your '.cell_groupings' file contains a 'cell_group_name' and 'cell' column with rows in the following format:

<pre>
all_observations.all_observations.1.1.1.1	  MGH264_A01
...
all_references.all_references.1.1.1.1	  GTEX-111FC-3326-SM-5GZYV
</pre>

On a unix system, you can quickly remove the reference cell data with the following command, substituting your values where appropriate:
<pre>
sed '/^all_references/d' <  infercnv.cell_groupings > trimmed_infercnv.cell_groupings 
</pre>


CaSpER or HoneyBADGER:
In an R session with your corressponding R libraries and objects loaded, install and use phylogram function 'as.dendrogram()' to export your trees as newick formated strings:

<pre>
> BiocManager::install('phylogram')
> library(phylogram)
> casper_dendrogram <— as.dendrogram(tree) # tree : CaSpER tree object of class 'phylo'
> hc_dendrogram <— as.dendrogram(hc_tree) # hc_tree : HoneyBADGER tree object of class 'hclust'
> vc_dendrogram <— as.dendrogram(vc_tree) # vc_tree: another HoneyBADGER tree object of class 'hclust'
> write.dendrogram(insert_your_dendrogram_name,file=‘/path/to/uphyloplot2/Inputs’)
> q()
</pre>

After exiting R, navigate to the uphyloplot2 home directory and run the following script:
<pre>
./newick_input.py
</pre>

The newick_input.py script parses the dendrogram object produced in the pre-processing steps above. The script allows you to select a desired maximum length for the tree. You can see sample execution and output below:
<pre>
Please input the path to your newick file (no quotes, absolute or relative to current path)
Path_to_newick_file= dendrograms/casper_dendro
Unrooted tree detected!
PRUNING
###########################################################
###########################################################
#################   USER_INPUT    #########################
###########################################################

Your tree currently has 69 individual leaves
The longest branch in your tree is forked 16 times
How long do you want your tree? (input an integer)
> Length = 4


Name your output file:
> File = casper_out
###########################################################
###########################################################
###########################################################
###########################################################

This configuration will stack the leaves of your tree into 6 clusters
There are 2 clusters that are smaller than 5% of the total cell population, these will not be plotted.
Not Plotted Clusters:  [11, 13]
</pre>

It will output a '.cell_groupings' file in the ~/Uphyloplot2/Inputs directory. For instance, in the example above, a 'casper_out.cell_groupings' will be placed in the Uphyloplot2/Inputs directory. 

3. Navigate to the uphyloplot2 home directory directory and run the script with this simple command:
<pre>
python uphyloplot2.py
</pre>
Optional:
-c Defines the percentage cutoff used to remove smaller subclones. Default is 5 (Only subclones that comprise at least 5% of cells will be included for plotting.

Example usage:
<pre>
python uphyloplot2.py -c 10
</pre>

UPhyloplot2 will generate a "output.svg" vector graphics plot. Also, it will generate a new folder called "CNV_files", containing CNV files for each input, containing the subclone ID's identified by inferCNV in column 1, the percentage of cells for each subclone in column 2, and the letter marking the subclone in the output.svg file in column 3. 

UPhyloplot2 will not identify the characteristic CNV changes for each subclone. If desired, these have to be be inferred manually for each subclone IDs in the "HMM_CNV_predictions.HMMi6.rand_trees.hmm_mode-subclusters.Pnorm_0.5.pred_cnv_regions.dat file from the inferCNV output manually.

Please be aware that depending on the subclones present branches and subclone circles of the output.svg file might overlap. However, they can be rotated manually with Adobe Illustrator or any other svg editor. 

For some reason the output SVG files appear empty when previewing in MacOS or opening with a browser. Use Adobe Illustrator or such to open them, I am working on why this issue occurs.
