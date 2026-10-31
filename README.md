# 🍎 AgriLoss Insight
### Apple Supply Chain Loss Pattern Analyzer | Data Mining Project

**AgriLoss Insight** is a data-driven analytical platform designed to identify, analyze, and understand apple supply chain losses in Himachal Pradesh, India.

From orchards to transportation and finally to mandis, apples pass through several stages where losses can occur due to environmental conditions, road quality, transportation distance, storage methods, and handling practices.

This project applies Data Mining techniques to discover hidden patterns, classify shipment risk levels, and identify factors that may contribute to apple losses.

---

## 🌟 Project Overview

The main objective of AgriLoss Insight is to transform shipment data into meaningful insights that can help understand where and why apple losses occur in the supply chain.

The system analyzes simulated shipment records and provides an interactive dashboard to explore:

- Shipment loss patterns and trends.
- Low, Medium, and High-risk shipment categories.
- Important factors associated with apple losses.
- Relationships between transportation conditions and loss levels.
- Association rules between different shipment conditions.

## 🎯 Key Objectives

- Analyze apple supply chain loss patterns.
- Identify major factors associated with shipment losses.
- Group shipments based on their risk profiles.
- Predict shipment loss categories using Machine Learning.
- Discover hidden relationships using association rule mining.
- Present analytical results through an interactive dashboard.

---

## 🧠 Data Mining Techniques Used

| Algorithm | Purpose | Application |
|---|---|---|
| K-Means Clustering | Unsupervised Learning | Groups shipments into different risk profiles. |
| Decision Tree | Supervised Learning | Classifies shipments into Low, Medium, and High loss categories. |
| Apriori Algorithm | Association Rule Mining | Discovers relationships between shipment conditions and loss categories. |

### 1. K-Means Clustering
- Groups similar apple shipments based on selected attributes.
- Identifies different shipment risk profiles.
- Helps understand patterns among low, medium, and high-risk shipments.

### 2. Decision Tree Classification
- Predicts the loss category of a shipment.
- Identifies important factors influencing the prediction.
- Provides an understandable decision-based classification model.

### 3. Apriori Association Rule Mining
- Identifies frequently occurring combinations of shipment conditions.
- Discovers associations between transportation factors and loss categories.
- Generates rules using Support, Confidence, and Lift.

**Example of an association rule:**

`Ambient Storage + Poor Road + Long Haul → High Loss`

*This is an illustrative example of the type of relationship the algorithm can discover.*

---

## 🚀 Dashboard Features

AgriLoss Insight provides an interactive Streamlit dashboard with the following modules:

| Module | Description |
|---|---|
| Overview | Displays overall shipment statistics and key performance indicators. |
| K-Means Analysis | Visualizes shipment clusters and risk profiles. |
| Decision Tree | Shows loss classification results and important factors. |
| Apriori Analysis | Displays frequent itemsets and association rules. |
| Insights | Presents important findings from the analysis. |

### Key Highlights
- Interactive data visualization.
- Shipment risk analysis.
- Machine Learning-based classification.
- Association rule discovery.
- CSV dataset upload functionality.
- Automatic synthetic dataset generation.
- Easy-to-use web dashboard.

---

## 🛠️ Technologies & Tools

| Technology | Usage |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive dashboard development |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Scikit-learn | K-Means and Decision Tree |
| Mlxtend | Apriori and association rules |
| Matplotlib / Seaborn | Data visualization |

---

## 📂 Project Structure

```text
AgriLoss-Insight/
│
├── app.py                  # Main Streamlit dashboard
├── mining.py               # Data mining algorithms
├── generate_data.py        # Synthetic dataset generator
├── apple_supply_chain.csv  # Shipment dataset
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
│
└── .venv/                  # Virtual environment (local)
```

---

## ⚙️ Installation & Setup

Follow these steps to run AgriLoss Insight on your local system.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Aditya-Rangta/AgriLoss-Insight.git
```

### Step 2: Open the Project Folder

```bash
cd AgriLoss-Insight
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Generate Dataset (Optional)

```bash
python generate_data.py
```

The application can also generate the dataset automatically if required.

### Step 5: Run the Application

```bash
streamlit run app.py
```

### Step 6: Open the Dashboard

After running the command, Streamlit will provide a local URL, generally:

```text
http://localhost:8501
```

Open this address in your web browser to explore the dashboard.

---

## 📊 Dataset Information

AgriLoss Insight uses a **synthetic dataset containing approximately 1,500 apple shipment records**.

The dataset simulates different supply chain conditions and possible loss-related factors.

### Sample Attributes

- Storage conditions
- Road quality
- Transportation distance
- Shipment duration
- Environmental conditions
- Shipment-related information
- Apple loss percentage
- Loss category

### Dataset Disclaimer

The dataset used in this project is synthetically generated for educational and analytical purposes.

Actual shipment-level apple supply chain data is not publicly available for this project. Therefore, simulated records are used to demonstrate Data Mining algorithms and analytical techniques.

**The results should not be interpreted as verified measurements of actual apple losses in Himachal Pradesh.**

---

## 📁 Using Your Own Dataset

Users can explore the application with their own shipment data.

1. Prepare a CSV file containing the required dataset columns.
2. Open the AgriLoss Insight dashboard.
3. Upload the CSV file using the sidebar.
4. Explore the available Data Mining modules.

The uploaded dataset should follow the column structure expected by the application.

---

## 🌱 Real-World Applications

AgriLoss Insight demonstrates how Data Mining can be applied to agricultural supply chain analysis.

Potential applications include:

- Understanding transportation-related loss patterns.
- Identifying shipment conditions associated with higher losses.
- Supporting better storage and transportation planning.
- Helping researchers study agricultural supply chains.
- Developing data-driven approaches to reduce post-harvest losses.

---

## 🔮 Future Scope

The project can be extended with:

- Real-time shipment tracking.
- Weather data integration.
- Actual orchard-to-mandi shipment records.
- Advanced prediction models.
- Geographic visualization of shipment routes.
- A recommendation system for reducing potential losses.
- Mobile-friendly dashboard support.

---

## 👨‍💻 Developer

**Aditya Rangta**

BCA Student | Data Mining & Data Analytics Enthusiast

- GitHub: [Aditya-Rangta](https://github.com/Aditya-Rangta)
- Project Repository: [AgriLoss Insight](https://github.com/Aditya-Rangta/AgriLoss-Insight)

---

## 📜 Academic Information

| Detail | Information |
|---|---|
| Project Name | AgriLoss Insight |
| Project Type | BCA Data Mining Project |
| Domain | Agriculture & Supply Chain Analytics |
| Programming Language | Python |
| Interface | Streamlit Dashboard |
| Dataset | Synthetic Apple Shipment Dataset |
| Core Techniques | K-Means, Decision Tree, Apriori |

---

**AgriLoss Insight – Turning Apple Supply Chain Data into Meaningful Insights.** 🍎

*Developed as an educational Data Mining project.*
