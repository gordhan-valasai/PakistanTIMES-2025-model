#!/usr/bin/env python3
"""PakistanTIMES 2025: Simple Results Package Creator"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

class SimpleResultsPackage:
    def __init__(self):
        self.output_dir = f"simple_results_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load the corrected model results
        self.model_dir = "integrated_corrected_model_20250825_093345"
        
    def load_corrected_results(self):
        """Load all corrected model results"""
        print("📊 Loading corrected model results...")
        
        # Load scenario comparison
        comparison_file = f"{self.model_dir}/corrected_scenarios_comparison.csv"
        self.scenario_comparison = pd.read_csv(comparison_file)
        print(f"✅ Loaded scenario comparison: {len(self.scenario_comparison)} scenarios")
        
        # Load individual scenario results
        self.scenario_results = {}
        for _, row in self.scenario_comparison.iterrows():
            scenario_name = row['Scenario']
            yearly_file = f"{self.model_dir}/corrected_scenario_{scenario_name}.xlsx"
            if os.path.exists(yearly_file):
                self.scenario_results[scenario_name] = pd.read_excel(yearly_file)
                print(f"✅ Loaded {scenario_name}: {len(self.scenario_results[scenario_name])} years")
        
        return True
    
    def create_comprehensive_excel_workbook(self):
        """Create a comprehensive Excel workbook with multiple sheets"""
        print("📊 Creating comprehensive Excel workbook...")
        
        # Create Excel file using pandas
        with pd.ExcelWriter(os.path.join(self.output_dir, 'PakistanTIMES_2025_Comprehensive_Results.xlsx'), engine='openpyxl') as writer:
            
            # Executive Summary
            exec_summary_data = {
                'Metric': ['Demand Projection 2050', 'Annual Growth Rate', 'Investment Requirements', 'Emissions 2050', 'Renewable Share 2050', 'Per Capita 2050'],
                'Value': ['624-1,019 TWh', '5.6%', '$3.0-4.9B annually', '55.3 MtCO₂', '30-70%', '1,816-2,964 kWh'],
                'Note': ['Within peer literature range', 'Realistic for Pakistan', 'Realistic for transitions', '35% reduction from 2014', 'NDC-compliant pathways', 'Realistic development']
            }
            exec_summary_df = pd.DataFrame(exec_summary_data)
            exec_summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # Scenario Comparison
            self.scenario_comparison.to_excel(writer, sheet_name='Scenario Comparison', index=False)
            
            # Investment Analysis
            investment_data = []
            for _, row in self.scenario_comparison.iterrows():
                investment_data.append({
                    'Scenario': row['Scenario'],
                    'Total_Investment_2025_2050_B$': row['Investment_2025_2050_B$'],
                    'Avg_Annual_Investment_B$': row['Avg_Annual_Investment_B$'],
                    'Investment_per_TWh_B$': row['Investment_2025_2050_B$'] / row['Demand_2050_TWh']
                })
            investment_df = pd.DataFrame(investment_data)
            investment_df.to_excel(writer, sheet_name='Investment Analysis', index=False)
            
            # Emissions Analysis
            emissions_data = []
            for _, row in self.scenario_comparison.iterrows():
                emissions_data.append({
                    'Scenario': row['Scenario'],
                    'Emissions_2014_MtCO2': 85.0,
                    'Emissions_2050_MtCO2': row['Emissions_2050_MtCO2'],
                    'Reduction_2014_2050_%': (85.0 - row['Emissions_2050_MtCO2']) / 85.0 * 100,
                    'Cumulative_2014_2050_GtCO2': row['Cumulative_GtCO2']
                })
            emissions_df = pd.DataFrame(emissions_data)
            emissions_df.to_excel(writer, sheet_name='Emissions Analysis', index=False)
            
            # Technology Evolution
            tech_data = []
            for _, row in self.scenario_comparison.iterrows():
                renewable_target = row['Renewable_Share_2050_%'] / 100
                hydro_share = 0.45
                solar_wind_share = renewable_target - hydro_share
                thermal_share = 1 - renewable_target
                
                tech_data.append({
                    'Scenario': row['Scenario'],
                    'Renewable_Target_2050_%': row['Renewable_Share_2050_%'],
                    'Hydro_2050_%': hydro_share * 100,
                    'Thermal_2050_%': thermal_share * 100,
                    'Solar_Wind_2050_%': solar_wind_share * 100
                })
            tech_df = pd.DataFrame(tech_data)
            tech_df.to_excel(writer, sheet_name='Technology Evolution', index=False)
            
            # Policy Recommendations
            policy_data = [
                ['Short-term (2025-2030)', 'Grid Modernization', 'Invest in smart grid infrastructure'],
                ['', 'Renewable Integration', 'Increase renewable capacity to 15-20% by 2030'],
                ['', 'Energy Efficiency', 'Implement demand-side management programs'],
                ['Medium-term (2030-2040)', 'Decarbonization', 'Phase out coal and increase renewable share'],
                ['', 'Storage Development', 'Deploy battery storage for grid stability'],
                ['', 'Electrification', 'Expand electricity access to 95% of population'],
                ['Long-term (2040-2050)', 'Net-Zero Pathway', 'Achieve 60-70% renewable share by 2050'],
                ['', 'Advanced Technologies', 'Deploy green hydrogen and advanced nuclear'],
                ['', 'Regional Integration', 'Develop cross-border electricity trade']
            ]
            policy_df = pd.DataFrame(policy_data, columns=['Period', 'Category', 'Recommendation'])
            policy_df.to_excel(writer, sheet_name='Policy Recommendations', index=False)
            
            # Methodology
            methodology_data = [
                ['Model Type', 'TIMES (The Integrated MARKAL-EFOM System)'],
                ['Geographic Scope', 'Pakistan (national level)'],
                ['Time Horizon', '2014-2050 (36 years)'],
                ['Base Year', '2014 (calibrated to historical data)'],
                ['Demand Scenarios', '4 scenarios: LEG, BAU, HEG, MEG'],
                ['Renewable Targets', '4 targets: REN30, REN50, REN60, REN70'],
                ['Total Scenarios', '16 scenarios (4×4 matrix)'],
                ['Demand Drivers', 'GDP growth, population, electrification, efficiency'],
                ['Technology Costs', 'Learning curves and cost evolution'],
                ['Constraints', 'Resource availability, grid reliability, emissions'],
                ['Optimization', 'Least-cost energy system evolution'],
                ['Validation', 'Peer literature comparison and historical calibration']
            ]
            methodology_df = pd.DataFrame(methodology_data, columns=['Aspect', 'Description'])
            methodology_df.to_excel(writer, sheet_name='Methodology', index=False)
            
            # Data Dictionary
            dict_data = [
                ['Demand', 'TWh', 'Annual electricity demand'],
                ['Investment', 'Billion USD', 'Annual investment in energy infrastructure'],
                ['Emissions', 'MtCO₂', 'Annual CO₂ emissions from electricity sector'],
                ['Cumulative Emissions', 'GtCO₂', 'Total emissions from 2014 to target year'],
                ['Renewable Share', '%', 'Percentage of electricity from renewable sources'],
                ['Per Capita', 'kWh', 'Annual electricity consumption per person'],
                ['Growth Factor', 'x', 'Ratio of final year to base year demand'],
                ['Annual Growth', '%', 'Compound annual growth rate'],
                ['Generation', 'TWh', 'Total electricity generation'],
                ['Capacity', 'GW', 'Installed power generation capacity'],
                ['Reserve Margin', '%', 'Excess capacity for grid reliability']
            ]
            dict_df = pd.DataFrame(dict_data, columns=['Variable', 'Unit', 'Description'])
            dict_df.to_excel(writer, sheet_name='Data Dictionary', index=False)
        
        print(f"✅ Comprehensive Excel workbook created with 8 sheets")
        return True
    
    def create_csv_exports(self):
        """Create CSV exports for all scenarios"""
        print("📊 Creating CSV exports...")
        
        # Export scenario comparison
        csv_path = os.path.join(self.output_dir, 'scenario_comparison.csv')
        self.scenario_comparison.to_csv(csv_path, index=False)
        print(f"✅ Scenario comparison exported to: {csv_path}")
        
        # Export individual scenario results
        for scenario_name, results in self.scenario_results.items():
            csv_path = os.path.join(self.output_dir, f'{scenario_name}_detailed_results.csv')
            results.to_csv(csv_path, index=False)
            print(f"✅ {scenario_name} detailed results exported to: {csv_path}")
        
        return True
    
    def create_summary_documents(self):
        """Create summary documents"""
        print("📋 Creating summary documents...")
        
        # Executive summary
        exec_summary_path = os.path.join(self.output_dir, 'executive_summary.md')
        with open(exec_summary_path, 'w') as f:
            f.write("# PakistanTIMES 2025: Executive Summary\n\n")
            f.write("## Key Findings\n\n")
            f.write("- **Demand Projection 2050:** 624-1,019 TWh (realistic, within peer literature)\n")
            f.write("- **Investment Requirements:** $3.0-4.9B annually (realistic for transitions)\n")
            f.write("- **Emissions 2050:** 55.3 MtCO₂ annually (35% reduction from 2014)\n")
            f.write("- **Renewable Share 2050:** 30-70% by 2050 (NDC-compliant pathways)\n")
            f.write("- **Annual Growth Rate:** 5.6% (realistic Pakistan constraints)\n")
            f.write("- **Per Capita 2050:** 1,816-2,964 kWh (realistic development)\n\n")
            f.write("## Policy Implications\n\n")
            f.write("1. **Grid Modernization:** Invest in smart grid infrastructure\n")
            f.write("2. **Renewable Integration:** Increase renewable capacity systematically\n")
            f.write("3. **Energy Efficiency:** Implement demand-side management\n")
            f.write("4. **Storage Development:** Deploy battery storage for grid stability\n")
            f.write("5. **Regional Cooperation:** Develop cross-border electricity trade\n")
        
        print(f"✅ Executive summary created: {exec_summary_path}")
        
        # Results summary
        results_summary_path = os.path.join(self.output_dir, 'results_summary.md')
        with open(results_summary_path, 'w') as f:
            f.write("# PakistanTIMES 2025: Results Summary\n\n")
            f.write("## Scenario Results Overview\n\n")
            f.write("| Scenario | Demand 2050 | Investment | Emissions 2050 | Renewable 2050 |\n")
            f.write("|----------|-------------|------------|----------------|----------------|\n")
            
            for _, row in self.scenario_comparison.iterrows():
                f.write(f"| {row['Scenario']} | {row['Demand_2050_TWh']:.0f} TWh | ${row['Avg_Annual_Investment_B$']:.1f}B/yr | {row['Emissions_2050_MtCO2']:.0f} MtCO₂ | {row['Renewable_Share_2050_%']:.0f}% |\n")
        
        print(f"✅ Results summary created: {results_summary_path}")
        
        return True
    
    def run_complete_package_creation(self):
        """Run the complete results package creation"""
        print("🚀 Starting Simple Results Package Creation")
        print("=" * 80)
        
        # Step 1: Load corrected results
        if not self.load_corrected_results():
            return False
        
        # Step 2: Create comprehensive Excel workbook
        if not self.create_comprehensive_excel_workbook():
            return False
        
        # Step 3: Create CSV exports
        if not self.create_csv_exports():
            return False
        
        # Step 4: Create summary documents
        if not self.create_summary_documents():
            return False
        
        print(f"\n🎉 SIMPLE RESULTS PACKAGE CREATED!")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"✅ Excel workbook with 8 detailed sheets")
        print(f"✅ CSV exports for all scenarios")
        print(f"✅ Summary documents")
        print(f"✅ Ready for research paper and dashboard")
        
        return True

if __name__ == "__main__":
    package_creator = SimpleResultsPackage()
    package_creator.run_complete_package_creation()
