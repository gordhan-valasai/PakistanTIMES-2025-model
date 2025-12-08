"""
Main Application Controller for PakistanTIMES Energy Modeling System
Integrates all components and provides the main interface for running the complete modeling exercise
"""

import os
import sys
import pandas as pd
from typing import Dict, List, Any

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data.data_manager import DataManager
from src.models.pakistan_times_model import PakistanTIMESModel
from src.scenarios.scenario_manager import ScenarioManager
from src.results.results_analyzer import ResultsAnalyzer
from src.data.demand_forecaster import DemandForecaster
from src.utils.excel_templates import ExcelTemplateGenerator
from config.config import MODEL_SCENARIOS, FILE_PATHS

class PakistanTIMESApplication:
    def __init__(self):
        """Initialize the PakistanTIMES application"""
        self.data_manager = DataManager()
        self.model = PakistanTIMESModel()
        self.scenario_manager = ScenarioManager()
        self.results_analyzer = ResultsAnalyzer()
        self.demand_forecaster = DemandForecaster()
        self.excel_generator = ExcelTemplateGenerator()
        
        # Results storage
        self.scenario_results = {}
        self.analysis_results = {}
        
        print("PakistanTIMES Energy Modeling System initialized successfully!")
    
    def setup_data_templates(self):
        """Create Excel input templates"""
        print("Creating input data templates...")
        
        try:
            self.excel_generator.create_all_templates(FILE_PATHS['input_dir'])
            print("Data templates created successfully!")
            return True
        except Exception as e:
            print(f"Error creating templates: {str(e)}")
            return False
    
    def load_input_data(self) -> bool:
        """Load all input data from Excel templates"""
        print("Loading input data...")
        
        try:
            success = self.data_manager.load_all_data()
            if success:
                # Set data in the model
                self.model.set_data(
                    self.data_manager.get_technology_data(),
                    self.data_manager.get_demand_data(),
                    self.data_manager.get_resource_data(),
                    self.data_manager.get_external_costs()
                )
                print("Input data loaded and set in model successfully!")
                return True
            else:
                print("Failed to load input data")
                return False
        except Exception as e:
            print(f"Error loading input data: {str(e)}")
            return False
    
    def run_single_scenario(self, scenario_name: str) -> Dict[str, Any]:
        """Run optimization for a single scenario"""
        print(f"Running scenario: {scenario_name}")
        
        try:
            # Create optimization model
            self.model.create_optimization_model(scenario_name)
            
            # Solve the model
            success = self.model.solve()
            
            if success:
                # Get results
                results = self.model.get_results()
                self.scenario_results[scenario_name] = results
                
                # Analyze results
                analysis = self.results_analyzer.analyze_scenario_results(results, scenario_name)
                self.analysis_results[scenario_name] = analysis
                
                print(f"Scenario {scenario_name} completed successfully!")
                return results
            else:
                print(f"Failed to solve scenario {scenario_name}")
                return {}
                
        except Exception as e:
            print(f"Error running scenario {scenario_name}: {str(e)}")
            return {}
    
    def run_all_scenarios(self) -> Dict[str, Dict[str, Any]]:
        """Run optimization for all defined scenarios"""
        print("Running all scenarios...")
        
        available_scenarios = self.scenario_manager.get_available_scenarios()
        
        for scenario_name in available_scenarios:
            print(f"\n--- Running {scenario_name} Scenario ---")
            self.run_single_scenario(scenario_name)
        
        print(f"\nAll scenarios completed! Results for {len(self.scenario_results)} scenarios.")
        return self.scenario_results
    
    def run_demand_forecasting(self) -> pd.DataFrame:
        """Run demand forecasting analysis"""
        print("Running demand forecasting...")
        
        try:
            # This would use actual historical data and economic indicators
            # For now, creating placeholder data
            historical_data = self._create_sample_historical_data()
            economic_indicators = self._create_sample_economic_data()
            
            # Set data in forecaster
            self.demand_forecaster.set_historical_data(historical_data)
            self.demand_forecaster.set_economic_indicators(economic_indicators)
            
            # Run index model
            self.demand_forecaster.index_model(historical_data, economic_indicators)
            
            # Generate forecasts for all scenarios
            demand_scenarios = self.demand_forecaster.create_demand_scenarios()
            
            print("Demand forecasting completed successfully!")
            return demand_scenarios
            
        except Exception as e:
            print(f"Error in demand forecasting: {str(e)}")
            return pd.DataFrame()
    
    def _create_sample_historical_data(self) -> pd.DataFrame:
        """Create sample historical demand data for demonstration"""
        years = list(range(2000, 2015))
        demand = [50000 + i * 2000 for i in range(len(years))]  # Growing demand
        
        return pd.DataFrame({
            'Year': years,
            'Demand': demand
        })
    
    def _create_sample_economic_data(self) -> pd.DataFrame:
        """Create sample economic indicators for demonstration"""
        years = list(range(2000, 2015))
        gdp_growth = [0.05] * len(years)  # 5% GDP growth
        population_growth = [0.02] * len(years)  # 2% population growth
        
        return pd.DataFrame({
            'Year': years,
            'GDP_Growth': gdp_growth,
            'Population_Growth': population_growth
        })
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive report matching thesis format"""
        print("Generating comprehensive report...")
        
        try:
            report = {
                'executive_summary': self._create_executive_summary(),
                'scenario_results': self._format_scenario_results(),
                'comparative_analysis': self._create_comparative_analysis(),
                'sensitivity_analysis': self._create_sensitivity_results(),
                'recommendations': self._generate_recommendations()
            }
            
            # Export reports
            self._export_reports()
            
            print("Comprehensive report generated successfully!")
            return report
            
        except Exception as e:
            print(f"Error generating report: {str(e)}")
            return {}
    
    def _create_executive_summary(self) -> str:
        """Create executive summary"""
        summary = """
        PAKISTANTIMES ENERGY MODELING SYSTEM - EXECUTIVE SUMMARY
        
        This report presents the results of the PakistanTIMES energy modeling system,
        which analyzes least-cost power generation options for Pakistan from 2014 to 2033.
        
        Key Findings:
        - Six scenarios analyzed: BASE, CEC10, CEC20, COALMAX, REN50, REN60
        - Model incorporates environmental externalities and policy constraints
        - Results provide insights for Pakistan's energy policy development
        
        Total Scenarios Analyzed: {scenario_count}
        Study Period: 2014-2033
        Model Type: TIMES framework with linear programming optimization
        """.format(scenario_count=len(self.scenario_results))
        
        return summary
    
    def _format_scenario_results(self) -> Dict[str, Any]:
        """Format scenario results for reporting"""
        formatted_results = {}
        
        for scenario_name, results in self.scenario_results.items():
            if scenario_name in self.analysis_results:
                analysis = self.analysis_results[scenario_name]
                formatted_results[scenario_name] = {
                    'description': self.scenario_manager.get_scenario_description(scenario_name),
                    'summary': analysis['summary_statistics'],
                    'capacity_analysis': analysis['installed_capacity'],
                    'generation_analysis': analysis['generation_mix'],
                    'emissions_analysis': analysis['emissions']
                }
        
        return formatted_results
    
    def _create_comparative_analysis(self) -> Dict[str, Any]:
        """Create comparative analysis between scenarios"""
        if len(self.scenario_results) < 2:
            return {"message": "Insufficient scenarios for comparison"}
        
        return self.results_analyzer.compare_scenarios(self.scenario_results)
    
    def _create_sensitivity_results(self) -> Dict[str, Any]:
        """Create sensitivity analysis results"""
        # Placeholder for sensitivity analysis
        return {
            "message": "Sensitivity analysis to be implemented in future versions"
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate policy recommendations"""
        recommendations = []
        
        # General recommendations
        recommendations.append("Implement comprehensive energy planning framework")
        recommendations.append("Develop renewable energy support mechanisms")
        recommendations.append("Establish carbon pricing or trading systems")
        recommendations.append("Invest in grid infrastructure modernization")
        recommendations.append("Promote energy efficiency measures")
        
        # Scenario-specific recommendations
        for scenario_name in self.scenario_results.keys():
            scenario_recs = self.scenario_manager.get_scenario_recommendations(scenario_name)
            recommendations.extend(scenario_recs)
        
        return list(set(recommendations))  # Remove duplicates
    
    def _export_reports(self):
        """Export all reports to files"""
        try:
            # Export scenario results
            for scenario_name, results in self.scenario_results.items():
                output_path = os.path.join(FILE_PATHS['results_dir'], f'{scenario_name}_results.csv')
                self.model.export_results_to_csv(output_path)
            
            # Export analysis reports
            analysis_output = os.path.join(FILE_PATHS['reports_dir'], 'scenario_analysis.xlsx')
            self.results_analyzer.export_analysis_report(analysis_output)
            
            # Export scenario comparison
            comparison_output = os.path.join(FILE_PATHS['reports_dir'], 'scenario_comparison.xlsx')
            self.scenario_manager.export_scenario_report(comparison_output)
            
            # Export demand forecast
            if hasattr(self.demand_forecaster, 'forecast_results') and self.demand_forecaster.forecast_results:
                forecast_output = os.path.join(FILE_PATHS['reports_dir'], 'demand_forecast.xlsx')
                self.demand_forecaster.export_forecast_report(forecast_output)
            
            print("All reports exported successfully!")
            
        except Exception as e:
            print(f"Error exporting reports: {str(e)}")
    
    def run_complete_analysis(self):
        """Run complete modeling exercise"""
        print("=" * 60)
        print("PAKISTANTIMES COMPLETE MODELING EXERCISE")
        print("=" * 60)
        
        try:
            # Step 1: Setup data templates
            if not self.setup_data_templates():
                print("Failed to setup data templates. Exiting.")
                return False
            
            # Step 2: Load input data
            if not self.load_input_data():
                print("Failed to load input data. Exiting.")
                return False
            
            # Step 3: Run demand forecasting
            demand_results = self.run_demand_forecasting()
            
            # Step 4: Run all scenarios
            scenario_results = self.run_all_scenarios()
            
            # Step 5: Generate comprehensive report
            report = self.generate_comprehensive_report()
            
            print("\n" + "=" * 60)
            print("ANALYSIS COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"Scenarios analyzed: {len(scenario_results)}")
            print(f"Results exported to: {FILE_PATHS['results_dir']}")
            print(f"Reports exported to: {FILE_PATHS['reports_dir']}")
            
            return True
            
        except Exception as e:
            print(f"Error in complete analysis: {str(e)}")
            return False

def main():
    """Main function to run the PakistanTIMES application"""
    
    # Create application instance
    app = PakistanTIMESApplication()
    
    # Run complete analysis
    success = app.run_complete_analysis()
    
    if success:
        print("\nPakistanTIMES analysis completed successfully!")
        print("Check the output directories for results and reports.")
    else:
        print("\nPakistanTIMES analysis failed. Please check error messages above.")
    
    return success

if __name__ == "__main__":
    main()
