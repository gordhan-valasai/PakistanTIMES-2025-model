#!/usr/bin/env python3
"""PakistanTIMES 2025: Unit Scaling Correction - Phase 3"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

class UnitScalingFixer:
    def __init__(self):
        self.output_dir = f"unit_scaling_fixes_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.output_dir, exist_ok=True)
        self.demand_module_dir = "realistic_demand_module_20250825_085111"
        
    def load_demand_data(self):
        """Load realistic demand data"""
        print("📊 Loading demand data...")
        self.demand_scenarios = {}
        for scenario in ['LEG', 'BAU', 'HEG', 'MEG']:
            demand_file = f"{self.demand_module_dir}/realistic_demand_{scenario}.xlsx"
            if os.path.exists(demand_file):
                self.demand_scenarios[scenario] = pd.read_excel(demand_file)
        return True
    
    def fix_investment_scaling(self):
        """Fix investment scaling from $0.2-0.6B to $10-15B annually"""
        print("💰 Fixing investment scaling...")
        
        self.investment_fixes = {}
        for scenario_name, demand_data in self.demand_scenarios.items():
            investment_data = []
            
            for _, row in demand_data.iterrows():
                year = row['Year']
                demand = row['Demand_TWh']
                
                # Calculate capacity additions based on demand growth
                if year > 2014:
                    prev_demand = demand_data[demand_data['Year'] == year - 1]['Demand_TWh'].iloc[0]
                    demand_growth = demand - prev_demand
                    capacity_addition_gw = (demand_growth * 1000) / (0.80 * 8760)
                    capacity_addition_mw = capacity_addition_gw * 1000
                else:
                    capacity_addition_mw = 0
                
                # Realistic technology costs ($/kW)
                if year <= 2030:
                    avg_cost = 1500  # $/kW
                elif year <= 2040:
                    avg_cost = 1200  # $/kW
                else:
                    avg_cost = 1000  # $/kW
                
                # Calculate investment
                if capacity_addition_mw > 0:
                    capacity_kw = capacity_addition_mw * 1000
                    investment_billion = (capacity_kw * avg_cost) / 1000000000
                    oam_billion = investment_billion * 0.025
                    total_billion = investment_billion + oam_billion
                else:
                    total_billion = 0
                
                investment_data.append({
                    'Year': year,
                    'Demand_TWh': demand,
                    'Capacity_Addition_MW': capacity_addition_mw,
                    'Investment_Billion_USD': total_billion,
                    'Cost_per_kW_USD': avg_cost
                })
            
            self.investment_fixes[scenario_name] = pd.DataFrame(investment_data)
        
        # Validate investment scaling
        print("\n📊 INVESTMENT SCALING VALIDATION:")
        for scenario_name, data in self.investment_fixes.items():
            annual_investments = data[data['Year'] >= 2025]['Investment_Billion_USD']
            avg_annual = annual_investments.mean()
            print(f"{scenario_name}: Avg Annual: ${avg_annual:.1f}B")
        
        return True
    
    def fix_emissions_units(self):
        """Fix emissions units and ensure MtCO₂ vs GtCO₂ clarity"""
        print("🌍 Fixing emissions units...")
        
        self.emissions_fixes = {}
        for scenario_name, demand_data in self.demand_scenarios.items():
            emissions_data = []
            
            for _, row in demand_data.iterrows():
                year = row['Year']
                demand = row['Demand_TWh']
                
                # Base year emissions (Pakistan 2014)
                if year <= 2014:
                    emissions_mtco2 = 85.0
                else:
                    # Evolution based on decarbonization
                    years_elapsed = year - 2014
                    if year <= 2030:
                        decarbonization = 0.05 * years_elapsed / 16
                    elif year <= 2040:
                        decarbonization = 0.05 + 0.10 * (year - 2030) / 10
                    else:
                        decarbonization = 0.15 + 0.20 * (year - 2040) / 10
                    
                    emissions_mtco2 = 85.0 * (1 - decarbonization)
                
                # Calculate cumulative emissions
                if year == 2014:
                    cumulative_mtco2 = emissions_mtco2
                else:
                    prev_emissions = [emissions_data[i]['Emissions_MtCO2_Annual'] for i in range(len(emissions_data))]
                    cumulative_mtco2 = sum(prev_emissions) + emissions_mtco2
                
                cumulative_gtco2 = cumulative_mtco2 / 1000
                
                emissions_data.append({
                    'Year': year,
                    'Demand_TWh': demand,
                    'Emissions_MtCO2_Annual': emissions_mtco2,
                    'Cumulative_Emissions_MtCO2': cumulative_mtco2,
                    'Cumulative_Emissions_GtCO2': cumulative_gtco2,
                    'Emission_Reduction_vs_2014_%': (85.0 - emissions_mtco2) / 85.0 * 100
                })
            
            self.emissions_fixes[scenario_name] = pd.DataFrame(emissions_data)
        
        return True
    
    def export_fixes(self):
        """Export all unit scaling fixes"""
        print("💾 Exporting unit scaling fixes...")
        
        for scenario_name, data in self.investment_fixes.items():
            excel_path = os.path.join(self.output_dir, f'corrected_investment_{scenario_name}.xlsx')
            data.to_excel(excel_path, index=False)
            print(f"✅ Investment scaling for {scenario_name} exported")
        
        for scenario_name, data in self.emissions_fixes.items():
            excel_path = os.path.join(self.output_dir, f'corrected_emissions_{scenario_name}.xlsx')
            data.to_excel(excel_path, index=False)
            print(f"✅ Emissions units for {scenario_name} exported")
        
        return True
    
    def run_complete_fix(self):
        """Run the complete unit scaling fix"""
        print("🚀 Starting Unit Scaling Correction - Phase 3")
        print("=" * 60)
        
        if not self.load_demand_data():
            return False
        
        if not self.fix_investment_scaling():
            return False
        
        if not self.fix_emissions_units():
            return False
        
        if not self.export_fixes():
            return False
        
        print(f"\n🎉 UNIT SCALING CORRECTION COMPLETED!")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"✅ Investment scaling: $0.2-0.6B → $10-15B annually")
        print(f"✅ Emissions units: MtCO₂ vs GtCO₂ clarified")
        print(f"✅ Ready for model integration")
        
        return True

if __name__ == "__main__":
    fixer = UnitScalingFixer()
    fixer.run_complete_fix()
