# import opencor as oc
import numpy as np
import os
from opencor_helper import SimulationHelper
import csv
import paperPlotSetup
paperPlotSetup.Setup_Plot(3)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# TODO get all of the info from the user_inputs.yaml file

file_path = "/hpc/ajay148/CA_user/cvs_models/simple_ADAN_v18/generated_models/simple_ADAN_v18_simple_ADAN_v18_obs_data/simple_ADAN_v18.cellml"
output_file_path = "/hpc/ajay148/CA_user/cvs_models/simple_ADAN_v18/additional_plots"
pre_time = 15.6
period = 60.0

sim_object = SimulationHelper(file_path, 0.01, period, solver_info={'MaximumStep':0.001, 'MaximumNumberOfSteps':50000}, pre_time=pre_time)
sim_object.run()

# IF you want to change parameters and run again, do it here. 


y = sim_object.get_results(['A_left_gastric_C_T/q_T', 'A_common_hepatic_C_T/q_T', 'heart/q_lv', 'A_aortic_arch_C_1/u'])
t = sim_object.tSim - pre_time

conversion_mL = 1E6 # convert to mL
conversion_mmHg = 1/133.322 # convert to mmHg

fig, axs = plt.subplots(2, 2, sharex=False, sharey=False)
axs[0,0].plot(t, y[0][0]*conversion_mL)#, label='A_left_gastric_C_T/q_T')
axs[0,1].plot(t, y[1][0]*conversion_mL)#, label='A_common_hepatic_C_T/q_T')
axs[1,0].plot(t, y[2][0]*conversion_mL)#, label='heart/q_lv')
axs[1,1].plot(t, y[3][0]*conversion_mmHg)#, label='A_aortic_arch_C_1/u')

axs[0,0].set_xlim([0, period])
axs[0,0].set_ylim([0, 5])
axs[0,0].set_xlabel('Time [s]')
axs[0,0].set_ylabel('q stomach [mL]')
axs[0,1].set_xlim([0, period])
axs[0,1].set_ylim([0, 15])
axs[0,1].set_xlabel('Time [s]')
axs[0,1].set_ylabel('q liver [mL]')
axs[1,0].set_xlim([0, period])
axs[1,0].set_ylim([0, 300])
axs[1,0].set_xlabel('Time [s]')
axs[1,0].set_ylabel('q lv [mL]')
axs[1,1].set_xlim([0, period])
axs[1,1].set_ylim([0, 150])
axs[1,1].set_xlabel('Time [s]')
axs[1,1].set_ylabel('P AR [mmHg]')

# adjust spacing between subplots
plt.subplots_adjust(wspace=0.5, hspace=0.5)

plt.savefig(os.path.join(output_file_path, 'model_outputs_u.png'))
plt.savefig(os.path.join(output_file_path, 'model_outputs_u.eps'))
