#!/usr/bin/env python3
"""
PakistanTIMES 2025 - Quality Assurance Script
This script performs data validation and quality checks on all generated files.
"""

import pandas as pd
import os

def validate_data_consistency():
    print("Performing quality assurance checks...")
    
    # Check if all required files exist
    required_files = [
        'PakistanTIMES_2025_Master_Results.xlsx',
        'Master_Scenario_Summary.csv',
        'Detailed_Annual_Results.csv',
        'Renewable_Trajectories.csv',
        'Investment_Analysis.csv',
        'Emissions_Analysis.csv',
        'Technology_Deployment.csv',
        'Economic_Impact.csv'
    ]
    
    print("Checking file existence...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
    
    # Validate Excel workbook structure
    print("\nValidating Excel workbook...")
    try:
        xls = pd.ExcelFile('PakistanTIMES_2025_Master_Results.xlsx')
        sheets = xls.sheet_names
        expected_sheets = [
            'Executive_Summary',
            'Scenario_Summary',
            'Detailed_Annual_Results',
            'Renewable_Trajectories',
            'Investment_Analysis',
            'Emissions_Analysis',
            'Technology_Deployment',
            'Economic_Impact',
            'Data_Dictionary'
        ]
        
        for sheet in expected_sheets:
            if sheet in sheets:
                print(f"✅ Sheet '{sheet}' - Found")
            else:
                print(f"❌ Sheet '{sheet}' - Missing")
                
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
    
    # Validate CSV files
    print("\nValidating CSV files...")
    csv_files = [
        'Master_Scenario_Summary.csv',
        'Detailed_Annual_Results.csv',
        'Renewable_Trajectories.csv',
        'Investment_Analysis.csv',
        'Emissions_Analysis.csv',
        'Technology_Deployment.csv',
        'Economic_Impact.csv'
    ]
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            print(f"✅ {csv_file} - Valid ({len(df)} rows, {len(df.columns)} columns)")
        except Exception as e:
            print(f"❌ {csv_file} - Error: {e}")
    
    # Check report files
    print("\nChecking report files...")
    report_files = [
        'Executive_Summary.md',
        'Investment_Analysis_Report.md',
        'Emissions_Analysis_Report.md',
        'Renewable_Trajectories_Report.md',
        'Technology_Deployment_Report.md',
        'Economic_Impact_Report.md',
        'Model_Validation_Report.md'
    ]
    
    for report in report_files:
        if os.path.exists(report):
            size = os.path.getsize(report)
            print(f"✅ {report} - Found ({size} bytes)")
        else:
            print(f"❌ {report} - Missing")
    
    # Check documentation files
    print("\nChecking documentation files...")
    doc_files = [
        'README.md',
        'Data_Dictionary.md',
        'Usage_Guidelines.md'
    ]
    
    for doc in doc_files:
        if os.path.exists(doc):
            size = os.path.getsize(doc)
            print(f"✅ {doc} - Found ({size} bytes)")
        else:
            print(f"❌ {doc} - Missing")
    
    print("\nQuality assurance checks completed!")

if __name__ == "__main__":
    validate_data_consistency()
