# PakistanTIMES 2025

A comprehensive energy system optimization model for analyzing Pakistan's energy transition pathways from 2014 to 2050.

## 📋 Overview

**PakistanTIMES 2025** is a TIMES (The Integrated MARKAL-EFOM System) based energy system optimization model that evaluates least-cost strategies for meeting Pakistan's electricity demand while achieving renewable energy targets and reducing greenhouse gas emissions.

### Key Features

- **16 Scenarios**: Combines renewable energy targets (30-70%) with demand growth projections
- **7 Technologies**: Solar, Wind, Hydro, Biomass, Coal, Gas, Nuclear
- **Optimization Framework**: Linear programming for least-cost power generation planning
- **Time Horizon**: 2014-2050 (36 years)
- **Geographic Scope**: Pakistan (3-zone representation)

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running the Model

1. **Basic Scenario Run**:
   ```bash
   python run_comprehensive_scenarios.py
   ```

2. **Generate Results Package**:
   ```bash
   python create_master_workbook.py
   python create_csv_files.py
   ```

3. **Create Interactive Dashboard**:
   ```bash
   python create_html_dashboard.py
   ```

## 📁 Project Structure

```
GIT.PK.TIMES.2025/
├── src/                    # Core model source code
│   ├── models/            # TIMES optimization model
│   ├── data/              # Data management modules
│   ├── scenarios/         # Scenario management
│   ├── results/           # Results analysis
│   └── utils/             # Utility functions
├── config/                # Configuration files
├── data/                  # Input data files
│   └── input/            # Excel input templates
├── *.py                   # Main execution scripts
└── *.md                   # Documentation
```

## 📊 Model Components

### Core Model (`src/models/pakistan_times_model.py`)
- TIMES optimization framework
- Least-cost generation planning
- Technology constraints and learning curves
- System reliability constraints

### Scenario Manager (`src/scenarios/scenario_manager.py`)
- Renewable energy targets (REN30, REN50, REN60, REN70)
- Demand growth projections (LEG, BAU, MEG, HEG)
- 16 scenario combinations

### Data Manager (`src/data/data_manager.py`)
- Technology cost data
- Demand forecasts
- Resource availability
- External costs

## 📈 Key Outputs

The model generates:
- **Renewable Share**: Percentage of renewable energy in generation mix
- **Annual Emissions**: MtCO₂ per year
- **Cumulative Investment**: Total investment required (Billion USD)
- **Installed Capacity**: GW by technology and year
- **Generation Mix**: TWh by technology and year

## 📚 Documentation

- **[MODEL_SUMMARY.md](MODEL_SUMMARY.md)**: Comprehensive model overview
- **[Executive_Summary.md](Executive_Summary.md)**: Key findings and policy recommendations
- **[Data_Dictionary.md](Data_Dictionary.md)**: Data structure and definitions
- **[Usage_Guidelines.md](Usage_Guidelines.md)**: Detailed usage instructions
- **[PakistanTIMES_2025_Equations_Word.md](PakistanTIMES_2025_Equations_Word.md)**: Model equations documentation

## 🎯 Scenario Results Summary

| Scenario | Renewable Share | Emissions Reduction | Total Investment |
|----------|----------------|---------------------|------------------|
| REN30 | 30% | 0-22% | $7.5-9.8B |
| REN50 | 50% | 28.6-45% | $12.0-15.4B |
| REN70 | 70% | 57.1-65% | $16.1-20.3B |

## 🔧 Configuration

Model parameters can be adjusted in `config/config.py`:
- Study period and base year
- Economic parameters (discount rate, carbon price)
- Technology costs and learning curves
- System reliability constraints

## 📝 Input Data

Input data templates are located in `data/input/`:
- `technology_costs_corrected_realistic.xlsx`: Technology cost assumptions
- `demand_forecast.xlsx`: Electricity demand projections
- `resources.xlsx`: Resource availability
- `emission_factors_corrected.xlsx`: Emission factors
- `external_costs.xlsx`: External cost parameters

## 🧪 Validation

The model has been validated against:
- International literature (LEAP, IEA references)
- Peer-reviewed energy system models
- Realistic demand projections and technology assumptions

## 📄 License

This project is developed for research and policy analysis purposes.

## 👥 Contributors

PakistanTIMES Model Development Team

## 📞 Contact

For questions or collaboration opportunities, please open an issue or contact the development team.

---

**Status**: ✅ Fully validated and publication-ready  
**Last Updated**: August 2025
