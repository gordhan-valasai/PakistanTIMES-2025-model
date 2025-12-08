"""
PakistanTIMES Core Optimization Model
Implements the TIMES framework for least-cost power generation planning
Based on Chapter 6 equations and methodology from the thesis
"""

import pulp
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from config.config import STUDY_PERIOD, ECONOMIC_PARAMS, EXTERNAL_COST_SCALING

class PakistanTIMESModel:
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.time_horizon = STUDY_PERIOD['years']
        self.base_year = STUDY_PERIOD['base_year']
        self.discount_rate = ECONOMIC_PARAMS['discount_rate']
        self.external_cost_scaling = EXTERNAL_COST_SCALING
        
        # Model components
        self.model = None
        self.decision_vars = {}
        self.constraints = {}
        self.results = {}
        
        # Data storage
        self.technology_data = None
        self.demand_data = None
        self.resource_data = None
        self.external_costs = None
        
    def set_data(self, technology_data: pd.DataFrame, demand_data: pd.DataFrame,
                 resource_data: pd.DataFrame, external_costs: pd.DataFrame):
        """Set input data for the model"""
        self.technology_data = technology_data
        self.demand_data = demand_data
        self.resource_data = resource_data
        self.external_costs = external_costs
        
    def create_optimization_model(self, scenario_name: str) -> pulp.LpProblem:
        """Create PULP optimization model for the given scenario"""
        
        # Create the optimization problem
        self.model = pulp.LpProblem(f"Pakistan_Power_Generation_{scenario_name}", 
                                   pulp.LpMinimize)
        
        # Create decision variables
        self._create_decision_variables()
        
        # Create objective function
        self._create_objective_function()
        
        # Create constraints
        self._create_constraints(scenario_name)
        
        return self.model
    
    def _create_decision_variables(self):
        """Create decision variables as per Chapter 6.4.12"""
        
        # New capacity installation (NCAP) - MW
        self.decision_vars['new_capacity'] = {}
        for tech in self.technology_data.index:
            for year in self.time_horizon:
                var_name = f"NCAP_{tech}_{year}"
                self.decision_vars['new_capacity'][(tech, year)] = pulp.LpVariable(
                    var_name, lowBound=0, cat='Continuous'
                )
        
        # Activity level (ACT) - GWh
        self.decision_vars['generation'] = {}
        for tech in self.technology_data.index:
            for year in self.time_horizon:
                var_name = f"ACT_{tech}_{year}"
                self.decision_vars['generation'][(tech, year)] = pulp.LpVariable(
                    var_name, lowBound=0, cat='Continuous'
                )
        
        # Commodity flows (FLOW) - PJ
        self.decision_vars['fuel_consumption'] = {}
        for tech in self.technology_data.index:
            for year in self.time_horizon:
                var_name = f"FLOW_{tech}_{year}"
                self.decision_vars['fuel_consumption'][(tech, year)] = pulp.LpVariable(
                    var_name, lowBound=0, cat='Continuous'
                )
    
    def _create_objective_function(self):
        """Create objective function based on Equation 6.1 from Chapter 6"""
        
        total_cost = 0
        
        for year in self.time_horizon:
            # Discount factor
            discount_factor = (1 + self.discount_rate) ** (self.base_year - year)
            
            # Investment costs (INVCOST)
            investment_cost = self._calculate_investment_costs(year)
            
            # Fixed costs (FIXCOST)
            fixed_cost = self._calculate_fixed_costs(year)
            
            # Variable costs (VARCOST)
            variable_cost = self._calculate_variable_costs(year)
            
            # External costs
            external_cost = self._calculate_external_costs(year)
            
            # Annual total cost
            annual_cost = (investment_cost + fixed_cost + variable_cost + external_cost)
            
            # Add to total with discounting
            total_cost += discount_factor * annual_cost
        
        # Set objective function
        self.model += total_cost
    
    def _calculate_investment_costs(self, year: int) -> pulp.LpAffineExpression:
        """Calculate investment costs based on conditions 1-4 from Chapter 6"""
        
        investment_cost = 0
        
        for tech in self.technology_data.index:
            capital_cost = self.technology_data.loc[tech, 'Capital_Cost_USD_MW']
            new_capacity = self.decision_vars['new_capacity'][(tech, year)]
            
            # Investment cost is capital cost per MW times capacity in MW
            investment_cost += capital_cost * new_capacity
        
        return investment_cost
    
    def _calculate_fixed_costs(self, year: int) -> pulp.LpAffineExpression:
        """Calculate fixed O&M costs based on Equations 6.8-6.11"""
        
        fixed_cost = 0
        
        for tech in self.technology_data.index:
            fom_cost = self.technology_data.loc[tech, 'FOM_Cost_USD_MW']
            
            # Total capacity in the year (existing + new)
            total_capacity = self._get_total_capacity(tech, year)
            
            fixed_cost += fom_cost * total_capacity
        
        return fixed_cost
    
    def _calculate_variable_costs(self, year: int) -> pulp.LpAffineExpression:
        """Calculate variable operational costs"""
        
        variable_cost = 0
        
        for tech in self.technology_data.index:
            var_cost = self.technology_data.loc[tech, 'Variable_Cost_USD_MWh']
            generation = self.decision_vars['generation'][(tech, year)]
            
            variable_cost += var_cost * generation
        
        return variable_cost
    
    def _calculate_external_costs(self, year: int) -> pulp.LpAffineExpression:
        """Calculate environmental external costs using scaled values"""
        
        external_cost = 0
        
        for tech in self.technology_data.index:
            # Get emission factors
            co2_factor = self.technology_data.loc[tech, 'CO2_Emission_kg_MWh']
            nox_factor = self.technology_data.loc[tech, 'NOx_Emission_kg_MWh']
            so2_factor = self.technology_data.loc[tech, 'SO2_Emission_kg_MWh']
            
            # Get external cost rates
            co2_cost = self.external_costs.loc['CO2', 'Adjusted_Cost_USD_kg']
            nox_cost = self.external_costs.loc['NOx', 'Adjusted_Cost_USD_kg']
            so2_cost = self.external_costs.loc['SO2', 'Adjusted_Cost_USD_kg']
            
            # Calculate emissions
            generation = self.decision_vars['generation'][(tech, year)]
            co2_emissions = co2_factor * generation
            nox_emissions = nox_factor * generation
            so2_emissions = so2_factor * generation
            
            # Calculate external costs
            tech_external_cost = (co2_emissions * co2_cost + 
                                nox_emissions * nox_cost + 
                                so2_emissions * so2_cost)
            
            external_cost += tech_external_cost
        
        return external_cost
    
    def _get_total_capacity(self, tech: str, year: int) -> pulp.LpAffineExpression:
        """Get total capacity for a technology in a given year"""
        
        # Start with base year capacity (always include this)
        total_capacity = 0
        if hasattr(self, 'base_year_capacity') and tech in self.base_year_capacity:
            total_capacity = self.base_year_capacity[tech]
        
        # Add new capacity from base year up to current year (inclusive)
        for prev_year in range(self.base_year, year + 1):
            if (tech, prev_year) in self.decision_vars['new_capacity']:
                total_capacity += self.decision_vars['new_capacity'][(tech, prev_year)]
        
        return total_capacity
    
    def _create_constraints(self, scenario_name: str):
        """Create all model constraints - ENHANCED IMPLEMENTATION"""
        
        print(f"🔧 Creating constraints for scenario: {scenario_name}")
        
        # Basic system constraints
        self._create_demand_constraints()
        self._create_technology_constraints()
        self._create_resource_constraints()
        
        # Scenario-specific constraints
        self._create_scenario_specific_constraints(scenario_name)
        
        print(f"✅ All constraints created for {scenario_name}")
        print(f"📊 Total constraints: {len(self.constraints)}")
    
    def _create_demand_constraints(self):
        """Create demand satisfaction constraints"""
        
        for year in self.time_horizon:
            # Get demand for the year (using BAU scenario for now)
            demand = self.demand_data.loc[year, 'BAU_GWh']
            
            # Total generation must equal demand
            total_generation = 0
            for tech in self.technology_data.index:
                total_generation += self.decision_vars['generation'][(tech, year)]
            
            # Add constraint
            constraint_name = f"Demand_{year}"
            self.constraints[constraint_name] = total_generation == demand
            
            self.model += self.constraints[constraint_name], constraint_name
    
    def _create_resource_constraints(self):
        """Create resource availability constraints"""
        
        # Add realistic resource potential limits based on Pakistan's actual potential
        # These reflect practical deployment constraints, not just technical potential
        resource_limits = {
            'HYDRO': 15000,      # MW - realistic large hydro by 2033 (slower development)
            'HYDRUNOF': 5000,    # MW - limited run-of-river development
            'WIND_A': 3000,      # MW - realistic wind deployment by 2033
            'SOLARE': 5000,      # MW - realistic solar deployment by 2033 
            'NUCFUEL': 3000,     # MW - realistic nuclear by 2033 (delays)
        }
        
        # Apply resource limits to total capacity (base + new)
        for tech, max_capacity in resource_limits.items():
            if tech in self.technology_data.index:
                for year in self.time_horizon:
                    total_capacity = self._get_total_capacity(tech, year)
                    constraint_name = f"ResourceLimit_{tech}_{year}"
                    self.constraints[constraint_name] = total_capacity <= max_capacity
                    self.model += self.constraints[constraint_name], constraint_name
        
        for year in self.time_horizon:
            for tech in self.technology_data.index:
                # Get fuel consumption
                fuel_consumption = self.decision_vars['fuel_consumption'][(tech, year)]
                
                # Get generation
                generation = self.decision_vars['generation'][(tech, year)]
                
                # Efficiency constraint
                efficiency = self.technology_data.loc[tech, 'Efficiency_%'] / 100
                if efficiency > 0:
                    constraint_name = f"Efficiency_{tech}_{year}"
                    self.constraints[constraint_name] = fuel_consumption == generation / efficiency
                    self.model += self.constraints[constraint_name], constraint_name
    
    def _create_technology_constraints(self):
        """Create technology-specific constraints"""
        
        for year in self.time_horizon:
            for tech in self.technology_data.index:
                # Generation cannot exceed capacity
                generation = self.decision_vars['generation'][(tech, year)]
                total_capacity = self._get_total_capacity(tech, year)
                
                # Convert capacity to generation potential (in GWh)
                capacity_factor = self.technology_data.loc[tech, 'Capacity_Factor_%'] / 100
                max_generation = total_capacity * 8760 * capacity_factor / 1000  # Convert MWh to GWh
                
                constraint_name = f"Capacity_{tech}_{year}"
                self.constraints[constraint_name] = generation <= max_generation
                self.model += self.constraints[constraint_name], constraint_name
    
    def _create_scenario_specific_constraints(self, scenario_name: str):
        """Create scenario-specific constraints - ENHANCED IMPLEMENTATION"""
        
        print(f"🔧 Creating scenario-specific constraints for {scenario_name}")
        
        if scenario_name == 'BASE':
            # Base scenario: no additional constraints
            print("  📊 BASE scenario: No additional constraints")
            
        elif 'CEC' in scenario_name:
            # Carbon emission cap constraints
            self._create_emission_cap_constraints(scenario_name)
            
        elif 'REN' in scenario_name:
            # Renewable energy target constraints
            self._create_renewable_target_constraints(scenario_name)
            
        elif scenario_name == 'COALMAX':
            # Maximum indigenous coal constraints
            self._create_coal_maximization_constraints()
            
        else:
            print(f"  ⚠️  Unknown scenario: {scenario_name}")
    
    def _create_emission_cap_constraints(self, scenario_name: str):
        """Create carbon emission cap constraints"""
        
        # Extract emission cap percentage
        if 'CEC10' in scenario_name:
            emission_cap = 0.10  # 10% reduction
        elif 'CEC20' in scenario_name:
            emission_cap = 0.20  # 20% reduction
        else:
            emission_cap = 0.0
        
        # Calculate base year emissions
        base_emissions = self._calculate_base_year_emissions()
        
        # Apply emission cap to each year
        for year in self.time_horizon:
            if year > self.base_year:
                total_emissions = 0
                
                for tech in self.technology_data.index:
                    co2_factor = self.technology_data.loc[tech, 'CO2_Emission_kg_MWh']
                    generation = self.decision_vars['generation'][(tech, year)]
                    total_emissions += co2_factor * generation
                
                # Emission cap constraint
                max_emissions = base_emissions * (1 - emission_cap)
                constraint_name = f"EmissionCap_{year}"
                self.constraints[constraint_name] = total_emissions <= max_emissions
                self.model += self.constraints[constraint_name], constraint_name
    
    def _create_renewable_target_constraints(self, scenario_name: str):
        """Create renewable energy target constraints - FIXED IMPLEMENTATION"""
        
        print(f"🔧 Creating renewable target constraints for {scenario_name}")
        
        # Extract renewable target percentage
        if 'REN50' in scenario_name:
            renewable_target = 0.50  # 50% renewable
            print(f"🎯 Setting renewable target: {renewable_target * 100}%")
        elif 'REN60' in scenario_name:
            renewable_target = 0.60  # 60% renewable
            print(f"🎯 Setting renewable target: {renewable_target * 100}%")
        else:
            renewable_target = 0.0
            print(f"🎯 No renewable target for {scenario_name}")
        
        if renewable_target > 0:
            # Define renewable technologies
            renewable_techs = ['HYDRO', 'HYDRUNOF', 'SOLARE', 'WIND_A', 'BIOMC', 'BAGAS']
            
            # Create renewable target constraints for each year
            for year in self.time_horizon:
                if year > self.base_year:  # Apply constraints for future years
                    
                    # Total generation in the year
                    total_generation = 0
                    for tech in self.technology_data.index:
                        total_generation += self.decision_vars['generation'][(tech, year)]
                    
                    # Renewable generation in the year
                    renewable_generation = 0
                    for tech in renewable_techs:
                        if tech in self.technology_data.index:
                            renewable_generation += self.decision_vars['generation'][(tech, year)]
                    
                    # Renewable target constraint: renewable_gen >= target * total_gen
                    constraint_name = f"RenewableTarget_{year}"
                    min_renewable = renewable_target * total_generation
                    
                    # Create the constraint: renewable_generation >= min_renewable
                    self.constraints[constraint_name] = renewable_generation >= min_renewable
                    self.model += self.constraints[constraint_name], constraint_name
                    
                    print(f"  📅 Year {year}: Renewable >= {renewable_target * 100}% of total generation")
            
            # Add capacity constraints to ensure renewable technologies can meet targets
            self._create_renewable_capacity_constraints(renewable_target)
            
            # Add fossil fuel reduction constraints
            self._create_fossil_fuel_reduction_constraints(renewable_target)
    
    def _create_renewable_capacity_constraints(self, renewable_target: float):
        """Create constraints to ensure sufficient renewable capacity"""
        
        print(f"🔧 Creating renewable capacity constraints for {renewable_target * 100}% target")
        
        renewable_techs = ['HYDRO', 'HYDRUNOF', 'SOLARE', 'WIND_A', 'BIOMC', 'BAGAS']
        
        for year in self.time_horizon:
            if year > self.base_year:
                
                # Calculate required renewable capacity based on target
                # Assume average capacity factor for renewables
                avg_renewable_cf = 0.35  # 35% average capacity factor
                hours_per_year = 8760
                
                # Get demand for the year
                year_demand = self.demand_data.loc[year, 'BAU_GWh'] if year in self.demand_data.index else 0
                
                # Required renewable capacity to meet target
                required_renewable_capacity = (year_demand * renewable_target * 1000) / (avg_renewable_cf * hours_per_year)
                
                # Total renewable capacity (existing + new)
                total_renewable_capacity = 0
                for tech in renewable_techs:
                    if tech in self.technology_data.index:
                        # Base year capacity
                        base_capacity = self.technology_data.loc[tech, 'Base_Capacity_MW'] if 'Base_Capacity_MW' in self.technology_data.columns else 0
                        
                        # New capacity from base year to current year
                        new_capacity = 0
                        for prev_year in range(self.base_year, year + 1):
                            if (tech, prev_year) in self.decision_vars['new_capacity']:
                                new_capacity += self.decision_vars['new_capacity'][(tech, prev_year)]
                        
                        total_renewable_capacity += base_capacity + new_capacity
                
                # Constraint: total renewable capacity >= required capacity
                constraint_name = f"RenewableCapacity_{year}"
                self.constraints[constraint_name] = total_renewable_capacity >= required_renewable_capacity
                self.model += self.constraints[constraint_name], constraint_name
                
                print(f"  📅 Year {year}: Required renewable capacity: {required_renewable_capacity:.0f} MW")
    
    def _create_fossil_fuel_reduction_constraints(self, renewable_target: float):
        """Create constraints to reduce fossil fuel generation"""
        
        print(f"🔧 Creating fossil fuel reduction constraints for {renewable_target * 100}% renewable target")
        
        fossil_techs = ['HCOAL', 'LIGIN', 'NGCC', 'NGTOC', 'OILFUR']
        
        for year in self.time_horizon:
            if year > self.base_year:
                
                # Get demand for the year
                year_demand = self.demand_data.loc[year, 'BAU_GWh'] if year in self.demand_data.index else 0
                
                # Maximum fossil fuel generation (1 - renewable_target)
                max_fossil_generation = year_demand * (1 - renewable_target)
                
                # Total fossil fuel generation
                total_fossil_generation = 0
                for tech in fossil_techs:
                    if tech in self.technology_data.index:
                        total_fossil_generation += self.decision_vars['generation'][(tech, year)]
                
                # Constraint: fossil generation <= max_fossil_generation
                constraint_name = f"FossilFuelLimit_{year}"
                self.constraints[constraint_name] = total_fossil_generation <= max_fossil_generation
                self.model += self.constraints[constraint_name], constraint_name
                
                print(f"  📅 Year {year}: Max fossil generation: {max_fossil_generation:.2f} GWh")
    
    def _create_coal_maximization_constraints(self):
        """Create maximum indigenous coal constraints"""
        
        # This would implement constraints to maximize use of indigenous coal
        # For now, placeholder implementation
        pass
    
    def _calculate_base_year_emissions(self) -> float:
        """Calculate base year emissions for reference"""
        
        base_emissions = 0
        
        for tech in self.technology_data.index:
            co2_factor = self.technology_data.loc[tech, 'CO2_Emission_kg_MWh']
            # This would use actual base year generation data
            # For now, using placeholder
            base_generation = 0
            base_emissions += co2_factor * base_generation
        
        return base_emissions
    
    def solve(self) -> bool:
        """Solve the optimization model"""
        
        if self.model is None:
            raise ValueError("Model not created. Call create_optimization_model first.")
        
        print("Solving optimization model...")
        
        # Solve the model
        status = self.model.solve()
        
        if status == pulp.LpStatusOptimal:
            print("Model solved successfully!")
            self._extract_results()
            return True
        else:
            print(f"Model solution failed with status: {pulp.LpStatus[status]}")
            return False
    
    def _extract_results(self):
        """Extract results from the solved model"""
        
        self.results = {
            'objective_value': pulp.value(self.model.objective),
            'new_capacity': {},
            'generation': {},
            'fuel_consumption': {}
        }
        
        # Extract decision variable values
        for (tech, year), var in self.decision_vars['new_capacity'].items():
            self.results['new_capacity'][(tech, year)] = pulp.value(var)
        
        for (tech, year), var in self.decision_vars['generation'].items():
            self.results['generation'][(tech, year)] = pulp.value(var)
        
        for (tech, year), var in self.decision_vars['fuel_consumption'].items():
            self.results['fuel_consumption'][(tech, year)] = pulp.value(var)
    
    def get_results(self) -> Dict:
        """Get model results"""
        return self.results
    
    def export_results_to_csv(self, output_path: str):
        """Export results to CSV format"""
        
        # Create results DataFrame
        results_data = []
        
        for (tech, year) in self.results['generation'].keys():
            row = {
                'Technology': tech,
                'Year': year,
                'New_Capacity_MW': self.results['new_capacity'].get((tech, year), 0),
                'Generation_GWh': self.results['generation'].get((tech, year), 0),
                'Fuel_Consumption_PJ': self.results['fuel_consumption'].get((tech, year), 0)
            }
            results_data.append(row)
        
        df = pd.DataFrame(results_data)
        df.to_csv(output_path, index=False)
        print(f"Results exported to: {output_path}")
