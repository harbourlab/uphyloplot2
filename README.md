# UPhyloplot2 version 2.0
Draw phylogenetic trees of tumor evolution, as seen in our Nature communications paper (Nature Communications volume 11, Article number: 496 (2020). 

![alt text](https://raw.githubusercontent.com/StefanKurtenbach/UPhyloplot2/master/Screen%20Shot%202019-06-26%20at%2010.43.48%20AM.png)

This python tool takes the ".cell_groupings" files from the inferCNV output, and generates the evolutionary plots. inferCNV needs to be run with HMM, which will produce a "HMM_CNV_predictions.HMMi6.rand_trees.hmm_mode-subclusters.Pnorm_0.5.cell_groupings” files used.

Place python script in a folder also containing a "Input" folder with all the ".cell_groupings" files. Files need to end with ".cell_groupings", but can have any name before. You can download example data from this github page to test the program. 

Quick start, run the script with this simple command. 
<pre>
python UPhyloPlot2.py
</pre>
Optional:
-c Defines the percentage cutoff used to remove smaller subclones. Default is 5 (Only subclones that comprise at least 5% of cells will be included for plotting.

Example usage:
<pre>
python UPhyloPlot2.py -c 10
</pre>


UPhyloPlot2 will generate a "output.svg" vector graphics plot. Also, it will generate a new folder called "CNV_files", containing CNV files for each input, containing the subclone ID's identified by inferCNV in column 1, the percentage of cells for each subclone in column 2, and the letter marking the subclone in the output.svg file in column 3. 

UPhyloplot2 will not identify the characteristic CNV changes for each subclone. If desired, these have to be be inferred manually for each subclone IDs in the "HMM_CNV_predictions.HMMi6.rand_trees.hmm_mode-subclusters.Pnorm_0.5.pred_cnv_regions.dat file from the inferCNV output manually.

Please be aware that depending on the subclones present branches and subclone circles of the output.svg file might overlap. However, they can be rotated manually with Adobe Illustrator or any other svg editor. 
