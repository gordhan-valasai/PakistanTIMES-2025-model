"""
Configuration file for PakistanTIMES Energy Modeling System
Based on thesis "Modelling and Analysis of the Least Cost Power Generation Options for Pakistan"
"""

# Study Period Configuration
STUDY_PERIOD = {
    'start_year': 2014,
    'end_year': 2033,
    'base_year': 2014,
    'years': list(range(2014, 2034))
}

# Economic Parameters
ECONOMIC_PARAMS = {
    'discount_rate': 0.10,  # 10% as per thesis
    'exchange_rate_usd_pkr': 105.0,  # Approximate rate during study period
    'inflation_rate': 0.05  # 5% annual inflation
}

# Technology Codes from Table 5.5
TECHNOLOGIES = {
    'BAGAS': 'Bagasse',
    'BIOMC': 'Biomass Combustion',
    'HCOAL': 'Hard Coal',
    'HYDRO': 'Hydroelectric',
    'HYDRUNOF': 'Hydro Run-of-River',
    'LIGIN': 'Lignite',
    'NGCC': 'Natural Gas Combined Cycle',
    'NGTOC': 'Natural Gas Open Cycle',
    'NUCFUEL': 'Nuclear Fuel',
    'OILFUR': 'Oil Furnace',
    'SOLARE': 'Solar Energy',
    'WIND_A': 'Wind Energy'
}

# Demand Scenarios from Chapter 4
DEMAND_SCENARIOS = {
    'BAU': 'Business as Usual',
    'LEG': 'Low Economic Growth',
    'MEG': 'Medium Economic Growth',
    'HEG': 'High Economic Growth'
}

# Model Scenarios from Table 8.1
MODEL_SCENARIOS = {
    'BASE': {
        'description': 'Business as Usual',
        'external_costs': False,
        'emission_cap': None,
        'renewable_target': None
    },
    'CEC10': {
        'description': 'Carbon Emission Cap 10%',
        'external_costs': True,
        'emission_cap': 0.10,
        'renewable_target': None
    },
    'CEC20': {
        'description': 'Carbon Emission Cap 20%',
        'external_costs': True,
        'emission_cap': 0.20,
        'renewable_target': None
    },
    'COALMAX': {
        'description': 'Maximum Indigenous Coal',
        'external_costs': True,
        'indigenous_preference': True,
        'coal_max': True
    },
    'REN50': {
        'description': 'Renewable Energy 50%',
        'external_costs': True,
        'renewable_target': 0.50
    },
    'REN60': {
        'description': 'Renewable Energy 60%',
        'external_costs': True,
        'renewable_target': 0.60
    }
}

# File Paths
FILE_PATHS = {
    'input_dir': 'data/input/',
    'output_dir': 'data/output/',
    'templates_dir': 'data/input/templates/',
    'results_dir': 'data/output/results/',
    'reports_dir': 'data/output/reports/'
}

# External Cost Scaling Factor (CASES study adaptation)
EXTERNAL_COST_SCALING = 19.0  # Scaling factor for Pakistan

# Validation Parameters
VALIDATION = {
    'base_year_tolerance': 0.05,  # 5% tolerance for base year calibration
    'emission_validation': True,
    'cost_validation': True
}
