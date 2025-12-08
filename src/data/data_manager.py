"""
Data Manager for PakistanTIMES Model
Handles loading and validation of input data from Excel templates
"""

import pandas as pd
import os
from typing import Dict, Any, Optional
from config.config import FILE_PATHS, TECHNOLOGIES, STUDY_PERIOD

class DataManager:
    def __init__(self, data_path: str = None):
        self.data_path = data_path or FILE_PATHS['input_dir']
        self.technology_data = None
        self.demand_data = None
        self.resource_data = None
        self.external_costs = None
        self.validation_errors = []
        
    def load_all_data(self) -> bool:
        """Load all input data from Excel templates"""
        try:
            self.technology_data = self.load_technology_data()
            self.demand_data = self.load_demand_data()
            self.resource_data = self.load_resource_data()
            self.external_costs = self.load_external_costs()
            
            # Validate all loaded data
            validation_result = self.validate_data()
            
            if not validation_result:
                print("Data validation failed. Please check the following errors:")
                for error in self.validation_errors:
                    print(f"  - {error}")
                return False
            
            print("All data loaded and validated successfully!")
            return True
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def load_technology_data(self) -> pd.DataFrame:
        """Load technology parameters from Excel file"""
        file_path = os.path.join(self.data_path, 'technologies.xlsx')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Technology data file not found: {file_path}")
        
        df = pd.read_excel(file_path, sheet_name='Technology_Parameters')
        
        # Validate required columns
        required_columns = [
            'Technology_Code', 'Technology_Name', 'Capital_Cost_USD_MW',
            'FOM_Cost_USD_MW', 'Variable_Cost_USD_MWh', 'Efficiency_%',
            'Annual_Availability_%', 'Lifetime_Years', 'Technical_Life_Years',
            'CO2_Emission_kg_MWh', 'NOx_Emission_kg_MWh', 'SO2_Emission_kg_MWh',
            'Construction_Lead_Time_Years', 'Capacity_Factor_%'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in technology data: {missing_columns}")
        
        # Set technology code as index
        df.set_index('Technology_Code', inplace=True)
        
        print(f"Technology data loaded: {len(df)} technologies")
        return df
    
    def load_demand_data(self) -> pd.DataFrame:
        """Load demand forecast data from Excel file"""
        file_path = os.path.join(self.data_path, 'demand_forecast.xlsx')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Demand forecast file not found: {file_path}")
        
        df = pd.read_excel(file_path, sheet_name='Demand_Forecast')
        
        # Validate required columns
        required_columns = ['Year', 'BAU_GWh', 'LEG_GWh', 'MEG_GWh', 'HEG_GWh']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in demand data: {missing_columns}")
        
        # Set year as index
        df.set_index('Year', inplace=True)
        
        print(f"Demand forecast data loaded: {len(df)} years")
        return df
    
    def load_resource_data(self) -> pd.DataFrame:
        """Load resource availability data from Excel file"""
        file_path = os.path.join(self.data_path, 'resources.xlsx')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Resource data file not found: {file_path}")
        
        df = pd.read_excel(file_path, sheet_name='Resource_Availability')
        
        # Validate required columns
        required_columns = [
            'Resource_Type', 'Annual_Availability_PJ', 'Unit_Cost_USD_PJ',
            'CO2_Content_kg_PJ', 'Availability_Constraint'
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in resource data: {missing_columns}")
        
        # Set resource type as index
        df.set_index('Resource_Type', inplace=True)
        
        print(f"Resource data loaded: {len(df)} resource types")
        return df
    
    def load_external_costs(self) -> pd.DataFrame:
        """Load external costs data from Excel file"""
        file_path = os.path.join(self.data_path, 'external_costs.xlsx')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"External costs file not found: {file_path}")
        
        df = pd.read_excel(file_path, sheet_name='External_Costs')
        
        # Validate required columns
        required_columns = [
            'Emission_Type', 'Unit_Cost_USD_kg', 'Scaling_Factor_Pakistan',
            'Adjusted_Cost_USD_kg', 'Source'
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns in external costs data: {missing_columns}")
        
        # Set emission type as index
        df.set_index('Emission_Type', inplace=True)
        
        print(f"External costs data loaded: {len(df)} emission types")
        return df
    
    def validate_data(self) -> bool:
        """Validate data consistency and completeness"""
        self.validation_errors = []
        
        # Validate technology data
        if self.technology_data is not None:
            self._validate_technology_data()
        
        # Validate demand data
        if self.demand_data is not None:
            self._validate_demand_data()
        
        # Validate resource data
        if self.resource_data is not None:
            self._validate_resource_data()
        
        # Validate external costs data
        if self.external_costs is not None:
            self._validate_external_costs_data()
        
        return len(self.validation_errors) == 0
    
    def _validate_technology_data(self):
        """Validate technology data"""
        df = self.technology_data
        
        # Check for missing values
        for col in df.columns:
            if df[col].isnull().any():
                self.validation_errors.append(f"Missing values in technology data column: {col}")
        
        # Check for negative costs
        cost_columns = ['Capital_Cost_USD_MW', 'FOM_Cost_USD_MW', 'Variable_Cost_USD_MWh']
        for col in cost_columns:
            if (df[col] < 0).any():
                self.validation_errors.append(f"Negative values found in {col}")
        
        # Check efficiency range
        if ((df['Efficiency_%'] < 0) | (df['Efficiency_%'] > 100)).any():
            self.validation_errors.append("Efficiency values must be between 0 and 100")
    
    def _validate_demand_data(self):
        """Validate demand forecast data"""
        df = self.demand_data
        
        # Check for missing values
        for col in df.columns:
            if df[col].isnull().any():
                self.validation_errors.append(f"Missing values in demand data column: {col}")
        
        # Check for negative demand
        demand_columns = ['BAU_GWh', 'LEG_GWh', 'MEG_GWh', 'HEG_GWh']
        for col in demand_columns:
            if (df[col] < 0).any():
                self.validation_errors.append(f"Negative values found in {col}")
        
        # Check year range
        expected_years = STUDY_PERIOD['years']
        if not all(year in df.index for year in expected_years):
            self.validation_errors.append("Demand data must cover all study period years")
    
    def _validate_resource_data(self):
        """Validate resource availability data"""
        df = self.resource_data
        
        # Check for missing values
        for col in df.columns:
            if df[col].isnull().any():
                self.validation_errors.append(f"Missing values in resource data column: {col}")
        
        # Check for negative availability
        if (df['Annual_Availability_PJ'] < 0).any():
            self.validation_errors.append("Resource availability cannot be negative")
    
    def _validate_external_costs_data(self):
        """Validate external costs data"""
        df = self.external_costs
        
        # Check for missing values
        for col in df.columns:
            if df[col].isnull().any():
                self.validation_errors.append(f"Missing values in external costs column: {col}")
        
        # Check for negative costs
        if (df['Unit_Cost_USD_kg'] < 0).any():
            self.validation_errors.append("External costs cannot be negative")
    
    def get_technology_data(self) -> pd.DataFrame:
        """Get technology data"""
        return self.technology_data
    
    def get_demand_data(self, scenario: str = 'BAU') -> pd.Series:
        """Get demand data for specific scenario"""
        if self.demand_data is None:
            return None
        
        if scenario not in self.demand_data.columns:
            raise ValueError(f"Scenario {scenario} not found in demand data")
        
        return self.demand_data[scenario]
    
    def get_resource_data(self) -> pd.DataFrame:
        """Get resource availability data"""
        return self.resource_data
    
    def get_external_costs(self) -> pd.DataFrame:
        """Get external costs data"""
        return self.external_costs
    
    def export_validation_report(self, output_path: str):
        """Export validation report to file"""
        if not self.validation_errors:
            report = "Data validation passed successfully!\n"
        else:
            report = "Data validation failed with the following errors:\n\n"
            for i, error in enumerate(self.validation_errors, 1):
                report += f"{i}. {error}\n"
        
        with open(output_path, 'w') as f:
            f.write(report)
        
        print(f"Validation report exported to: {output_path}")
