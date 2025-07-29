#!/usr/bin/env python3
"""
generate_dataset.py

This script generates synthetic datasets with customizable statistical properties.

FEATURES:
- Specify the dependent variable name (e.g., "Length").
- Define groups (e.g., "Control", "Treatment").
- Set sample sizes per group.
- Choose between normal or non-normal distributions.
- Control whether group differences are statistically significant.
- Set baseline mean and standard deviation.
- Randomly increase means of non-control groups up to a maximum percentage change.
- Limit the precision (decimal places) of the data.
- Optionally visualize the dataset as a grouped boxplot and save it as a .png.
- Output to CSV with unique identifiers.

USAGE EXAMPLES:
---------------
1. Generate a dataset with up to +10% random increases for groups:
    python generate_dataset.py --variable "Length (mm)" --groups Control Treatment --max_change 10

2. Generate a dataset with 3 groups with up to +20% random increases:
    python generate_dataset.py --variable "Weight (g)" --groups Control Group1 Group2 --max_change 20

3. Generate data with a boxplot:
    python generate_dataset.py --variable "Length (mm)" --groups Control Polluted --max_change 8 --plot
"""

import argparse
import numpy as np
import pandas as pd
import uuid
import matplotlib.pyplot as plt

def generate_group_data(n, mean, sd, distribution='normal'):
    """
    Generate synthetic values for a group.
    """
    if distribution == 'normal':
        return np.random.normal(loc=mean, scale=sd, size=n)
    elif distribution == 'exponential':
        return np.random.exponential(scale=mean, size=n)
    else:
        raise ValueError(f"Unsupported distribution: {distribution}")

def create_dataset(variable, groups, n_per_group, distribution, significant, precision, mean, sd, max_change):
    """
    Generate a synthetic dataset with the specified parameters.
    Each non-control group mean is increased randomly up to max_change%.
    """
    data = []
    base_mean = mean
    base_sd = sd

    for i, group in enumerate(groups):
        if i == 0:
            group_mean = base_mean
        else:
            # Random increase between [0, max_change%]
            change_percent = np.random.uniform(0, max_change) / 100.0
            group_mean = base_mean * (1 + change_percent)

            if not significant:
                # Add small random noise to avoid clear significance
                group_mean += np.random.uniform(-base_sd * 0.1, base_sd * 0.1)

        group_data = generate_group_data(n_per_group, group_mean, base_sd, distribution)
        for value in group_data:
            data.append({
                "ID": str(uuid.uuid4())[:8],
                "Group": group,
                variable: round(value, precision)
            })

    return pd.DataFrame(data)

def save_boxplot(df, variable, output_file):
    """
    Save a grouped boxplot for the dataset to a .png file.
    """
    plt.figure(figsize=(8, 6))
    df.boxplot(column=variable, by='Group', grid=False)
    plt.title(f'{variable} by Group')
    plt.suptitle('')
    plt.ylabel(variable)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Boxplot saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Generate synthetic datasets with statistical properties.')
    
    parser.add_argument('--variable', type=str, default='Measurement',
                        help='Name of the dependent variable (default: Measurement)')
    parser.add_argument('--groups', nargs='+', default=['Control', 'Treatment'],
                        help='List of groups (default: Control Treatment)')
    parser.add_argument('--n_per_group', type=int, default=50,
                        help='Number of samples per group (default: 50)')
    parser.add_argument('--distribution', type=str, choices=['normal', 'exponential'], default='normal',
                        help='Distribution type (default: normal)')
    parser.add_argument('--significant', type=lambda x: (str(x).lower() == 'true'), default=True,
                        help='Whether to create significant differences (default: True)')
    parser.add_argument('--mean', type=float, default=100.0,
                        help='Baseline mean for Control group (default: 100.0)')
    parser.add_argument('--sd', type=float, default=15.0,
                        help='Standard deviation (default: 15.0)')
    parser.add_argument('--max_change', type=float, default=5.0,
                        help='Maximum percentage increase in group means (default: 5.0)')
    parser.add_argument('--precision', type=int, default=2,
                        help='Number of decimal places to round data to (default: 2)')
    parser.add_argument('--output', type=str, default='dataset.csv',
                        help='Output CSV filename (default: dataset.csv)')
    parser.add_argument('--plot', action='store_true',
                        help='Generate a grouped boxplot and save as PNG')
    parser.add_argument('--plot_file', type=str, default='boxplot.png',
                        help='Output filename for the boxplot PNG (default: boxplot.png)')
    
    args = parser.parse_args()

    df = create_dataset(
        variable=args.variable,
        groups=args.groups,
        n_per_group=args.n_per_group,
        distribution=args.distribution,
        significant=args.significant,
        precision=args.precision,
        mean=args.mean,
        sd=args.sd,
        max_change=args.max_change
    )

    df.to_csv(args.output, index=False)
    print(f"Dataset saved to {args.output}")

    if args.plot:
        save_boxplot(df, args.variable, args.plot_file)

if __name__ == '__main__':
    main()
