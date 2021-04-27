# uphyloplot2 version 2.3
If you encounter any issues or to request features please open an issue on this github page, and state the version you are running.

Please cite  uphyloplot2: Visualizing Phylogenetic Trees from Single-Cell RNA-seq Data, Stefan Kurtenbach, Daniel A. Rodriguez, Michael A. Durante, J. William Harbour, bioRxiv 2020.05.25.115550; doi: https://doi.org/10.1101/2020.05.25.115550 

Draw phylogenetic trees of tumor evolution, as seen in our Nature communications paper (Nature Communications volume 11, Article number: 496 (2020). 


<img src="https://github.com/harbourlab/uphyloplot2/blob/master/Screen%20Shot%202019-06-26%20at%2010.43.48%20AM.png" width="300">


This python tool takes input from CaSpER, HoneyBADGER, and InferCNV. Please follow the guide below to visualize your tree using inputs from all three programs. In an R session with your corressponding program loaded:

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

The newick_input.py script parses the dendrogram object produced in the pre-processing steps above. It will output a '.cell_groupings' file
in the ~/uphyloplot2/Inputs directory. Simply follow the command line prompts to load and analyze your data.

".cell_groupings" files from the inferCNV output, and generates the evolutionary plots. Important! Make sure to remove the reference or control cells in the ".cell_groupings" file, which are usually at the end. inferCNV needs to be run with HMM, which will produce the "HMM_CNV_predictions.HMMi6.rand_trees.hmm_mode-subclusters.Pnorm_0.5.cell_groupings” files used for plotting. cluster_by_groups should be set to FALSE.

Place python script in a folder also containing a "Input" folder with all the ".cell_groupings" files. Files need to end with ".cell_groupings", but can have any name before. You can download example data from this github page to test the program. 

Quick start, run the script with this simple command. 
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
