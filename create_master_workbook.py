#!/usr/bin/env python3
"""
PakistanTIMES 2025 - Master Workbook Creator
This script creates a comprehensive Excel workbook with all scenario data.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def create_master_workbook():
    print("Creating PakistanTIMES 2025 Master Workbook...")
    
    # Read the detailed results CSV
    csv_path = "comprehensive_results_export_20250825_083359/PakistanTIMES_2025_Detailed_Results_20250825_083359.csv"
    df = pd.read_csv(csv_path)
    
    # Create Excel writer
    output_path = "PakistanTIMES_2025_Master_Results.xlsx"
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        
        # 1. Scenario Summary Sheet
        print("Creating Scenario Summary sheet...")
        create_scenario_summary(df, writer)
        
        # 2. Detailed Annual Results Sheet
        print("Creating Detailed Annual Results sheet...")
        df.to_excel(writer, sheet_name='Detailed_Annual_Results', index=False)
        
        # 3. Renewable Trajectories Sheet
        print("Creating Renewable Trajectories sheet...")
        create_renewable_trajectories(df, writer)
        
        # 4. Investment Analysis Sheet
        print("Creating Investment Analysis sheet...")
        create_investment_analysis(df, writer)
        
        # 5. Emissions Analysis Sheet
        print("Creating Emissions Analysis sheet...")
        create_emissions_analysis(df, writer)
        
        # 6. Technology Deployment Sheet
        print("Creating Technology Deployment sheet...")
        create_technology_deployment(df, writer)
        
        # 7. Economic Impact Sheet
        print("Creating Economic Impact sheet...")
        create_economic_impact(df, writer)
    
    print(f"Master workbook created successfully: {output_path}")
    print("Workbook contains 7 sheets with comprehensive analysis")

def create_scenario_summary(df, writer):
    """Create scenario summary sheet with key metrics"""
    summary_data = []
    
    # Group by scenario and calculate summary statistics
    for scenario in df['Scenario'].unique():
        scenario_df = df[df['Scenario'] == scenario]
        
        # Extract scenario components
        renewable_target = scenario.split('_')[0]
        demand_scenario = scenario.split('_')[1]
        
        summary_data.append({
            'Scenario': scenario,
            'Renewable_Target': renewable_target,
            'Demand_Scenario': demand_scenario,
            'Final_Renewable_Share_2050_%': scenario_df[scenario_df['Year'] == 2050]['Renewable_Share_%'].values[0],
            'Avg_Renewable_Share_%': scenario_df['Renewable_Share_%'].mean(),
            'Cumulative_Emissions_2014_2050_GtCO2': scenario_df['Annual_Emissions_MtCO2'].sum() / 1000,
            'Annual_Emissions_2050_MtCO2': scenario_df[scenario_df['Year'] == 2050]['Annual_Emissions_MtCO2'].values[0],
            'Total_Investment_2014_2050_Billion_USD': scenario_df['Investment_Billion_USD'].sum(),
            'Final_Demand_2050_TWh': scenario_df[scenario_df['Year'] == 2050]['Demand_TWh'].values[0],
            'Emissions_Reduction_vs_BAU_%': calculate_emissions_reduction(df, scenario)
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Scenario_Summary', index=False)

def create_renewable_trajectories(df, writer):
    """Create renewable trajectories sheet"""
    # Pivot to get renewable share by year and scenario
    pivot_df = df.pivot_table(
        values='Renewable_Share_%',
        index='Year',
        columns='Scenario',
        aggfunc='mean'
    )
    pivot_df.to_excel(writer, sheet_name='Renewable_Trajectories')

def create_investment_analysis(df, writer):
    """Create investment analysis sheet"""
    # Cumulative investment by scenario
    investment_df = df.groupby(['Scenario', 'Year'])['Investment_Billion_USD'].sum().unstack('Scenario')
    investment_df.to_excel(writer, sheet_name='Investment_Analysis')

def create_emissions_analysis(df, writer):
    """Create emissions analysis sheet"""
    # Emissions by scenario
    emissions_df = df.pivot_table(
        values='Annual_Emissions_MtCO2',
        index='Year',
        columns='Scenario',
        aggfunc='mean'
    )
    emissions_df.to_excel(writer, sheet_name='Emissions_Analysis')

def create_technology_deployment(df, writer):
    """Create technology deployment sheet"""
    tech_df = df[['Year', 'Scenario', 'Renewable_Generation_GWh', 'Fossil_Generation_GWh', 'Total_Generation_GWh']].copy()
    tech_df['Renewable_Share_GWh'] = tech_df['Renewable_Generation_GWh']
    tech_df['Fossil_Share_GWh'] = tech_df['Fossil_Generation_GWh']
    
    pivot_df = tech_df.pivot_table(
        values=['Renewable_Share_GWh', 'Fossil_Share_GWh'],
        index='Year',
        columns='Scenario',
        aggfunc='mean'
    )
    pivot_df.to_excel(writer, sheet_name='Technology_Deployment')

def create_economic_impact(df, writer):
    """Create economic impact sheet"""
    # Economic indicators by scenario
    economic_df = df.groupby(['Scenario', 'Year']).agg({
        'Investment_Billion_USD': 'sum',
        'Demand_TWh': 'mean',
        'Annual_Emissions_MtCO2': 'mean'
    }).unstack('Scenario')
    economic_df.to_excel(writer, sheet_name='Economic_Impact')

def calculate_emissions_reduction(df, scenario):
    """Calculate emissions reduction compared to BAU scenario"""
    bau_scenario = scenario.split('_')[0] + '_BAU'
    if scenario == bau_scenario:
        return 0.0
    
    scenario_2050_emissions = df[(df['Scenario'] == scenario) & (df['Year'] == 2050)]['Annual_Emissions_MtCO2'].values[0]
    bau_2050_emissions = df[(df['Scenario'] == bau_scenario) & (df['Year'] == 2050)]['Annual_Emissions_MtCO2'].values[0]
    
    reduction = ((bau_2050_emissions - scenario_2050_emissions) / bau_2050_emissions) * 100
    return round(reduction, 1)

if __name__ == "__main__":
    create_master_workbook()
