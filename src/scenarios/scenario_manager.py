"""
Scenario Manager for PakistanTIMES Model
Manages different modeling scenarios as defined in Table 8.1 of the thesis
"""

import pandas as pd
from typing import Dict, List, Any, Optional
from config.config import MODEL_SCENARIOS, STUDY_PERIOD

class ScenarioManager:
    def __init__(self):
        self.scenarios = MODEL_SCENARIOS
        self.active_scenarios = []
        self.scenario_results = {}
        
    def get_available_scenarios(self) -> List[str]:
        """Get list of available scenarios"""
        return list(self.scenarios.keys())
    
    def get_scenario_description(self, scenario_name: str) -> str:
        """Get description of a specific scenario"""
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario {scenario_name} not found")
        
        return self.scenarios[scenario_name]['description']
    
    def get_scenario_constraints(self, scenario_name: str) -> Dict[str, Any]:
        """Get constraints for a specific scenario"""
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario {scenario_name} not found")
        
        # The constraints are stored directly in the scenario dictionary
        scenario = self.scenarios[scenario_name]
        constraints = {
            'external_costs': scenario.get('external_costs', False),
            'emission_cap': scenario.get('emission_cap', None),
            'renewable_target': scenario.get('renewable_target', None),
            'indigenous_preference': scenario.get('indigenous_preference', False),
            'coal_max': scenario.get('coal_max', False)
        }
        
        return constraints
    
    def validate_scenario(self, scenario_name: str) -> bool:
        """Validate if a scenario is properly configured"""
        if scenario_name not in self.scenarios:
            return False
        
        scenario = self.scenarios[scenario_name]
        required_keys = ['description']
        
        return all(key in scenario for key in required_keys)
    
    def add_custom_scenario(self, name: str, description: str, constraints: Dict[str, Any]):
        """Add a custom scenario to the manager"""
        if name in self.scenarios:
            raise ValueError(f"Scenario {name} already exists")
        
        self.scenarios[name] = {
            'description': description,
            'constraints': constraints
        }
        
        print(f"Custom scenario '{name}' added successfully")
    
    def modify_scenario(self, scenario_name: str, new_constraints: Dict[str, Any]):
        """Modify constraints of an existing scenario"""
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario {scenario_name} not found")
        
        self.scenarios[scenario_name]['constraints'].update(new_constraints)
        print(f"Scenario '{scenario_name}' modified successfully")
    
    def get_scenario_summary(self) -> pd.DataFrame:
        """Get summary of all scenarios"""
        
        summary_data = []
        
        for name, scenario in self.scenarios.items():
            row = {
                'Scenario': name,
                'Description': scenario['description'],
                'External_Costs': scenario.get('external_costs', False),
                'Emission_Cap': scenario.get('emission_cap', 'None'),
                'Renewable_Target': scenario.get('renewable_target', 'None'),
                'Indigenous_Preference': scenario.get('indigenous_preference', False),
                'Coal_Max': scenario.get('coal_max', False)
            }
            
            summary_data.append(row)
        
        return pd.DataFrame(summary_data)
    
    def compare_scenarios(self, scenario_names: List[str]) -> Dict[str, Any]:
        """Compare multiple scenarios"""
        if not scenario_names:
            raise ValueError("No scenarios specified for comparison")
        
        comparison = {
            'scenarios': scenario_names,
            'constraints': {},
            'differences': {}
        }
        
        # Get constraints for each scenario
        for name in scenario_names:
            if name in self.scenarios:
                comparison['constraints'][name] = self.get_scenario_constraints(name)
            else:
                print(f"Warning: Scenario {name} not found")
        
        # Identify key differences
        if len(scenario_names) >= 2:
            comparison['differences'] = self._identify_differences(scenario_names)
        
        return comparison
    
    def _identify_differences(self, scenario_names: List[str]) -> Dict[str, Any]:
        """Identify key differences between scenarios"""
        differences = {}
        
        # Get constraints for all scenarios
        all_constraints = {}
        for name in scenario_names:
            if name in self.scenarios:
                all_constraints[name] = self.get_scenario_constraints(name)
        
        if len(all_constraints) < 2:
            return differences
        
        # Compare external costs
        external_costs_values = [constraints.get('external_costs', False) 
                               for constraints in all_constraints.values()]
        if len(set(external_costs_values)) > 1:
            differences['external_costs'] = {
                'values': dict(zip(all_constraints.keys(), external_costs_values)),
                'description': 'Different external cost inclusion policies'
            }
        
        # Compare emission caps
        emission_caps = [constraints.get('emission_cap', None) 
                        for constraints in all_constraints.values()]
        if len(set(emission_caps)) > 1:
            differences['emission_caps'] = {
                'values': dict(zip(all_constraints.keys(), emission_caps)),
                'description': 'Different carbon emission reduction targets'
            }
        
        # Compare renewable targets
        renewable_targets = [constraints.get('renewable_target', None) 
                           for constraints in all_constraints.values()]
        if len(set(renewable_targets)) > 1:
            differences['renewable_targets'] = {
                'values': dict(zip(all_constraints.keys(), renewable_targets)),
                'description': 'Different renewable energy penetration targets'
            }
        
        # Compare coal maximization
        coal_max_values = [constraints.get('coal_max', False) 
                          for constraints in all_constraints.values()]
        if len(set(coal_max_values)) > 1:
            differences['coal_maximization'] = {
                'values': dict(zip(all_constraints.keys(), coal_max_values)),
                'description': 'Different indigenous coal utilization policies'
            }
        
        return differences
    
    def get_scenario_recommendations(self, scenario_name: str) -> List[str]:
        """Get policy recommendations for a specific scenario"""
        if scenario_name not in self.scenarios:
            return []
        
        scenario = self.scenarios[scenario_name]
        recommendations = []
        
        # Base recommendations
        recommendations.append("Ensure adequate grid infrastructure for planned capacity additions")
        recommendations.append("Implement robust monitoring and reporting systems")
        
        # Scenario-specific recommendations
        if scenario.get('external_costs', False):
            recommendations.append("Include environmental externalities in cost-benefit analysis")
            recommendations.append("Consider carbon pricing mechanisms for emission reduction")
        
        if scenario.get('emission_cap'):
            cap_percentage = scenario['emission_cap'] * 100
            recommendations.append(f"Implement policies to achieve {cap_percentage}% emission reduction")
            recommendations.append("Develop carbon trading or offset mechanisms")
        
        if scenario.get('renewable_target'):
            target_percentage = scenario['renewable_target'] * 100
            recommendations.append(f"Establish renewable energy targets of {target_percentage}%")
            recommendations.append("Implement feed-in tariffs or renewable portfolio standards")
        
        if scenario.get('coal_max', False):
            recommendations.append("Maximize utilization of indigenous coal resources")
            recommendations.append("Invest in clean coal technologies and emission controls")
        
        return recommendations
    
    def export_scenario_report(self, output_path: str):
        """Export comprehensive scenario report"""
        
        # Create scenario summary
        summary_df = self.get_scenario_summary()
        
        # Create detailed constraints table
        constraints_data = []
        for name, scenario in self.scenarios.items():
            row = {
                'Scenario': name,
                'Description': scenario['description'],
                'External_Costs_Included': 'Yes' if scenario.get('external_costs') else 'No',
                'Emission_Reduction': f"{scenario.get('emission_cap', 0) * 100}%" if scenario.get('emission_cap') else 'None',
                'Renewable_Target': f"{scenario.get('renewable_target', 0) * 100}%" if scenario.get('renewable_target') else 'None',
                'Indigenous_Coal_Max': 'Yes' if scenario.get('coal_max') else 'No',
                'Policy_Focus': self._get_policy_focus(scenario)
            }
            constraints_data.append(row)
        
        constraints_df = pd.DataFrame(constraints_data)
        
        # Export to Excel with multiple sheets
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            summary_df.to_excel(writer, sheet_name='Scenario_Summary', index=False)
            constraints_df.to_excel(writer, sheet_name='Detailed_Constraints', index=False)
            
            # Add recommendations sheet
            recommendations_data = []
            for name in self.scenarios.keys():
                recs = self.get_scenario_recommendations(name)
                for i, rec in enumerate(recs):
                    recommendations_data.append({
                        'Scenario': name if i == 0 else '',
                        'Recommendation': rec
                    })
            
            rec_df = pd.DataFrame(recommendations_data)
            rec_df.to_excel(writer, sheet_name='Policy_Recommendations', index=False)
        
        print(f"Scenario report exported to: {output_path}")
    
    def _get_policy_focus(self, constraints: Dict[str, Any]) -> str:
        """Determine the main policy focus of a scenario"""
        if constraints.get('emission_cap'):
            return "Emission Reduction"
        elif constraints.get('renewable_target'):
            return "Renewable Energy"
        elif constraints.get('coal_max'):
            return "Indigenous Resources"
        elif constraints.get('external_costs'):
            return "Environmental Externalities"
        else:
            return "Business as Usual"
    
    def run_scenario_analysis(self, scenario_names: List[str] = None) -> Dict[str, Any]:
        """Run analysis for specified scenarios"""
        if scenario_names is None:
            scenario_names = list(self.scenarios.keys())
        
        analysis_results = {}
        
        for scenario_name in scenario_names:
            if scenario_name in self.scenarios:
                print(f"Analyzing scenario: {scenario_name}")
                
                # Get scenario details
                scenario_info = {
                    'description': self.scenarios[scenario_name]['description'],
                    'constraints': self.get_scenario_constraints(scenario_name),
                    'recommendations': self.get_scenario_recommendations(scenario_name)
                }
                
                analysis_results[scenario_name] = scenario_info
        
        return analysis_results
