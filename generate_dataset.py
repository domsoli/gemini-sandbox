
import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Define constants
n_rows = 100000
coverages = ['Coverage_A', 'Coverage_B', 'Coverage_C']

# Generate Policy IDs
policy_ids = [f'POL_{i+1:05d}' for i in range(n_rows)]

# Generate Coverages
coverage_data = np.random.choice(coverages, n_rows)

# Generate Number of Claims (using a Poisson distribution)
claims_number = np.random.poisson(lam=1.5, size=n_rows)

# Generate Claim Status (95% closed, 5% open)
claim_status = np.random.choice([False, True], n_rows, p=[0.95, 0.05])

# Define cost distribution parameters for each coverage
coverage_cost_params = {
    'Coverage_A': {'shape': 1.5, 'scale': 800.0},
    'Coverage_B': {'shape': 2.5, 'scale': 1200.0},
    'Coverage_C': {'shape': 3.0, 'scale': 1500.0}
}

# Generate Claim Cost based on coverage
base_cost = np.zeros(n_rows)
for cov, params in coverage_cost_params.items():
    indices = np.where(coverage_data == cov)[0]
    base_cost[indices] = np.random.gamma(params['shape'], params['scale'], len(indices))


# Add noise
noise = np.random.normal(0, 250, n_rows)
noisy_cost = base_cost + noise
noisy_cost[noisy_cost < 0] = 0  # Ensure cost is not negative

# Introduce peaks for open claims
# Select 5% of open claims to have a peak
open_claims_indices = np.where(claim_status == True)[0]
peak_indices = np.random.choice(open_claims_indices, size=int(len(open_claims_indices) * 0.05), replace=False)

# Apply a stronger multiplier for the peaks
peak_multiplier = np.random.uniform(10, 25, len(peak_indices))
noisy_cost[peak_indices] *= peak_multiplier

# Create DataFrame
df = pd.DataFrame({
    'policy_id': policy_ids,
    'coverage': coverage_data,
    'claims_number': claims_number,
    'claim_status_open': claim_status,
    'claims_cost': noisy_cost
})

# Save to Parquet
df.to_parquet('insurance_dataset.parquet')

print("Synthetic dataset generated and saved to 'insurance_dataset.parquet'")
