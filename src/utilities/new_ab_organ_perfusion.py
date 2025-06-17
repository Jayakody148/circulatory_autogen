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
output_file_path = "/people/ajay148/Desktop/plots_p"
pre_time = 15.6
period = 600.0

sim_object = SimulationHelper(file_path, 0.01, period, solver_info={'MaximumStep':0.001, 'MaximumNumberOfSteps':50000}, pre_time=pre_time)
sim_object.run()

# IF you want to change parameters and run again, do it here. 


y = sim_object.get_results(['A_left_gastric_C_T/v', 'A_common_hepatic_C_T/v', 'A_renal_L_T/v', 'A_splenic_C_T/v'])
t = sim_object.tSim - pre_time

conversion_mL = 1E6 # convert to mL
#conversion_mmHg = 1/133.322 # convert to mmHg

data1 = y[0][0] * conversion_mL
mean1 = np.mean(data1)
plt.figure()
plt.plot(t, data1, color='blue')
plt.axhline(y=mean1, color='orange', linestyle='--', label='Mean flow')
plt.xlim([0, period])
plt.ylim(bottom=0)
plt.xlabel('Time [s]')
plt.ylabel('Flow Rate [mL/s]')
plt.title('Stomach')
plt.grid(False)
plt.legend(loc='lower right')
plt.savefig(os.path.join(output_file_path, 'Stomach_v1.png'))
plt.close()

# Plot 2: A_common_hepatic_C_T/v
data2 = y[1][0] * conversion_mL
mean2 = np.mean(data2)
plt.figure()
plt.plot(t, data2, color='green')
plt.axhline(y=mean2, color='orange', linestyle='--', label='Mean flow')
plt.xlim([0, period])
plt.ylim(bottom=0)
plt.xlabel('Time [s]')
plt.ylabel('Flow Rate [mL/s]')
plt.title('Liver')
plt.grid(False)
plt.legend(loc='lower right')
plt.savefig(os.path.join(output_file_path, 'Liver_v1.png'))
plt.close()

# Plot 3: A_renal_L_T/v
data3 = y[2][0] * conversion_mL
mean3 = np.mean(data2)
plt.figure()
plt.plot(t, data3, color='purple')
plt.axhline(y=mean3, color='orange', linestyle='--', label='Mean flow')
plt.xlim([0, period])
plt.ylim(bottom=0)  # Adjust this based on expected data range
plt.xlabel('Time [s]')
plt.ylabel('Flow Rate [mL/s]')
plt.title('Kidney')
plt.grid(False)
plt.legend(loc='lower right')
plt.savefig(os.path.join(output_file_path, 'kidney_v1.png'))
plt.close()

# Plot 4: A_splenic_C_T/v
data4 = y[3][0] * conversion_mL
mean4 = np.mean(data4)
plt.figure()
plt.plot(t, data4, color='red')
plt.axhline(y=mean4, color='orange', linestyle='--', label='Mean flow')
plt.xlim([0, period])
plt.ylim(bottom=0)  # Adjust this based on expected data range
plt.xlabel('Time [s]')
plt.ylabel('Flow Rate [mL/s]')
plt.title('Spleen')
plt.grid(False)
plt.legend(loc='lower right')
plt.savefig(os.path.join(output_file_path, 'spleen_v1.png'))
plt.close()
