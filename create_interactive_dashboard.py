#!/usr/bin/env python3
"""PakistanTIMES 2025: Interactive Dashboard Creator"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
from datetime import datetime

class PakistanTIMESDashboard:
    def __init__(self):
        self.model_dir = "integrated_corrected_model_20250825_093345"
        self.results_dir = "simple_results_package_20250825_093857"
        
    def load_data(self):
        """Load all model data"""
        # Load scenario comparison
        comparison_file = f"{self.model_dir}/corrected_scenarios_comparison.csv"
        self.scenario_comparison = pd.read_csv(comparison_file)
        
        # Load individual scenario results
        self.scenario_results = {}
        for _, row in self.scenario_comparison.iterrows():
            scenario_name = row['Scenario']
            yearly_file = f"{self.model_dir}/corrected_scenario_{scenario_name}.xlsx"
            if os.path.exists(yearly_file):
                self.scenario_results[scenario_name] = pd.read_excel(yearly_file)
        
        return True
    
    def create_dashboard(self):
        """Create the main dashboard"""
        st.set_page_config(
            page_title="PakistanTIMES 2025 Dashboard",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Header
        st.title("⚡ PakistanTIMES 2025: Energy System Modeling Dashboard")
        st.markdown("**Interactive Analysis of Pakistan's Energy Transition Pathways (2014-2050)**")
        st.markdown("---")
        
        # Sidebar
        self.create_sidebar()
        
        # Main content
        if 'selected_scenario' in st.session_state:
            self.create_main_content()
        else:
            st.info("👈 Please select a scenario from the sidebar to begin analysis.")
    
    def create_sidebar(self):
        """Create the sidebar with controls"""
        st.sidebar.header("🎛️ Dashboard Controls")
        
        # Scenario selection
        st.sidebar.subheader("📊 Scenario Selection")
        selected_scenario = st.sidebar.selectbox(
            "Choose a scenario:",
            options=self.scenario_comparison['Scenario'].tolist(),
            index=0
        )
        
        if st.sidebar.button("🔍 Load Scenario Analysis"):
            st.session_state.selected_scenario = selected_scenario
            st.rerun()
        
        # Quick stats
        st.sidebar.subheader("📈 Quick Statistics")
        scenario_data = self.scenario_comparison[self.scenario_comparison['Scenario'] == selected_scenario].iloc[0]
        
        st.sidebar.metric("Demand 2050", f"{scenario_data['Demand_2050_TWh']:.0f} TWh")
        st.sidebar.metric("Investment", f"${scenario_data['Avg_Annual_Investment_B$']:.1f}B/yr")
        st.sidebar.metric("Emissions 2050", f"{scenario_data['Emissions_2050_MtCO2']:.0f} MtCO₂")
        st.sidebar.metric("Renewable 2050", f"{scenario_data['Renewable_Share_2050_%']:.0f}%")
        
        # Filters
        st.sidebar.subheader("🔍 Data Filters")
        year_range = st.sidebar.slider(
            "Year Range:",
            min_value=2014,
            max_value=2050,
            value=(2014, 2050),
            step=1
        )
        
        st.session_state.year_range = year_range
        
        # Export options
        st.sidebar.subheader("💾 Export Options")
        if st.sidebar.button("📥 Download Scenario Data"):
            self.download_scenario_data(selected_scenario)
        
        if st.sidebar.button("📊 Download All Results"):
            self.download_all_results()
    
    def create_main_content(self):
        """Create the main dashboard content"""
        selected_scenario = st.session_state.selected_scenario
        year_range = st.session_state.year_range
        
        # Scenario overview
        col1, col2, col3, col4 = st.columns(4)
        scenario_data = self.scenario_comparison[self.scenario_comparison['Scenario'] == selected_scenario].iloc[0]
        
        with col1:
            st.metric("Demand 2050", f"{scenario_data['Demand_2050_TWh']:.0f} TWh", 
                     delta=f"{scenario_data['Growth_Factor_2014_2050']:.1f}x from 2014")
        
        with col2:
            st.metric("Investment", f"${scenario_data['Avg_Annual_Investment_B$']:.1f}B/yr",
                     delta=f"${scenario_data['Investment_2025_2050_B$']:.0f}B total")
        
        with col3:
            st.metric("Emissions 2050", f"{scenario_data['Emissions_2050_MtCO2']:.0f} MtCO₂",
                     delta=f"{(scenario_data['Emissions_2050_MtCO2'] - 85.0) / 85.0 * 100:.0f}% from 2014")
        
        with col4:
            st.metric("Renewable 2050", f"{scenario_data['Renewable_Share_2050_%']:.0f}%",
                     delta=f"{scenario_data['Renewable_Share_2050_%'] - 5:.0f}% from 2014")
        
        st.markdown("---")
        
        # Tabs for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Demand & Generation", 
            "💰 Investment Analysis", 
            "🌍 Emissions & Decarbonization",
            "⚙️ Technology Evolution",
            "📊 Scenario Comparison"
        ])
        
        with tab1:
            self.create_demand_generation_tab(selected_scenario, year_range)
        
        with tab2:
            self.create_investment_tab(selected_scenario, year_range)
        
        with tab3:
            self.create_emissions_tab(selected_scenario, year_range)
        
        with tab4:
            self.create_technology_tab(selected_scenario, year_range)
        
        with tab5:
            self.create_scenario_comparison_tab()
    
    def create_demand_generation_tab(self, scenario_name, year_range):
        """Create demand and generation analysis tab"""
        st.header("📈 Demand & Generation Analysis")
        
        if scenario_name in self.scenario_results:
            data = self.scenario_results[scenario_name]
            filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]
            
            # Demand evolution
            col1, col2 = st.columns(2)
            
            with col1:
                fig_demand = px.line(
                    filtered_data, 
                    x='Year', 
                    y='Demand_TWh',
                    title=f"Electricity Demand Evolution - {scenario_name}",
                    labels={'Demand_TWh': 'Demand (TWh)', 'Year': 'Year'}
                )
                fig_demand.update_layout(height=400)
                st.plotly_chart(fig_demand, use_container_width=True)
            
            with col2:
                fig_generation = px.line(
                    filtered_data,
                    x='Year',
                    y=['Renewable_Generation_TWh', 'Thermal_Generation_TWh'],
                    title=f"Generation Mix Evolution - {scenario_name}",
                    labels={'value': 'Generation (TWh)', 'Year': 'Year', 'variable': 'Type'}
                )
                fig_generation.update_layout(height=400)
                st.plotly_chart(fig_generation, use_container_width=True)
            
            # Capacity analysis
            st.subheader("📊 Capacity Requirements")
            col1, col2 = st.columns(2)
            
            with col1:
                fig_capacity = px.line(
                    filtered_data,
                    x='Year',
                    y=['Renewable_Capacity_GW', 'Thermal_Capacity_GW'],
                    title=f"Installed Capacity - {scenario_name}",
                    labels={'value': 'Capacity (GW)', 'Year': 'Year', 'variable': 'Type'}
                )
                fig_capacity.update_layout(height=400)
                st.plotly_chart(fig_capacity, use_container_width=True)
            
            with col2:
                fig_ratio = px.line(
                    filtered_data,
                    x='Year',
                    y='Generation_Demand_Ratio',
                    title=f"Generation-Demand Ratio - {scenario_name}",
                    labels={'Generation_Demand_Ratio': 'Ratio', 'Year': 'Year'}
                )
                fig_ratio.update_layout(height=400)
                st.plotly_chart(fig_ratio, use_container_width=True)
    
    def create_investment_tab(self, scenario_name, year_range):
        """Create investment analysis tab"""
        st.header("💰 Investment Analysis")
        
        if scenario_name in self.scenario_results:
            data = self.scenario_results[scenario_name]
            filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]
            
            # Investment evolution
            col1, col2 = st.columns(2)
            
            with col1:
                fig_investment = px.bar(
                    filtered_data,
                    x='Year',
                    y='Investment_Billion_USD',
                    title=f"Annual Investment Requirements - {scenario_name}",
                    labels={'Investment_Billion_USD': 'Investment (Billion USD)', 'Year': 'Year'}
                )
                fig_investment.update_layout(height=400)
                st.plotly_chart(fig_investment, use_container_width=True)
            
            with col2:
                # Cumulative investment
                filtered_data['Cumulative_Investment'] = filtered_data['Investment_Billion_USD'].cumsum()
                fig_cumulative = px.line(
                    filtered_data,
                    x='Year',
                    y='Cumulative_Investment',
                    title=f"Cumulative Investment - {scenario_name}",
                    labels={'Cumulative_Investment': 'Cumulative Investment (Billion USD)', 'Year': 'Year'}
                )
                fig_cumulative.update_layout(height=400)
                st.plotly_chart(fig_cumulative, use_container_width=True)
            
            # Investment summary
            st.subheader("📊 Investment Summary")
            col1, col2, col3 = st.columns(3)
            
            total_investment = filtered_data['Investment_Billion_USD'].sum()
            avg_investment = filtered_data['Investment_Billion_USD'].mean()
            max_investment = filtered_data['Investment_Billion_USD'].max()
            
            with col1:
                st.metric("Total Investment", f"${total_investment:.1f}B")
            
            with col2:
                st.metric("Average Annual", f"${avg_investment:.1f}B")
            
            with col3:
                st.metric("Peak Annual", f"${max_investment:.1f}B")
    
    def create_emissions_tab(self, scenario_name, year_range):
        """Create emissions analysis tab"""
        st.header("🌍 Emissions & Decarbonization Analysis")
        
        if scenario_name in self.scenario_results:
            data = self.scenario_results[scenario_name]
            filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]
            
            # Emissions evolution
            col1, col2 = st.columns(2)
            
            with col1:
                fig_emissions = px.line(
                    filtered_data,
                    x='Year',
                    y='Annual_Emissions_MtCO2',
                    title=f"Annual Emissions - {scenario_name}",
                    labels={'Annual_Emissions_MtCO2': 'Emissions (MtCO₂)', 'Year': 'Year'}
                )
                fig_emissions.update_layout(height=400)
                st.plotly_chart(fig_emissions, use_container_width=True)
            
            with col2:
                fig_cumulative = px.line(
                    filtered_data,
                    x='Year',
                    y='Cumulative_Emissions_GtCO2',
                    title=f"Cumulative Emissions - {scenario_name}",
                    labels={'Cumulative_Emissions_GtCO2': 'Cumulative Emissions (GtCO₂)', 'Year': 'Year'}
                )
                fig_cumulative.update_layout(height=400)
                st.plotly_chart(fig_cumulative, use_container_width=True)
            
            # Decarbonization metrics
            st.subheader("📊 Decarbonization Metrics")
            col1, col2, col3 = st.columns(3)
            
            emissions_2014 = 85.0
            emissions_2050 = filtered_data[filtered_data['Year'] == 2050]['Annual_Emissions_MtCO2'].iloc[0]
            reduction_pct = (emissions_2014 - emissions_2050) / emissions_2014 * 100
            
            with col1:
                st.metric("Emissions 2014", f"{emissions_2014:.0f} MtCO₂")
            
            with col2:
                st.metric("Emissions 2050", f"{emissions_2050:.0f} MtCO₂")
            
            with col3:
                st.metric("Reduction", f"{reduction_pct:.0f}%")
    
    def create_technology_tab(self, scenario_name, year_range):
        """Create technology evolution tab"""
        st.header("⚙️ Technology Evolution Analysis")
        
        if scenario_name in self.scenario_results:
            data = self.scenario_results[scenario_name]
            filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]
            
            # Technology mix evolution
            col1, col2 = st.columns(2)
            
            with col1:
                fig_mix = px.line(
                    filtered_data,
                    x='Year',
                    y='Renewable_Share_%',
                    title=f"Renewable Share Evolution - {scenario_name}",
                    labels={'Renewable_Share_%': 'Renewable Share (%)', 'Year': 'Year'}
                )
                fig_mix.update_layout(height=400)
                st.plotly_chart(fig_mix, use_container_width=True)
            
            with col2:
                # Technology mix pie chart for 2050
                if 2050 in filtered_data['Year'].values:
                    data_2050 = filtered_data[filtered_data['Year'] == 2050].iloc[0]
                    renewable_share = data_2050['Renewable_Share_%'] / 100
                    thermal_share = 1 - renewable_share
                    
                    fig_pie = px.pie(
                        values=[renewable_share, thermal_share],
                        names=['Renewable', 'Thermal'],
                        title=f"Technology Mix 2050 - {scenario_name}"
                    )
                    fig_pie.update_layout(height=400)
                    st.plotly_chart(fig_pie, use_container_width=True)
            
            # System reliability metrics
            st.subheader("📊 System Reliability Metrics")
            col1, col2, col3 = st.columns(3)
            
            if 2050 in filtered_data['Year'].values:
                data_2050 = filtered_data[filtered_data['Year'] == 2050].iloc[0]
                
                with col1:
                    st.metric("Reserve Margin", f"{data_2050['Reserve_Margin_%']:.0f}%")
                
                with col2:
                    st.metric("System Losses", f"{data_2050['System_Losses_%']:.0f}%")
                
                with col3:
                    st.metric("Storage Requirement", f"{data_2050['Storage_Requirement_%']:.0f}%")
    
    def create_scenario_comparison_tab(self):
        """Create scenario comparison tab"""
        st.header("📊 Scenario Comparison Analysis")
        
        # Scenario matrix
        st.subheader("🎯 Scenario Matrix Overview")
        
        # Create comparison table
        comparison_data = self.scenario_comparison.copy()
        comparison_data['Demand_2050_TWh'] = comparison_data['Demand_2050_TWh'].round(0)
        comparison_data['Avg_Annual_Investment_B$'] = comparison_data['Avg_Annual_Investment_B$'].round(1)
        comparison_data['Emissions_2050_MtCO2'] = comparison_data['Emissions_2050_MtCO2'].round(0)
        comparison_data['Renewable_Share_2050_%'] = comparison_data['Renewable_Share_2050_%'].round(0)
        
        st.dataframe(
            comparison_data[['Scenario', 'Demand_2050_TWh', 'Avg_Annual_Investment_B$', 'Emissions_2050_MtCO2', 'Renewable_Share_2050_%']],
            use_container_width=True
        )
        
        # Interactive comparison charts
        st.subheader("📈 Interactive Comparison Charts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Demand comparison
            fig_demand_comp = px.bar(
                self.scenario_comparison,
                x='Scenario',
                y='Demand_2050_TWh',
                title="Demand 2050 Comparison",
                labels={'Demand_2050_TWh': 'Demand 2050 (TWh)', 'Scenario': 'Scenario'}
            )
            fig_demand_comp.update_xaxes(tickangle=45)
            fig_demand_comp.update_layout(height=400)
            st.plotly_chart(fig_demand_comp, use_container_width=True)
        
        with col2:
            # Investment comparison
            fig_inv_comp = px.bar(
                self.scenario_comparison,
                x='Scenario',
                y='Avg_Annual_Investment_B$',
                title="Average Annual Investment Comparison",
                labels={'Avg_Annual_Investment_B$': 'Investment (Billion USD/yr)', 'Scenario': 'Scenario'}
            )
            fig_inv_comp.update_xaxes(tickangle=45)
            fig_inv_comp.update_layout(height=400)
            st.plotly_chart(fig_inv_comp, use_container_width=True)
        
        # Emissions comparison
        st.subheader("🌍 Emissions Comparison")
        fig_emissions_comp = px.bar(
            self.scenario_comparison,
            x='Scenario',
            y='Emissions_2050_MtCO2',
            title="Emissions 2050 Comparison",
            labels={'Emissions_2050_MtCO2': 'Emissions 2050 (MtCO₂)', 'Scenario': 'Scenario'}
        )
        fig_emissions_comp.update_xaxes(tickangle=45)
        fig_emissions_comp.update_layout(height=400)
        st.plotly_chart(fig_emissions_comp, use_container_width=True)
    
    def download_scenario_data(self, scenario_name):
        """Download scenario data"""
        if scenario_name in self.scenario_results:
            data = self.scenario_results[scenario_name]
            csv = data.to_csv(index=False)
            st.download_button(
                label=f"📥 Download {scenario_name} Data (CSV)",
                data=csv,
                file_name=f"{scenario_name}_data.csv",
                mime="text/csv"
            )
    
    def download_all_results(self):
        """Download all results"""
        csv = self.scenario_comparison.to_csv(index=False)
        st.download_button(
            label="📥 Download All Results (CSV)",
            data=csv,
            file_name="PakistanTIMES_2025_all_results.csv",
            mime="text/csv"
        )
    
    def run_dashboard(self):
        """Run the dashboard"""
        if self.load_data():
            self.create_dashboard()
        else:
            st.error("❌ Failed to load model data. Please check the data files.")

def main():
    """Main function to run the dashboard"""
    dashboard = PakistanTIMESDashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main()
