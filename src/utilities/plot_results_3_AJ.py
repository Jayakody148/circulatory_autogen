# --- Import libraries ---
import numpy as np
import os
from opencor_helper import SimulationHelper
import paperPlotSetup
paperPlotSetup.Setup_Plot(3)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- File paths ---
#file_path = "/hpc/ajay148/CA_user/haemorrhage_models/haemorrhage_v9/generated_models/haemorrhage_v9/haemorrhage_v9.cellml"
#output_file_path = "/people/ajay148/Desktop/plots_p"

file_path = "/hpc/ajay148/CA_user/cvs_hm_baro_models/cvs_hm_baro_v1/generated_models/cvs_hm_baro_v1/cvs_hm_baro_v1.cellml"
output_file_path = "/people/ajay148/Desktop/plots_p"

# --- Simulation settings ---
pre_time = 15.6
step_size = 0.01
period = 700.0  # total 10 minutes
solver_info = {'MaximumStep': 0.001, 'MaximumNumberOfSteps': 50000}

# --- Run simulation ---
sim_object = SimulationHelper(file_path, step_size, period, solver_info=solver_info, pre_time=pre_time)
sim_object.run()

# --- Get results ---
y = sim_object.get_results([
    'A_common_hepatic_C_leak_T/q_lost', 
    'A_common_hepatic_C_T/v', 
    'heart/q_lv', 
    'A_aortic_arch_C_1/u'
])
t = sim_object.tSim - pre_time

# --- Unit conversions ---
conversion_mL = 1E6       # to mL
conversion_mmHg = 1/133.322  # to mmHg

# --- Plotting ---
fig, axs = plt.subplots(2, 2, figsize=(12, 8), sharex=False, sharey=False)

# q_leak
axs[0,0].plot(t, y[0][0] * conversion_mL, color='red')
axs[0,0].set_ylabel('volume [mL]')
axs[0,0].set_xlim([0, 700])
axs[0,0].set_ylim(bottom=0)
axs[0,0].set_title('Volume lost from haemorrhage')

# q_liver
axs[0,1].plot(t, y[1][0] * conversion_mL, color='purple')
axs[0,1].set_ylabel('flow rate [mL/s]')
axs[0,1].set_xlim([0, 700])
axs[0,1].set_ylim(bottom=0)
axs[0,1].set_ylim(0, 30)
axs[0,1].set_title('liver')

# q_lv
axs[1,0].plot(t, y[2][0] * conversion_mL, color='purple')
axs[1,0].set_ylabel('volume [mL]')
axs[1,0].set_xlim([0, 700])
axs[1,0].set_ylim(0, 500)
axs[1,0].set_title('left ventricle')

# P_AR
axs[1,1].plot(t, y[3][0] * conversion_mmHg, color='purple')
axs[1,1].set_ylabel('pressure [mmHg]')
axs[1,1].set_xlim([0, 700])
axs[1,1].set_ylim(0, 200)
axs[1,1].set_title('aortic root')

# --- Add x-axis labels ---
for ax in axs.flat:
    ax.set_xlabel('Time [s]')

# --- Label subplots A, B, C, D ---
subplot_labels = ['A', 'B', 'C', 'D']
positions = [(-0.12, 1.05), (-0.12, 1.05), (-0.12, 1.05), (-0.12, 1.05)]  # moved outward

for ax, label, pos in zip(axs.flat, subplot_labels, positions):
    ax.text(pos[0], pos[1], label, transform=ax.transAxes,
            fontsize=18, fontweight='bold', va='bottom', ha='right')

# --- Add vertical dashed line at 120s (start of haemorrhage) ---
for ax in axs.flat:
    ax.axvline(x=120, color='gray', linestyle='--', linewidth=1)

# --- Add horizontal dashed line at 0s  ---
#for ax in axs.flat:
#    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1)

# --- Adjust layout and save ---
plt.subplots_adjust(wspace=0.5, hspace=0.5)
plt.savefig(os.path.join(output_file_path, 'cvs_hm_baro_1_plot_1.png'))
plt.savefig(os.path.join(output_file_path, 'cvs_hm_baro_1_plot_1.eps'))
