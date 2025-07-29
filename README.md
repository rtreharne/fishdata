# Fish Data Generator

This project provides Python scripts for generating synthetic datasets with flexible statistical properties. It is designed for teaching scenarios where you need to create realistic datasets for statistical analysis (e.g., formative and summative assessments).

---

## **Features**

1. **Generate datasets for any dependent variable**  
   - Examples: fish length, weight, or any continuous measurement.

2. **Create multiple groups**  
   - Example: `Control` vs `Polluted`.
   - Customizable number of groups.

3. **Specify data distribution**  
   - Choose between **normal** (Gaussian) or **non-normal** distributions.
   - Non-normal data can be skewed or generated from other probability distributions.

4. **Control statistical significance**  
   - Decide whether group differences are statistically significant.
   - Define mean differences and variance levels to achieve desired effects (e.g., 5% difference but not statistically significant).

5. **Set sample sizes**  
   - Approximate or exact number of data points per group can be specified.

6. **Unique identifiers for each record**  
   - Each row in the dataset includes a unique ID (e.g., `ID001`, `ID002`, etc.).

---

## **Example Use Cases**
- Creating formative datasets (e.g., dogfish morphometric data).
- Summative datasets (e.g., trout length) where groups are **not significantly different**.
- Demonstrating statistical tests such as t-tests, ANOVAs, or non-parametric equivalents.

---

## **Quick Start**

### **1. Clone the Repository**
```bash
git clone https://github.com/<your-username>/fish-data-generator.git
cd fish-data-generator
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```
Dependencies include:
- `numpy`
- `pandas`
- `scipy` (for significance testing)
- `faker` (optional, for generating unique IDs)

---

## **3. Generate a Dataset**
Example script usage:
```bash
python generate_dataset.py --variable "Length (mm)" \
                           --groups Control Polluted \
                           --n_per_group 50 \
                           --distribution normal \
                           --significant false
```

This will:
- Generate 50 samples per group.
- Use a normal distribution.
- Ensure the mean difference between groups is **not statistically significant**.

---

## **4. Output**
- A CSV file, e.g., `dataset_length.csv`, containing columns:
  - `ID` (unique identifier)
  - `Group`
  - `Length (mm)`
- A grouped boxplot saved as `boxplot.png` (if `--plot` is enabled).

---

## **Project Structure**
```
fish-data-generator/
│
├── generate_dataset.py      # Main script for dataset generation
├── utils.py                 # Helper functions for distributions & IDs
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── examples/                # Example datasets and usage
```

---

## **Example Command with Boxplot**
The following command:
```bash
python generate_dataset.py --variable "Length (mm)" --groups Control A B C --mean 120 --sd 10 --max_change -10 --plot --significant false
```
Generates:
- **`dataset.csv`** – The dataset with group data.
- **`boxplot.png`** – A grouped boxplot visualizing the dataset.

---

## **Future Enhancements**
- Support for multiple dependent variables in one dataset.
- Integration with R for generating example statistical reports.
- Customizable effect sizes and power analysis for planning sample sizes.

---

## **License**
MIT License – see [LICENSE](LICENSE) file for details.
