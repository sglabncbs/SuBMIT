#FOR GROMACS 4.5.4
cp ../SuBMIT_Output/gromacs.* .
editconf -f gromacs.gro -o gromacs.gro -c -box 50 50 50
echo -e "a 1-120\na 121-240\nq" | make_ndx -f gromacs.gro -o index.ndx
grompp -f ../../run_table_dswap.mdp  -c gromacs.gro -p gromacs.top -o Output -po Output  -n index.ndx
mdrun -deffnm Output -nt 1 -v -pd -table ../SuBMIT_Output/Tables/table_lj1012.xvg -tablep ../SuBMIT_Output/Tables/table_lj1012.xvg
rm \#*
