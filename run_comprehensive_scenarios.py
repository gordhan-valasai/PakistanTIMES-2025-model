#!/usr/bin/env python3
"""
Comprehensive Scenario Runner for PakistanTIMES 2025 Model
========================================================

Runs each REN scenario against 4 demand scenarios:
- REN30, REN50, REN60, REN70 (Renewable Energy Targets)
- BAU, HEG, LEG, MEG (Demand Forecasts)

Creates a complete analysis matrix with all combinations.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ComprehensiveScenarioRunner:
    def __init__(self):
        self.base_year = 2014
        self.study_years = list(range(2014, 2051))
        self.renewable_scenarios = ['REN30', 'REN50', 'REN60', 'REN70']
        self.demand_scenarios = ['BAU', 'HEG', 'LEG', 'MEG']
        
        # Results storage
        self.scenario_results = {}
        self.comparison_matrix = {}
        
        # Create output directory
        self.output_dir = f"comprehensive_scenario_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_input_data(self):
        """Load all input data files"""
        print("📊 Loading input data...")
        
        try:
            # Load demand forecasts
            self.demand_data = pd.read_excel('data/input/demand_forecast_extended_2025_2050.xlsx')
            print(f"✅ Loaded demand data: {self.demand_data.shape}")
            
            # Load technology costs
            self.tech_costs = pd.read_excel('data/input/technology_costs_extended_2025_2050.xlsx')
            print(f"✅ Loaded technology costs: {self.tech_costs.shape}")
            
            # Load carbon calculations
            self.carbon_data = pd.read_excel('data/input/corrected_carbon_calculations_2025_2050.xlsx')
            print(f"✅ Loaded carbon data: {self.carbon_data.shape}")
            
            # Load investment profiles
            self.investment_data = pd.read_excel('data/input/corrected_investment_profiles_2025_2050.xlsx')
            print(f"✅ Loaded investment data: {self.investment_data.shape}")
            
            # Load emission factors
            self.emission_factors = pd.read_excel('data/input/emission_factors_corrected.xlsx')
            print(f"✅ Loaded emission factors: {self.emission_factors.shape}")
            
            # Load external costs
            self.external_costs = pd.read_excel('data/input/external_costs.xlsx')
            print(f"✅ Loaded external costs: {self.external_costs.shape}")
            
            # Load resources
            self.resources = pd.read_excel('data/input/resources.xlsx')
            print(f"✅ Loaded resources: {self.resources.shape}")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
        
        return True
    
    def prepare_demand_scenarios(self):
        """Prepare demand data for each scenario"""
        print("📈 Preparing demand scenarios...")
        
        self.demand_scenarios_data = {}
        
        for scenario in self.demand_scenarios:
            column_name = scenario + '_GWh'
            if column_name in self.demand_data.columns:
                scenario_data = self.demand_data[['Unnamed: 0', column_name]].copy()
                scenario_data.columns = ['Year', 'Demand_GWh']
                scenario_data = scenario_data.dropna()
                self.demand_scenarios_data[scenario] = scenario_data
                print(f"✅ {scenario}: {len(scenario_data)} years of data")
        
        return True
    
    def run_single_scenario(self, ren_scenario: str, demand_scenario: str):
        """Run a single scenario combination"""
        
        scenario_name = f"{ren_scenario}_{demand_scenario}"
        print(f"\n🚀 Running scenario: {scenario_name}")
        
        try:
            # Extract renewable target from REN scenario
            if 'REN30' in ren_scenario:
                renewable_target = 0.30
            elif 'REN50' in ren_scenario:
                renewable_target = 0.50
            elif 'REN60' in ren_scenario:
                renewable_target = 0.60
            elif 'REN70' in ren_scenario:
                renewable_target = 0.70
            else:
                renewable_target = 0.30
            
            # Get demand data for this scenario
            demand_data = self.demand_scenarios_data[demand_scenario]
            
            # Run simplified model simulation
            results = self._simulate_scenario(ren_scenario, demand_scenario, renewable_target, demand_data)
            
            # Store results
            self.scenario_results[scenario_name] = results
            
            print(f"✅ Completed {scenario_name}")
            return results
            
        except Exception as e:
            print(f"❌ Error in scenario {scenario_name}: {e}")
            return None
    
    def _simulate_scenario(self, ren_scenario: str, demand_scenario: str, renewable_target: float, demand_data: pd.DataFrame):
        """Simulate a scenario using simplified calculations"""
        
        results = {
            'scenario_name': f"{ren_scenario}_{demand_scenario}",
            'renewable_target': renewable_target,
            'demand_scenario': demand_scenario,
            'years': demand_data['Year'].tolist(),
            'demand_gwh': demand_data['Demand_GWh'].tolist(),
            'renewable_generation': [],
            'fossil_generation': [],
            'total_generation': [],
            'renewable_share': [],
            'emissions_mtco2': [],
            'total_cost_million_usd': [],
            'capacity_additions': {}
        }
        
        # Technology mix assumptions
        renewable_techs = ['HYDRO', 'HYDRUNOF', 'SOLARE', 'WIND_A', 'BIOMC', 'BAGAS']
        fossil_techs = ['HCOAL', 'NGCC', 'NUCFUEL']
        
        # Base year capacity (simplified)
        base_capacity = {
            'HYDRO': 7000, 'HYDRUNOF': 2000, 'SOLARE': 1000, 'WIND_A': 500,
            'BIOMC': 300, 'BAGAS': 800, 'HCOAL': 5000, 'NGCC': 8000, 'NUCFUEL': 1000
        }
        
        # Technology costs (simplified)
        tech_costs = {
            'SOLARE': 800, 'WIND_A': 1200, 'HYDRO': 2000, 'BIOMC': 1500,
            'HCOAL': 1500, 'NGCC': 1000, 'NUCFUEL': 5000
        }
        
        # Emission factors (kg CO2/MWh)
        emission_factors = {
            'HYDRO': 0, 'HYDRUNOF': 0, 'SOLARE': 0, 'WIND_A': 0, 'BIOMC': 900, 'BAGAS': 800,
            'HCOAL': 950, 'NGCC': 400, 'NUCFUEL': 0
        }
        
        current_capacity = base_capacity.copy()
        
        for i, year in enumerate(results['years']):
            demand = results['demand_gwh'][i]
            
            # Calculate required generation (with 15% reserve margin)
            required_generation = demand * 1.15
            
            # Calculate renewable generation based on target
            renewable_generation = required_generation * renewable_target
            fossil_generation = required_generation - renewable_generation
            
            # Calculate capacity additions for renewables
            renewable_capacity_needed = renewable_generation / (8760 * 0.25)  # 25% capacity factor
            
            # Add new renewable capacity
            for tech in renewable_techs:
                if tech in current_capacity:
                    additional_capacity = max(0, renewable_capacity_needed * 0.2)  # 20% of each tech
                    current_capacity[tech] += additional_capacity
                    
                    if tech not in results['capacity_additions']:
                        results['capacity_additions'][tech] = []
                    results['capacity_additions'][tech].append(additional_capacity)
            
            # Calculate emissions
            emissions = 0
            for tech in fossil_techs:
                if tech in current_capacity:
                    tech_generation = fossil_generation * 0.4  # 40% of fossil generation
                    emissions += tech_generation * emission_factors[tech] / 1000  # Convert to Mt CO2
            
            # Calculate costs
            total_cost = 0
            for tech in renewable_techs:
                if tech in current_capacity and tech in tech_costs:
                    additional_capacity = results['capacity_additions'].get(tech, [0])[-1] if results['capacity_additions'].get(tech) else 0
                    total_cost += additional_capacity * tech_costs[tech] / 1000000  # Convert to million USD
            
            # Store results
            results['renewable_generation'].append(renewable_generation)
            results['fossil_generation'].append(fossil_generation)
            results['total_generation'].append(required_generation)
            results['renewable_share'].append(renewable_target * 100)
            results['emissions_mtco2'].append(emissions)
            results['total_cost_million_usd'].append(total_cost)
        
        return results
    
    def run_all_scenarios(self):
        """Run all scenario combinations"""
        print(f"\n🎯 Running all {len(self.renewable_scenarios)} x {len(self.demand_scenarios)} = {len(self.renewable_scenarios) * len(self.demand_scenarios)} scenarios")
        print("=" * 80)
        
        for ren_scenario in self.renewable_scenarios:
            for demand_scenario in self.demand_scenarios:
                self.run_single_scenario(ren_scenario, demand_scenario)
        
        print(f"\n✅ All scenarios completed!")
    
    def create_comparison_matrix(self):
        """Create a comprehensive comparison matrix"""
        print("\n📊 Creating comparison matrix...")
        
        # Create summary DataFrame
        summary_data = []
        
        for scenario_name, results in self.scenario_results.items():
            if results:
                # Calculate key metrics
                avg_renewable_share = np.mean(results['renewable_share'])
                total_emissions = sum(results['emissions_mtco2'])
                total_cost = sum(results['total_cost_million_usd'])
                final_demand = results['demand_gwh'][-1]
                
                summary_data.append({
                    'Scenario': scenario_name,
                    'Renewable_Target_%': results['renewable_target'] * 100,
                    'Demand_Scenario': results['demand_scenario'],
                    'Avg_Renewable_Share_%': round(avg_renewable_share, 1),
                    'Total_Emissions_MtCO2': round(total_emissions, 1),
                    'Total_Investment_Million_USD': round(total_cost, 1),
                    'Final_Demand_2050_GWh': round(final_demand, 0),
                    'Emissions_Reduction_vs_BAU_%': 0  # Will calculate below
                })
        
        self.summary_df = pd.DataFrame(summary_data)
        
        # Calculate emissions reduction vs BAU
        bau_emissions = {}
        for _, row in self.summary_df.iterrows():
            if 'BAU' in row['Demand_Scenario']:
                bau_emissions[row['Renewable_Target_%']] = row['Total_Emissions_MtCO2']
        
        for i, row in self.summary_df.iterrows():
            if row['Renewable_Target_%'] in bau_emissions:
                bau_emission = bau_emissions[row['Renewable_Target_%']]
                reduction = ((bau_emission - row['Total_Emissions_MtCO2']) / bau_emission) * 100
                self.summary_df.at[i, 'Emissions_Reduction_vs_BAU_%'] = round(reduction, 1)
        
        print("✅ Comparison matrix created")
        return self.summary_df
    
    def export_results(self):
        """Export all results to files"""
        print("\n💾 Exporting results...")
        
        # Export summary matrix
        summary_path = os.path.join(self.output_dir, 'comprehensive_scenario_summary.xlsx')
        self.summary_df.to_excel(summary_path, index=False)
        print(f"✅ Summary exported to: {summary_path}")
        
        # Export detailed results for each scenario
        for scenario_name, results in self.scenario_results.items():
            if results:
                # Create detailed results DataFrame
                detailed_data = []
                for i, year in enumerate(results['years']):
                    row = {
                        'Year': year,
                        'Demand_GWh': results['demand_gwh'][i],
                        'Renewable_Generation_GWh': results['renewable_generation'][i],
                        'Fossil_Generation_GWh': results['fossil_generation'][i],
                        'Total_Generation_GWh': results['total_generation'][i],
                        'Renewable_Share_%': results['renewable_share'][i],
                        'Emissions_MtCO2': results['emissions_mtco2'][i],
                        'Investment_Million_USD': results['total_cost_million_usd'][i]
                    }
                    detailed_data.append(row)
                
                detailed_df = pd.DataFrame(detailed_data)
                detailed_path = os.path.join(self.output_dir, f'{scenario_name}_detailed_results.xlsx')
                detailed_df.to_excel(detailed_path, index=False)
                print(f"✅ {scenario_name} detailed results exported")
        
        # Export capacity additions
        capacity_data = []
        for scenario_name, results in self.scenario_results.items():
            if results and 'capacity_additions' in results:
                for tech, additions in results['capacity_additions'].items():
                    for i, addition in enumerate(additions):
                        if i < len(results['years']):
                            capacity_data.append({
                                'Scenario': scenario_name,
                                'Technology': tech,
                                'Year': results['years'][i],
                                'Capacity_Addition_MW': addition
                            })
        
        if capacity_data:
            capacity_df = pd.DataFrame(capacity_data)
            capacity_path = os.path.join(self.output_dir, 'capacity_additions_all_scenarios.xlsx')
            capacity_df.to_excel(capacity_path, index=False)
            print(f"✅ Capacity additions exported to: {capacity_path}")
        
        print(f"\n📁 All results exported to: {self.output_dir}")
    
    def generate_analysis_report(self):
        """Generate a comprehensive analysis report"""
        print("\n📋 Generating analysis report...")
        
        report_path = os.path.join(self.output_dir, 'comprehensive_analysis_report.txt')
        
        with open(report_path, 'w') as f:
            f.write("COMPREHENSIVE SCENARIO ANALYSIS REPORT\n")
            f.write("=====================================\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Scenarios: {len(self.scenario_results)}\n\n")
            
            f.write("SCENARIO MATRIX:\n")
            f.write("-" * 50 + "\n")
            f.write("Renewable Scenarios: " + ", ".join(self.renewable_scenarios) + "\n")
            f.write("Demand Scenarios: " + ", ".join(self.demand_scenarios) + "\n\n")
            
            f.write("KEY FINDINGS:\n")
            f.write("-" * 50 + "\n")
            
            # Find best performing scenarios
            if not self.summary_df.empty:
                best_emissions = self.summary_df.loc[self.summary_df['Total_Emissions_MtCO2'].idxmin()]
                best_cost = self.summary_df.loc[self.summary_df['Total_Investment_Million_USD'].idxmin()]
                highest_renewable = self.summary_df.loc[self.summary_df['Avg_Renewable_Share_%'].idxmax()]
                
                f.write(f"Lowest Emissions: {best_emissions['Scenario']} ({best_emissions['Total_Emissions_MtCO2']} MtCO2)\n")
                f.write(f"Lowest Investment: {best_cost['Scenario']} (${best_cost['Total_Investment_Million_USD']}M)\n")
                f.write(f"Highest Renewable Share: {highest_renewable['Scenario']} ({highest_renewable['Avg_Renewable_Share_%']}%)\n\n")
            
            f.write("DETAILED RESULTS:\n")
            f.write("-" * 50 + "\n")
            if not self.summary_df.empty:
                f.write(self.summary_df.to_string(index=False))
        
        print(f"✅ Analysis report generated: {report_path}")
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("🚀 Starting Comprehensive PakistanTIMES 2025 Scenario Analysis")
        print("=" * 80)
        
        # Step 1: Load data
        if not self.load_input_data():
            return False
        
        # Step 2: Prepare demand scenarios
        if not self.prepare_demand_scenarios():
            return False
        
        # Step 3: Run all scenarios
        self.run_all_scenarios()
        
        # Step 4: Create comparison matrix
        self.create_comparison_matrix()
        
        # Step 5: Export results
        self.export_results()
        
        # Step 6: Generate report
        self.generate_analysis_report()
        
        print(f"\n🎉 COMPREHENSIVE ANALYSIS COMPLETED!")
        print(f"📁 Results saved in: {self.output_dir}")
        print(f"📊 Total scenarios analyzed: {len(self.scenario_results)}")
        
        return True

if __name__ == "__main__":
    runner = ComprehensiveScenarioRunner()
    runner.run_complete_analysis()
