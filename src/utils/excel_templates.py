"""
Excel Template Generator for PakistanTIMES Model
Creates input data templates based on thesis specifications
"""

import pandas as pd
import xlsxwriter
from config.config import TECHNOLOGIES, STUDY_PERIOD, DEMAND_SCENARIOS

class ExcelTemplateGenerator:
    def __init__(self):
        self.technologies = TECHNOLOGIES
        self.years = STUDY_PERIOD['years']
        self.demand_scenarios = DEMAND_SCENARIOS
    
    def create_technology_template(self, output_path):
        """Create technology parameters template based on Table 7.3 and 7.4"""
        
        # Technology parameters structure
        tech_data = {
            'Technology_Code': list(self.technologies.keys()),
            'Technology_Name': list(self.technologies.values()),
            'Capital_Cost_USD_MW': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Placeholder values
            'FOM_Cost_USD_MW': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],      # Placeholder values
            'Variable_Cost_USD_MWh': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Placeholder values
            'Efficiency_%': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],          # Placeholder values
            'Annual_Availability_%': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Placeholder values
            'Lifetime_Years': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],        # Placeholder values
            'Technical_Life_Years': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # Placeholder values
            'CO2_Emission_kg_MWh': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Placeholder values
            'NOx_Emission_kg_MWh': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Placeholder values
            'SO2_Emission_kg_MWh': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # Placeholder values
            'Construction_Lead_Time_Years': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Placeholder values
            'Capacity_Factor_%': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]       # Placeholder values
        }
        
        df = pd.DataFrame(tech_data)
        
        # Create Excel file with formatting
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Technology_Parameters', index=False)
            
            # Get workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Technology_Parameters']
            
            # Add formatting
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # Apply header formatting
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Set column widths
            for col_num, value in enumerate(df.columns.values):
                max_length = max(len(str(value)), 
                               df[value].astype(str).str.len().max())
                worksheet.set_column(col_num, col_num, max_length + 2)
        
        print(f"Technology template created: {output_path}")
        return df
    
    def create_demand_template(self, output_path):
        """Create demand forecast template based on Table 7.1"""
        
        # Demand forecast structure
        demand_data = {
            'Year': self.years,
            'BAU_GWh': [0] * len(self.years),  # Placeholder values
            'LEG_GWh': [0] * len(self.years),  # Placeholder values
            'MEG_GWh': [0] * len(self.years),  # Placeholder values
            'HEG_GWh': [0] * len(self.years)   # Placeholder values
        }
        
        df = pd.DataFrame(demand_data)
        
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Demand_Forecast', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Demand_Forecast']
            
            # Add formatting
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # Apply header formatting
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Set column widths
            for col_num, value in enumerate(df.columns.values):
                max_length = max(len(str(value)), 
                               df[value].astype(str).str.len().max())
                worksheet.set_column(col_num, col_num, max_length + 2)
        
        print(f"Demand forecast template created: {output_path}")
        return df
    
    def create_resource_template(self, output_path):
        """Create resource availability template"""
        
        resource_types = [
            'Natural_Gas', 'Coal_Hard', 'Coal_Lignite', 'Oil_Furnace',
            'Nuclear_Fuel', 'Biomass', 'Bagasse', 'Solar_Resource', 
            'Wind_Resource', 'Hydro_Resource'
        ]
        
        resource_data = {
            'Resource_Type': resource_types,
            'Annual_Availability_PJ': [0] * len(resource_types),  # Placeholder values
            'Unit_Cost_USD_PJ': [0] * len(resource_types),       # Placeholder values
            'CO2_Content_kg_PJ': [0] * len(resource_types),      # Placeholder values
            'Availability_Constraint': ['Yes'] * len(resource_types)  # Placeholder values
        }
        
        df = pd.DataFrame(resource_data)
        
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Resource_Availability', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Resource_Availability']
            
            # Add formatting
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # Apply header formatting
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Set column widths
            for col_num, value in enumerate(df.columns.values):
                max_length = max(len(str(value)), 
                               df[value].astype(str).str.len().max())
                worksheet.set_column(col_num, col_num, max_length + 2)
        
        print(f"Resource availability template created: {output_path}")
        return df
    
    def create_external_costs_template(self, output_path):
        """Create external costs template based on CASES study adaptation"""
        
        external_costs_data = {
            'Emission_Type': ['CO2', 'NOx', 'SO2', 'PM10', 'PM2.5'],
            'Unit_Cost_USD_kg': [0, 0, 0, 0, 0],  # Placeholder values
            'Scaling_Factor_Pakistan': [19.0, 19.0, 19.0, 19.0, 19.0],
            'Adjusted_Cost_USD_kg': [0, 0, 0, 0, 0],  # Placeholder values
            'Source': ['CASES Study', 'CASES Study', 'CASES Study', 'CASES Study', 'CASES Study']
        }
        
        df = pd.DataFrame(external_costs_data)
        
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='External_Costs', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['External_Costs']
            
            # Add formatting
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            # Apply header formatting
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Set column widths
            for col_num, value in enumerate(df.columns.values):
                max_length = max(len(str(value)), 
                               df[value].astype(str).str.len().max())
                worksheet.set_column(col_num, col_num, max_length + 2)
        
        print(f"External costs template created: {output_path}")
        return df
    
    def create_all_templates(self, output_dir):
        """Create all input templates"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        self.create_technology_template(f"{output_dir}/technologies.xlsx")
        self.create_demand_template(f"{output_dir}/demand_forecast.xlsx")
        self.create_resource_template(f"{output_dir}/resources.xlsx")
        self.create_external_costs_template(f"{output_dir}/external_costs.xlsx")
        
        print("All templates created successfully!")

if __name__ == "__main__":
    generator = ExcelTemplateGenerator()
    generator.create_all_templates("data/input/")
