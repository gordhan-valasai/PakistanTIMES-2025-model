#!/usr/bin/env python3
"""
PakistanTIMES 2025 - CSV Files Creator
This script generates comprehensive CSV files from the master workbook data.
"""

import pandas as pd

def create_csv_files():
    print("Generating comprehensive CSV files for PakistanTIMES 2025...")
    
    # Load the master workbook
    master_workbook_path = "PakistanTIMES_2025_Master_Results.xlsx"
    xls = pd.ExcelFile(master_workbook_path)
    
    # 1. Master Scenario Summary CSV
    print("Creating Master Scenario Summary CSV...")
    scenario_summary_df = pd.read_excel(xls, sheet_name='Scenario_Summary')
    scenario_summary_df.to_csv('Master_Scenario_Summary.csv', index=False)

    # 2. Detailed Annual Results CSV
    print("Creating Detailed Annual Results CSV...")
    annual_results_df = pd.read_excel(xls, sheet_name='Detailed_Annual_Results')
    annual_results_df.to_csv('Detailed_Annual_Results.csv', index=False)

    # 3. Renewable Trajectories CSV
    print("Creating Renewable Trajectories CSV...")
    renewable_trajectories_df = pd.read_excel(xls, sheet_name='Renewable_Trajectories')
    renewable_trajectories_df.to_csv('Renewable_Trajectories.csv', index=False)

    # 4. Investment Analysis CSV
    print("Creating Investment Analysis CSV...")
    investment_analysis_df = pd.read_excel(xls, sheet_name='Investment_Analysis')
    investment_analysis_df.to_csv('Investment_Analysis.csv', index=False)

    # 5. Emissions Analysis CSV
    print("Creating Emissions Analysis CSV...")
    emissions_analysis_df = pd.read_excel(xls, sheet_name='Emissions_Analysis')
    emissions_analysis_df.to_csv('Emissions_Analysis.csv', index=False)

    # 6. Technology Deployment CSV
    print("Creating Technology Deployment CSV...")
    technology_deployment_df = pd.read_excel(xls, sheet_name='Technology_Deployment')
    technology_deployment_df.to_csv('Technology_Deployment.csv', index=False)

    # 7. Economic Impact CSV
    print("Creating Economic Impact CSV...")
    economic_impact_df = pd.read_excel(xls, sheet_name='Economic_Impact')
    economic_impact_df.to_csv('Economic_Impact.csv', index=False)

    print("All CSV files created successfully!")

if __name__ == "__main__":
    create_csv_files()
