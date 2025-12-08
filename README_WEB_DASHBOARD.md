# 🌐 PakistanTIMES Interactive Web Dashboard

## 📋 Overview

The PakistanTIMES Interactive Web Dashboard is a powerful, web-based interface that provides dynamic visualization and analysis of Pakistan's energy future under the BASE scenario with government plans (2025-2050). Built with Streamlit and Plotly, it offers an engaging, interactive experience for policymakers, researchers, and stakeholders.

## ✨ Features

### 🎛️ **Interactive Controls**
- **Year Range Slider**: Filter data for specific time periods
- **Scenario Selector**: Choose between BAU, HEG, LEG, MEG scenarios
- **Metric Selector**: Focus on specific performance indicators
- **Real-time Filtering**: Instant updates as you adjust parameters

### 📊 **Dynamic Visualizations**
- **Interactive Charts**: Hover, zoom, and pan capabilities
- **Responsive Design**: Adapts to different screen sizes
- **Professional Styling**: Clean, modern interface with custom CSS
- **Export Capabilities**: Download filtered data as CSV files

### 🎯 **Key Dashboard Panels**
1. **Key Performance Indicators**: High-level metrics at a glance
2. **Interactive Charts**: Demand projections, renewable analysis, capacity planning
3. **Key Insights**: Critical findings and analysis
4. **Policy Recommendations**: Strategic guidance for stakeholders
5. **Detailed Analysis**: Comprehensive data tables with filtering

## 🚀 **Quick Start**

### **Option 1: Simple Launch (Recommended)**
```bash
python launch_web_dashboard.py
```

### **Option 2: Manual Launch**
```bash
# Install dependencies first
pip install -r requirements_web_dashboard.txt

# Launch dashboard
streamlit run create_web_dashboard.py
```

### **Option 3: Direct Streamlit Launch**
```bash
streamlit run create_web_dashboard.py
```

## 📦 **Installation Requirements**

### **System Requirements**
- Python 3.8 or higher
- 4GB RAM minimum
- Modern web browser (Chrome, Firefox, Safari, Edge)

### **Python Dependencies**
```
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0
```

### **Installation Commands**
```bash
# Install all requirements
pip install -r requirements_web_dashboard.txt

# Or install individually
pip install streamlit plotly pandas numpy openpyxl
```

## 🌐 **Accessing the Dashboard**

### **Local Access**
- **URL**: http://localhost:8501
- **Port**: 8501 (default)
- **Browser**: Automatically opens in default browser

### **Network Access**
- **URL**: http://[YOUR_IP]:8501
- **Port**: 8501 (configurable)
- **Access**: Available to other devices on your network

## 🎛️ **Dashboard Navigation**

### **Sidebar Controls**
- **🎛️ Dashboard Controls**: Main control panel
- **📅 Year Range**: Select specific time periods
- **📊 Scenario**: Choose demand scenario
- **📈 Metric**: Select primary performance indicator
- **📊 Quick Stats**: Key metrics at a glance

### **Main Content Area**
- **📊 Key Performance Indicators**: Four metric cards
- **📈 Interactive Visualizations**: Dynamic charts and graphs
- **🎯 Key Insights**: Critical findings and analysis
- **📋 Policy Recommendations**: Strategic guidance
- **🔍 Detailed Analysis**: Data tables and export options

## 📊 **Dashboard Features**

### **1. Key Performance Indicators**
- **📊 Total Demand (2050)**: 560 TWh with growth percentage
- **💰 Total Investment**: $26.1 Billion required
- **🌱 Renewable Targets**: 0/6 targets met
- **⚡ Peak Capacity**: 5,219 MW annual addition

### **2. Interactive Charts**
- **📈 Demand Projection**: BAU, HEG, LEG scenarios
- **🌱 Renewable Analysis**: Target vs. actual comparison
- **⚡ Capacity Planning**: Annual new capacity additions
- **💰 Investment Requirements**: Yearly investment needs

### **3. Data Export**
- **📥 Summary Data**: Download filtered summary data
- **📥 Demand Data**: Download demand projection data
- **📊 Format**: CSV files for Excel/analysis tools

## 🔧 **Customization Options**

### **Modifying Charts**
Edit `create_web_dashboard.py` to:
- Change chart colors and styles
- Add new chart types
- Modify chart layouts and dimensions
- Customize hover information

### **Adding New Metrics**
Extend the dashboard by:
- Adding new metric cards
- Creating additional visualizations
- Including new data sources
- Implementing custom calculations

