from OpenSMOG import SBM
import sys
from openmm import CustomCentroidBondForce
from openmm.unit import kilocalories_per_mole, nanometer
import numpy as np

#setting MD params
simul_prefix = "Output"
dt = 0.0005 #ps
collision_rate = 1.0 #ps-1
r_cutoff = 3.0 #nm 
T_in_K =122 #K
T = float(T_in_K)*0.008314 #reduced units RT

sbm_CA = SBM(name=simul_prefix, time_step=dt, collision_rate=collision_rate, r_cutoff=r_cutoff, temperature=T,pbc=True)

#platform="cuda"` or ="HIP" or ="opencl" or ="cpu"
sbm_CA.setup_openmm(platform='cpu',GPUindex='default')


sbm_CA.saveFolder("output_01")

sbm_CA_grofile = [x.strip() for x in sys.argv if x.endswith(".gro")][0]
sbm_CA_topfile = [x.strip() for x in sys.argv if x.endswith(".top")][0]
sbm_CA_xmlfile = [x.strip() for x in sys.argv if x.endswith(".xml")][0]

sbm_CA.loadSystem(Grofile=sbm_CA_grofile, Topfile=sbm_CA_topfile, Xmlfile=sbm_CA_xmlfile)

######_adding_CustomCentroidBondForce ###################
######_harmonic_restraint_##_tested_bu_Antony_John_######
group1_atoms = np.intp(list(range(1,120)))-1 #chain 1
group2_atoms = np.intp(list(range(121,240)))-1 #chain 2

k = 1.0 * kilocalories_per_mole / nanometer**2  
r0 = 3.0 * nanometer

restraint = CustomCentroidBondForce(2,"0.5*k*(distance(g1,g2)-r0)^2")
restraint.addPerBondParameter("k")
restraint.addPerBondParameter("r0")
g1 = restraint.addGroup(group1_atoms)
g2 = restraint.addGroup(group2_atoms)
restraint.addBond([g1,g2], [k,r0])
#restraint.setForceGroup(11)
sbm_CA.system.addForce(restraint)
#########################################################

sbm_CA.createSimulation()
trjformat = "xtc"
sbm_CA.createReporters(trajectory=True,trajectoryFormat=trjformat, energies=True, energy_components=True, interval=1000)

#report is for verbose
#for appending/extending simulations
#sbm_CA.simulation.loadCheckpoint("output_01/Output_checkpoint.chk")      
#sbm_CA.simulation.loadCheckpoint("endfile.chk")
#sbm_CA.simulation.loadState("endfile.state")
#mdrun

sbm_CA.run(nsteps=1000000000, report=True, interval=10000)
sbm_CA.simulation.saveState("endfile.state")
sbm_CA.simulation.saveCheckpoint("endfile.chk")

