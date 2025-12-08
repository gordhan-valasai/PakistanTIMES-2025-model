#!/usr/bin/env python3
"""
Excel Report Generator for PakistanTIMES
========================================

This module generates comprehensive Excel reports with separate sheets for
input data and results analysis.

Author: PakistanTIMES Model Development Team
Date: 2025
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import os
from datetime import datetime

class ExcelReportGenerator:
    """
    Comprehensive Excel report generator for PakistanTIMES analysis
    """
    
    def __init__(self):
        """Initialize the Excel report generator"""
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"📊 Excel Report Generator initialized at {self.timestamp}")
    
    def create_comprehensive_report(self, 
                                  historical_data: pd.DataFrame,
                                  scenario_results: Dict,
                                  output_path: str = "data/reports/") -> str:
        """
        Create comprehensive Excel report with input and results sheets
        
        Args:
            historical_data: Historical Pakistan data (2000-2024)
            scenario_results: Results from all scenarios
            output_path: Path to save the report
            
        Returns:
            Path to the generated Excel file
        """
        print("📊 Creating comprehensive Excel report...")
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Generate filename with timestamp
        filename = f"pakistan_times_comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(output_path, filename)
        
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            # Create Input Data Sheet
            self._create_input_data_sheet(writer, historical_data)
            
            # Create Results Summary Sheet
            self._create_results_summary_sheet(writer, scenario_results)
            
            # Create Scenario Comparison Sheet
            self._create_scenario_comparison_sheet(writer, scenario_results)
            
            # Create Technical Analysis Sheet
            self._create_technical_analysis_sheet(writer, scenario_results)
            
            # Create Policy Recommendations Sheet
            self._create_policy_recommendations_sheet(writer, scenario_results)
            
            # Create Data Dictionary Sheet
            self._create_data_dictionary_sheet(writer)
        
        print(f"✅ Comprehensive Excel report created: {filepath}")
        return filepath
    
    def _create_input_data_sheet(self, writer, historical_data: pd.DataFrame):
        """Create comprehensive input data sheet"""
        
        # Prepare historical data for input sheet
        input_data = historical_data.copy()
        input_data.index.name = 'Year'
        
        # Add data source information
        input_data['Data_Source'] = 'Pakistan Bureau of Statistics'
        input_data['Last_Updated'] = '2024'
        input_data['Data_Quality'] = 'High'
        
        # Create input sheet
        input_data.to_excel(writer, sheet_name='Input_Data_2000_2024')
        
        # Get workbook and worksheet for formatting
        workbook = writer.book
        worksheet = writer.sheets['Input_Data_2000_2024']
        
        # Add formatting
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        # Format headers
        for col_num, value in enumerate(input_data.columns.values):
            worksheet.write(0, col_num + 1, value, header_format)
        
        # Add metadata section
        self._add_metadata_section(worksheet, workbook, 'Input Data Sources and Methodology')
        
        print("✅ Input Data sheet created")
    
    def _create_results_summary_sheet(self, writer, scenario_results: Dict):
        """Create results summary sheet"""
        
        # Prepare summary data
        summary_data = []
        
        for scenario_name, results in scenario_results.items():
            metrics = results['key_metrics']
            summary_data.append({
                'Scenario': scenario_name,
                'Electricity_2024_TWh': results['scenario_data'].loc[2024, 'Electricity_Consumption_TWh'],
                'Electricity_2050_TWh': metrics['electricity_2050'],
                'Electricity_Growth_%': metrics['electricity_growth_2024_2050'],
                'Energy_2024_MTOE': results['scenario_data'].loc[2024, 'Total_Energy_Consumption_MTOE'],
                'Energy_2050_MTOE': metrics['energy_2050'],
                'Energy_Growth_%': metrics['energy_growth_2024_2050'],
                'Capacity_2024_MW': results['scenario_data'].loc[2024, 'Installed_Capacity_MW'],
                'Capacity_2050_MW': metrics['capacity_2050'],
                'Capacity_Growth_%': metrics['capacity_growth_2024_2050'],
                'Emissions_2024_Mt': results['scenario_data'].loc[2024, 'CO2_Emissions_Million_Tonnes'] if 'CO2_Emissions_Million_Tonnes' in results['scenario_data'].columns else 0,
                'Emissions_2050_Mt': metrics['emissions_2050'],
                'Emissions_Change_%': metrics['emissions_change_2024_2050']
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Results_Summary', index=False)
        
        # Format the results sheet
        workbook = writer.book
        worksheet = writer.sheets['Results_Summary']
        
        # Add formatting
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#B8CCE4',
            'border': 1
        })
        
        # Format headers
        for col_num, value in enumerate(summary_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Add metadata section
        self._add_metadata_section(worksheet, workbook, 'Model Results Summary')
        
        print("✅ Results Summary sheet created")
    
    def _create_scenario_comparison_sheet(self, writer, scenario_results: Dict):
        """Create detailed scenario comparison sheet"""
        
        # Prepare comparison data for key years
        key_years = [2024, 2030, 2040, 2050]
        comparison_data = []
        
        for scenario_name, results in scenario_results.items():
            data = results['scenario_data']
            
            for year in key_years:
                if year in data.index:
                    row = {
                        'Scenario': scenario_name,
                        'Year': year,
                        'Electricity_TWh': data.loc[year, 'Electricity_Consumption_TWh'],
                        'Energy_MTOE': data.loc[year, 'Total_Energy_Consumption_MTOE'],
                        'Capacity_MW': data.loc[year, 'Installed_Capacity_MW'],
                        'GDP_Billion_USD': data.loc[year, 'GDP_Current_USD_Billion'],
                        'Population_Million': data.loc[year, 'Population_Million']
                    }
                    
                    if 'CO2_Emissions_Million_Tonnes' in data.columns:
                        row['CO2_Emissions_Mt'] = data.loc[year, 'CO2_Emissions_Million_Tonnes']
                    else:
                        row['CO2_Emissions_Mt'] = 0
                    
                    comparison_data.append(row)
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df.to_excel(writer, sheet_name='Scenario_Comparison', index=False)
        
        # Format the comparison sheet
        workbook = writer.book
        worksheet = writer.sheets['Scenario_Comparison']
        
        # Add formatting
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D8E4BC',
            'border': 1
        })
        
        # Format headers
        for col_num, value in enumerate(comparison_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        print("✅ Scenario Comparison sheet created")
    
    def _create_technical_analysis_sheet(self, writer, scenario_results: Dict):
        """Create technical analysis sheet"""
        
        # Prepare technical analysis data
        technical_data = []
        
        for scenario_name, results in scenario_results.items():
            data = results['scenario_data']
            
            # Calculate technical indicators
            for year in [2024, 2030, 2040, 2050]:
                if year in data.index:
                    # Energy intensity
                    energy_intensity = data.loc[year, 'Total_Energy_Consumption_MTOE'] / data.loc[year, 'GDP_Current_USD_Billion']
                    
                    # Electricity intensity
                    electricity_intensity = data.loc[year, 'Electricity_Consumption_TWh'] * 1000 / data.loc[year, 'GDP_Current_USD_Billion']
                    
                    # GDP per capita
                    gdp_per_capita = data.loc[year, 'GDP_Current_USD_Billion'] * 1000 / data.loc[year, 'Population_Million']
                    
                    # Capacity factor (estimated)
                    annual_hours = 8760
                    capacity_factor = (data.loc[year, 'Electricity_Consumption_TWh'] * 1000) / (data.loc[year, 'Installed_Capacity_MW'] * annual_hours)
                    
                    row = {
                        'Scenario': scenario_name,
                        'Year': year,
                        'Energy_Intensity_MTOE_per_Billion_USD': energy_intensity,
                        'Electricity_Intensity_MWh_per_Billion_USD': electricity_intensity,
                        'GDP_per_Capita_USD': gdp_per_capita,
                        'Estimated_Capacity_Factor': capacity_factor,
                        'Population_Million': data.loc[year, 'Population_Million'],
                        'GDP_Billion_USD': data.loc[year, 'GDP_Current_USD_Billion']
                    }
                    
                    technical_data.append(row)
        
        technical_df = pd.DataFrame(technical_data)
        technical_df.to_excel(writer, sheet_name='Technical_Analysis', index=False)
        
        # Format the technical analysis sheet
        workbook = writer.book
        worksheet = writer.sheets['Technical_Analysis']
        
        # Add formatting
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#E6B8B8',
            'border': 1
        })
        
        # Format headers
        for col_num, value in enumerate(technical_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        print("✅ Technical Analysis sheet created")
    
    def _create_policy_recommendations_sheet(self, writer, scenario_results: Dict):
        """Create policy recommendations sheet"""
        
        # Prepare policy recommendations
        policy_data = [
            {
                'Policy_Area': 'Renewable Energy',
                'Recommendation': 'Implement ambitious renewable energy targets',
                'Target_2050': '80-95% renewable penetration',
                'Implementation_Time': '2025-2050',
                'Expected_Impact': '60-90% CO2 emissions reduction',
                'Priority': 'High'
            },
            {
                'Policy_Area': 'Energy Efficiency',
                'Recommendation': 'Establish energy efficiency standards',
                'Target_2050': '2-3% annual efficiency improvement',
                'Implementation_Time': '2025-2030',
                'Expected_Impact': '20-30% energy demand reduction',
                'Priority': 'High'
            },
            {
                'Policy_Area': 'Carbon Pricing',
                'Recommendation': 'Introduce carbon pricing mechanism',
                'Target_2050': '$100-200/ton CO2',
                'Implementation_Time': '2025-2040',
                'Expected_Impact': 'Market-driven decarbonization',
                'Priority': 'Medium'
            },
            {
                'Policy_Area': 'Grid Infrastructure',
                'Recommendation': 'Develop smart grid infrastructure',
                'Target_2050': '100% smart grid coverage',
                'Implementation_Time': '2025-2045',
                'Expected_Impact': 'Improved renewable integration',
                'Priority': 'Medium'
            },
            {
                'Policy_Area': 'Technology Investment',
                'Recommendation': 'Invest in clean energy technologies',
                'Target_2050': '5% of GDP annually',
                'Implementation_Time': '2025-2050',
                'Expected_Impact': 'Accelerated technology deployment',
                'Priority': 'High'
            }
        ]
        
        policy_df = pd.DataFrame(policy_data)
        policy_df.to_excel(writer, sheet_name='Policy_Recommendations', index=False)
        
        # Format the policy recommendations sheet
        workbook = writer.book
        worksheet = writer.sheets['Policy_Recommendations']
        
        # Add formatting
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#B8CCE4',
            'border': 1
        })
        
        # Format headers
        for col_num, value in enumerate(policy_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        print("✅ Policy Recommendations sheet created")
    
    def _create_data_dictionary_sheet(self, writer):
        """Create data dictionary sheet"""
        
        # Prepare data dictionary
        data_dict = [
            {
                'Variable': 'Electricity_Consumption_TWh',
                'Description': 'Total electricity consumption in Terawatt-hours',
                'Unit': 'TWh',
                'Source': 'Pakistan Energy Yearbook',
                'Frequency': 'Annual'
            },
            {
                'Variable': 'Total_Energy_Consumption_MTOE',
                'Description': 'Total primary energy consumption in Million Tonnes of Oil Equivalent',
                'Unit': 'MTOE',
                'Source': 'Pakistan Energy Yearbook',
                'Frequency': 'Annual'
            },
            {
                'Variable': 'Installed_Capacity_MW',
                'Description': 'Total installed electricity generation capacity in Megawatts',
                'Unit': 'MW',
                'Source': 'NEPRA Annual Reports',
                'Frequency': 'Annual'
            },
            {
                'Variable': 'GDP_Current_USD_Billion',
                'Description': 'Gross Domestic Product in current US Dollars (Billions)',
                'Unit': 'Billion USD',
                'Source': 'Pakistan Bureau of Statistics',
                'Frequency': 'Annual'
            },
            {
                'Variable': 'Population_Million',
                'Description': 'Total population in millions',
                'Unit': 'Million',
                'Source': 'Pakistan Bureau of Statistics',
                'Frequency': 'Annual'
            },
            {
                'Variable': 'CO2_Emissions_Million_Tonnes',
                'Description': 'Carbon dioxide emissions from energy sector in million tonnes',
                'Unit': 'Million Tonnes',
                'Source': 'Calculated from energy consumption data',
                'Frequency': 'Annual'
            }
        ]
        
        dict_df = pd.DataFrame(data_dict)
        dict_df.to_excel(writer, sheet_name='Data_Dictionary', index=False)
        
        # Format the data dictionary sheet
        workbook = writer.book
        worksheet = writer.sheets['Data_Dictionary']
        
        # Add formatting
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#F2DCDB',
            'border': 1
        })
        
        # Format headers
        for col_num, value in enumerate(dict_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        print("✅ Data Dictionary sheet created")
    
    def _add_metadata_section(self, worksheet, workbook, title: str):
        """Add metadata section to worksheet"""
        
        # Metadata format
        metadata_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'fg_color': '#E6E6E6'
        })
        
        # Add metadata
        worksheet.write('A1', f'Report: {title}', metadata_format)
        worksheet.write('A2', f'Generated: {self.timestamp}', metadata_format)
        worksheet.write('A3', 'Source: PakistanTIMES Energy Model', metadata_format)
        worksheet.write('A4', 'Data Quality: High', metadata_format)
        
        # Adjust column widths
        worksheet.set_column('A:Z', 15)
    
    def create_simple_two_sheet_report(self, 
                                     historical_data: pd.DataFrame,
                                     scenario_results: Dict,
                                     output_path: str = "data/reports/") -> str:
        """
        Create simple two-sheet report: Input and Results
        
        Args:
            historical_data: Historical Pakistan data (2000-2024)
            scenario_results: Results from all scenarios
            output_path: Path to save the report
            
        Returns:
            Path to the generated Excel file
        """
        print("📊 Creating simple two-sheet Excel report...")
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Generate filename
        filename = f"pakistan_times_input_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(output_path, filename)
        
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            # Sheet 1: Input Data
            self._create_input_data_sheet(writer, historical_data)
            
            # Sheet 2: Results Summary
            self._create_results_summary_sheet(writer, scenario_results)
        
        print(f"✅ Simple two-sheet report created: {filepath}")
        return filepath
