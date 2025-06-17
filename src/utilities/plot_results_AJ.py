import numpy as np
import os
from opencor_helper import SimulationHelper
import paperPlotSetup
paperPlotSetup.Setup_Plot(3)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- File paths ---
baseline_path = "/hpc/ajay148/CA_user/cvs_models/simple_ADAN_v18/generated_models/simple_ADAN_v18_simple_ADAN_v18_obs_data/simple_ADAN_v18.cellml"
haemorrhage_path = "/hpc/ajay148/CA_user/haemorrhage_models/haemorrhage_v6/generated_models/haemorrhage_v6/haemorrhage_v6.cellml"
output_file_path = "/hpc/ajay148/CA_user/haemorrhage_models/haemorrhage_v6/additional_plots"

# --- Simulation settings ---
pre_time = 15.6
period_baseline = 120.0  # 2 minutes
period_haemorrhage = 480.0  # 8 minutes
step_size = 0.01
solver_info = {'MaximumStep': 0.001, 'MaximumNumberOfSteps': 50000}

# --- Run baseline model ---
sim_base = SimulationHelper(baseline_path, step_size, period_baseline, solver_info=solver_info, pre_time=pre_time)
sim_base.run()
y_base = sim_base.get_results(['A_common_hepatic_C_T/q_T', 'heart/q_lv', 'A_aortic_arch_C_1/u'])
t_base = sim_base.tSim - pre_time

# --- Run haemorrhage model ---
sim_haem = SimulationHelper(haemorrhage_path, step_size, period_haemorrhage, solver_info=solver_info, pre_time=pre_time)
sim_haem.run()
y_haem = sim_haem.get_results(['A_common_hepatic_C_leak_T/q_lost', 'A_common_hepatic_C_T/q_T', 'heart/q_lv', 'A_aortic_arch_C_1/u'])
t_haem = sim_haem.tSim - pre_time

# --- Adjust haemorrhage time to continue from baseline ---
t_haem = t_haem + t_base[-1] + (t_base[1] - t_base[0])  # Small step to avoid overlap

# --- Unit conversions ---
conversion_mL = 1E6
conversion_mmHg = 1 / 133.322

# --- Plotting ---
fig, axs = plt.subplots(2, 2, figsize=(12, 8), sharex=False, sharey=False)

# q leak (only haemorrhage)
axs[0, 0].plot(t_haem, y_haem[0][0] * conversion_mL, color='red', label='q leak (haem)')
axs[0, 0].set_ylabel('q leak [mL]')
axs[0, 0].legend()
axs[0, 0].set_xlim([0, t_haem[-1]])

# q liver
axs[0, 1].plot(t_base, y_base[0][0] * conversion_mL, color='blue', label='baseline')
axs[0, 1].plot(t_haem, y_haem[1][0] * conversion_mL, color='red', label='haemorrhage')
axs[0, 1].set_ylabel('q liver [mL]')
axs[0, 1].legend()
axs[0, 1].set_xlim([0, t_haem[-1]])

# q lv
axs[1, 0].plot(t_base, y_base[1][0] * conversion_mL, color='blue', label='baseline')
axs[1, 0].plot(t_haem, y_haem[2][0] * conversion_mL, color='red', label='haemorrhage')
axs[1, 0].set_ylabel('q lv [mL]')
axs[1, 0].legend()
axs[1, 0].set_xlim([0, t_haem[-1]])

# P AR
axs[1, 1].plot(t_base, y_base[2][0] * conversion_mmHg, color='blue', label='baseline')
axs[1, 1].plot(t_haem, y_haem[3][0] * conversion_mmHg, color='red', label='haemorrhage')
axs[1, 1].set_ylabel('P AR [mmHg]')
axs[1, 1].legend()
axs[1, 1].set_xlim([0, t_haem[-1]])

# --- Label all x-axes ---
for ax in axs.flat:
    ax.set_xlabel('Time [s]')

# --- Add dashed line at 120s (onset of haemorrhage) ---
for ax in axs.flat:
    ax.axvline(x=120, color='gray', linestyle='--', linewidth=1)

# --- Adjust layout and save ---
plt.subplots_adjust(wspace=0.5, hspace=0.5)
plt.savefig(os.path.join(output_file_path, 'combined_transition_plot_3.png'))
plt.savefig(os.path.join(output_file_path, 'combined_transition_plot_3.eps'))