### **Styling Changes**
Modify the CSS in the `create_streamlit_app` function to:
- Change color schemes
- Adjust fonts and sizes
- Modify layout spacing
- Add custom animations

## 📱 **Mobile and Tablet Support**

### **Responsive Design**
- **Mobile**: Optimized for smartphones
- **Tablet**: Touch-friendly interface
- **Desktop**: Full-featured experience
- **Responsive**: Adapts to screen size

### **Touch Controls**
- **Swipe**: Navigate between sections
- **Tap**: Interact with charts
- **Pinch**: Zoom in/out on charts
- **Scroll**: Navigate long content

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Port Already in Use**
```bash
# Kill existing process
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run create_web_dashboard.py --server.port 8502
```

#### **2. Missing Dependencies**
```bash
# Reinstall requirements
pip install -r requirements_web_dashboard.txt --force-reinstall
```

#### **3. Browser Compatibility**
- **Chrome**: Recommended (best performance)
- **Firefox**: Good compatibility
- **Safari**: Basic support
- **Edge**: Good compatibility

#### **4. Performance Issues**
- **Close other applications** to free up memory
- **Use smaller year ranges** for faster filtering
- **Restart the dashboard** if it becomes slow

### **Error Messages**

#### **"No government plans report found"**
- Ensure BASE scenario has been run first
- Check data/reports/` directory for Excel files
- Verify file naming convention

#### **"Missing required package"**
- Install dependencies: `pip install -r requirements_web_dashboard.txt`
- Check Python version compatibility
- Verify pip installation

#### **"Port 8501 is already in use"**
- Use different port: `streamlit run create_web_dashboard.py --server.port 8502`
- Kill existing process: `lsof -ti:8501 | xargs kill -9`

## 🔒 **Security Considerations**

### **Local Development**
- **Firewall**: Ensure port 8501 is not exposed externally
- **Network**: Limit access to local network if needed
- **Authentication**: Consider adding login for production use

### **Production Deployment**
- **HTTPS**: Use SSL certificates for secure access
- **Authentication**: Implement user login system
- **Access Control**: Restrict access to authorized users
- **Monitoring**: Log access and usage patterns

## 📈 **Performance Optimization**

### **Data Loading**
- **Lazy Loading**: Load data only when needed
- **Caching**: Implement data caching for faster access
- **Compression**: Compress large datasets

### **Chart Rendering**
- **Limit Data Points**: Show reasonable number of data points
- **Progressive Loading**: Load charts progressively
- **Optimization**: Use efficient chart libraries

## 🎯 **Use Cases**

### **Policy Makers**
- **Scenario Analysis**: Compare different energy futures
- **Investment Planning**: Understand financial requirements
- **Target Assessment**: Evaluate renewable energy goals
- **Policy Development**: Inform energy policy decisions

### **Researchers**
- **Data Analysis**: Explore detailed model results
- **Trend Analysis**: Identify patterns and trends
- **Sensitivity Analysis**: Test different assumptions
- **Publication**: Generate charts for reports

### **Stakeholders**
- **Presentation**: Professional visualizations for meetings
- **Communication**: Share insights with stakeholders
- **Decision Support**: Inform strategic decisions
- **Monitoring**: Track progress over time

## 🔮 **Future Enhancements**

### **Planned Features**
- **Real-time Updates**: Live data integration
- **Advanced Analytics**: Statistical analysis tools
- **Scenario Comparison**: Side-by-side scenario analysis
- **Export Options**: PDF reports, PowerPoint slides

### **User Experience**
- **Dark Mode**: Alternative color scheme
- **Customizable Layout**: User-defined dashboard layout
- **Notifications**: Alert system for important changes
- **Collaboration**: Multi-user editing capabilities

## 📞 **Support and Contact**

### **Technical Support**
- **Documentation**: Check this README first
- **Issues**: Review troubleshooting section
- **Updates**: Check for latest versions

### **Feature Requests**
- **Suggestions**: Submit enhancement ideas
- **Feedback**: Share user experience feedback
- **Contributions**: Contribute code improvements

## 📄 **License and Attribution**

### **Open Source**
- **License**: MIT License
- **Contributions**: Welcome from the community
- **Attribution**: Credit PakistanTIMES development team

### **Data Sources**
- **Government Plans**: Planning Commission, WAPDA, CPEC
- **Model Results**: PakistanTIMES energy model
- **Historical Data**: World Bank, PBS, Energy Yearbook

---

**🇵🇰 PakistanTIMES Interactive Web Dashboard**  
*Empowering Pakistan's Energy Future Through Interactive Analysis*  
*Generated on: 2025-08-24*  
*Version: 1.0*
