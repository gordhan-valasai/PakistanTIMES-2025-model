"""
Demand Forecaster for PakistanTIMES Model
Implements demand forecasting models based on Chapter 4 methodology
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from typing import Dict, List, Tuple, Optional, Any
from config.config import STUDY_PERIOD, DEMAND_SCENARIOS

class DemandForecaster:
    def __init__(self):
        self.models = {}
        self.forecast_results = {}
        self.historical_data = None
        self.economic_indicators = None
        
    def set_historical_data(self, historical_data: pd.DataFrame):
        """Set historical electricity demand data"""
        self.historical_data = historical_data
        
    def set_economic_indicators(self, economic_indicators: pd.DataFrame):
        """Set economic indicators for forecasting"""
        self.economic_indicators = economic_indicators
    
    def index_model(self, historical_data: pd.DataFrame, 
                   economic_indicators: pd.DataFrame) -> Dict[str, Any]:
        """
        Implement Index Model from Chapter 4.2.5
        Y = a + b1*Y(i-1) + b2*G(i) + b3*C(i) + e
        
        Where:
        Y = Electricity demand
        G = GDP growth rate
        C = Population growth rate
        """
        
        if historical_data is None or economic_indicators is None:
            raise ValueError("Historical data and economic indicators required")
        
        # Prepare data for regression
        model_data = self._prepare_regression_data(historical_data, economic_indicators)
        
        if model_data is None or len(model_data) < 3:
            raise ValueError("Insufficient data for regression analysis")
        
        # Create regression model
        X = model_data[['Demand_Lag1', 'GDP_Growth', 'Population_Growth']]
        y = model_data['Demand']
        
        # Fit linear regression
        model = LinearRegression()
        model.fit(X, y)
        
        # Calculate predictions
        y_pred = model.predict(X)
        
        # Calculate model performance metrics
        r2 = r2_score(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        mape = np.mean(np.abs((y - y_pred) / y)) * 100
        
        # Store model results
        model_results = {
            'model': model,
            'coefficients': {
                'intercept': model.intercept_,
                'demand_lag': model.coef_[0],
                'gdp_growth': model.coef_[1],
                'population_growth': model.coef_[2]
            },
            'performance': {
                'r2_score': r2,
                'rmse': rmse,
                'mape': mape
            },
            'predictions': y_pred,
            'actual': y.values
        }
        
        self.models['index_model'] = model_results
        
        print(f"Index Model Results:")
        print(f"  R² Score: {r2:.4f}")
        print(f"  RMSE: {rmse:.2f}")
        print(f"  MAPE: {mape:.2f}%")
        
        return model_results
    
    def _prepare_regression_data(self, historical_data: pd.DataFrame, 
                                economic_indicators: pd.DataFrame) -> pd.DataFrame:
        """Prepare data for regression analysis"""
        
        # Merge historical demand with economic indicators
        merged_data = pd.merge(historical_data, economic_indicators, 
                              on='Year', how='inner')
        
        # Sort by year
        merged_data = merged_data.sort_values('Year').reset_index(drop=True)
        
        # Create lagged demand variable
        merged_data['Demand_Lag1'] = merged_data['Demand'].shift(1)
        
        # Remove rows with missing values
        merged_data = merged_data.dropna()
        
        return merged_data
    
    def trend_model(self, historical_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Implement Trend Model for demand forecasting
        Y = a + b*t + e
        
        Where:
        Y = Electricity demand
        t = Time trend
        """
        
        if historical_data is None:
            raise ValueError("Historical data required")
        
        # Prepare time series data
        data = historical_data.sort_values('Year').reset_index(drop=True)
        data['Time_Trend'] = range(len(data))
        
        # Create regression model
        X = data[['Time_Trend']]
        y = data['Demand']
        
        # Fit linear regression
        model = LinearRegression()
        model.fit(X, y)
        
        # Calculate predictions
        y_pred = model.predict(X)
        
        # Calculate model performance metrics
        r2 = r2_score(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        mape = np.mean(np.abs((y - y_pred) / y)) * 100
        
        # Store model results
        model_results = {
            'model': model,
            'coefficients': {
                'intercept': model.intercept_,
                'trend': model.coef_[0]
            },
            'performance': {
                'r2_score': r2,
                'rmse': rmse,
                'mape': mape
            },
            'predictions': y_pred,
            'actual': y.values
        }
        
        self.models['trend_model'] = model_results
        
        print(f"Trend Model Results:")
        print(f"  R² Score: {r2:.4f}")
        print(f"  RMSE: {rmse:.2f}")
        print(f"  MAPE: {mape:.2f}%")
        
        return model_results
    
    def forecast_demand(self, scenario: str = 'BAU', end_year: int = 2033) -> pd.Series:
        """Generate demand forecast for given scenario"""
        
        if 'index_model' not in self.models:
            raise ValueError("Index model not fitted. Run index_model() first.")
        
        # Get base year demand
        base_year = STUDY_PERIOD['base_year']
        base_demand = self._get_base_demand(base_year)
        
        # Generate forecast years
        forecast_years = range(base_year + 1, end_year + 1)
        
        # Initialize forecast results
        forecast_results = pd.Series(index=forecast_years, dtype=float)
        forecast_results[base_year] = base_demand
        
        # Get model coefficients
        model = self.models['index_model']['model']
        coefficients = self.models['index_model']['coefficients']
        
        # Generate forecasts
        for year in forecast_years:
            if year == base_year + 1:
                # First forecast year
                lag_demand = base_demand
            else:
                lag_demand = forecast_results[year - 1]
            
            # Get economic indicators for the year
            gdp_growth = self._get_economic_indicator(year, 'GDP_Growth', scenario)
            population_growth = self._get_economic_indicator(year, 'Population_Growth', scenario)
            
            # Calculate forecast
            forecast = (coefficients['intercept'] + 
                       coefficients['demand_lag'] * lag_demand +
                       coefficients['gdp_growth'] * gdp_growth +
                       coefficients['population_growth'] * population_growth)
            
            # Ensure non-negative demand
            forecast = max(0, forecast)
            forecast_results[year] = forecast
        
        # Store forecast results
        self.forecast_results[scenario] = forecast_results
        
        return forecast_results
    
    def _get_base_demand(self, base_year: int) -> float:
        """Get base year demand from historical data"""
        if self.historical_data is None:
            # Use default value if no historical data
            return 100000  # GWh placeholder
        
        base_data = self.historical_data[self.historical_data['Year'] == base_year]
        if len(base_data) > 0:
            return base_data['Demand'].iloc[0]
        else:
            # Use last available year
            return self.historical_data['Demand'].iloc[-1]
    
    def _get_economic_indicator(self, year: int, indicator: str, scenario: str) -> float:
        """Get economic indicator value for a given year and scenario"""
        
        if self.economic_indicators is None:
            # Use default values if no economic indicators
            if indicator == 'GDP_Growth':
                return 0.05  # 5% default GDP growth
            elif indicator == 'Population_Growth':
                return 0.02  # 2% default population growth
            else:
                return 0.0
        
        # Get indicator data for the year
        year_data = self.economic_indicators[self.economic_indicators['Year'] == year]
        
        if len(year_data) > 0:
            # Apply scenario-specific adjustments
            base_value = year_data[indicator].iloc[0]
            
            if scenario == 'LEG':  # Low Economic Growth
                return base_value * 0.7
            elif scenario == 'MEG':  # Medium Economic Growth
                return base_value * 1.0
            elif scenario == 'HEG':  # High Economic Growth
                return base_value * 1.3
            else:  # BAU
                return base_value
        else:
            # Use default values for future years
            if indicator == 'GDP_Growth':
                return 0.05
            elif indicator == 'Population_Growth':
                return 0.02
            else:
                return 0.0
    
    def create_demand_scenarios(self) -> pd.DataFrame:
        """Create demand scenarios for all economic growth assumptions"""
        
        scenarios = list(DEMAND_SCENARIOS.keys())
        demand_scenarios = {}
        
        for scenario in scenarios:
            forecast = self.forecast_demand(scenario)
            demand_scenarios[scenario] = forecast
        
        # Create DataFrame
        df = pd.DataFrame(demand_scenarios)
        df.index.name = 'Year'
        
        return df
    
    def validate_forecast(self, actual_data: pd.DataFrame) -> Dict[str, float]:
        """Validate forecast against actual data"""
        
        if 'index_model' not in self.models:
            raise ValueError("No forecast model available for validation")
        
        # Get actual and predicted values for overlapping years
        common_years = set(actual_data['Year']) & set(self.forecast_results['BAU'].index)
        
        if len(common_years) == 0:
            return {"error": "No overlapping years for validation"}
        
        actual_values = []
        predicted_values = []
        
        for year in sorted(common_years):
            actual_values.append(actual_data[actual_data['Year'] == year]['Demand'].iloc[0])
            predicted_values.append(self.forecast_results['BAU'][year])
        
        # Calculate validation metrics
        r2 = r2_score(actual_values, predicted_values)
        rmse = np.sqrt(mean_squared_error(actual_values, predicted_values))
        mape = np.mean(np.abs((np.array(actual_values) - np.array(predicted_values)) / np.array(actual_values))) * 100
        
        validation_results = {
            'r2_score': r2,
            'rmse': rmse,
            'mape': mape,
            'validation_years': len(common_years)
        }
        
        return validation_results
    
    def export_forecast_report(self, output_path: str):
        """Export demand forecast report to Excel"""
        
        if not self.forecast_results:
            print("No forecast results available for export")
            return
        
        # Create forecast summary
        forecast_summary = pd.DataFrame(self.forecast_results)
        
        # Create model performance summary
        performance_data = []
        for model_name, model_results in self.models.items():
            performance = model_results['performance']
            performance_data.append({
                'Model': model_name,
                'R² Score': performance['r2_score'],
                'RMSE': performance['rmse'],
                'MAPE (%)': performance['mape']
            })
        
        performance_df = pd.DataFrame(performance_data)
        
        # Export to Excel
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            forecast_summary.to_excel(writer, sheet_name='Demand_Forecasts', index=True)
            performance_df.to_excel(writer, sheet_name='Model_Performance', index=False)
            
            # Add scenario descriptions
            scenario_desc = pd.DataFrame([
                {'Scenario': k, 'Description': v} 
                for k, v in DEMAND_SCENARIOS.items()
            ])
            scenario_desc.to_excel(writer, sheet_name='Scenario_Descriptions', index=False)
        
        print(f"Demand forecast report exported to: {output_path}")
    
    def plot_forecast(self, scenario: str = 'BAU'):
        """Plot demand forecast for a specific scenario"""
        
        if scenario not in self.forecast_results:
            print(f"No forecast available for scenario: {scenario}")
            return
        
        import matplotlib.pyplot as plt
        
        forecast = self.forecast_results[scenario]
        
        plt.figure(figsize=(10, 6))
        plt.plot(forecast.index, forecast.values, 'b-', linewidth=2, label=f'{scenario} Forecast')
        
        # Add historical data if available
        if self.historical_data is not None:
            plt.scatter(self.historical_data['Year'], self.historical_data['Demand'], 
                       color='red', s=50, label='Historical Data')
        
        plt.xlabel('Year')
        plt.ylabel('Electricity Demand (GWh)')
        plt.title(f'Electricity Demand Forecast - {scenario} Scenario')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
