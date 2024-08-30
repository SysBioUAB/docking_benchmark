# Script to carry out the analysis shown in Figure 3. RMSD, potential_energy-rog and free energy landscape plots.

MD_SCRIPT_PATH="../docking_analysis"
MD_PATH="../../data/output_files/MD"

python3 $MD_SCRIPT_PATH/MD_RMSD_plot.py -md $MD_PATH/1e50/ -n 1e50 -r 1

bash $MD_SCRIPT_PATH/MD_analysis.sh

python3 $MD_SCRIPT_PATH/energy_rog_plots.py -md $MD_PATH/1e50/ -n 1e50 -emin -13600 -emax -10000 -t 500 -rmin 1.6 -rmax 7

python $MD_SCRIPT_PATH/xpm2txt.py -f $MD_PATH/1e50/FES.xpm -o $MD_PATH/1e50/free-energy-landscape.dat

python $MD_SCRIPT_PATH/free_energy_landscape_plot.py -md $MD_PATH/1e50/ -n 1e50
