export SuBMITdir=../../../../SuBMIT/
python ${SuBMITdir}/submit.py --calpha_sbm --opensmog\
      	--aa_pdb pdbfiles/6Y2E_CTD.pdb pdbfiles/sp_prot{1..6}.pdb \
       	--cmap contfiles/6Y2E_CTD.cont contfiles/stap_prot{1..6}.cont \
	--cmap_i contfiles/inter.cont --nmol 1 200 200 200 200 200 200 
rm contfiles/*protcont
rm pdbfiles/*renum* 


