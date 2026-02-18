import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Chapter 17: Advanced Charts",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Chapter 17: Advanced Interactive Charts")
st.markdown("---")

# Initialize session state for channel selection
if 'selected_channels' not in st.session_state:
    st.session_state.selected_channels = ['FTF_Standalone', 'SRP', 'Remote_Telephone']

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Response Curve",
    "🎯 More Advanced Charts",
    "💡 Learn",
    "🧪 Quiz"
])

# ============ TAB 1: RESPONSE CURVE ============
with tab1:
    st.header("Response Curve")
    st.caption("Relationship between sales and average frequency. Base case and scenario points are marked.")
    
    st.write("")
    
    # Channel selection and X-axis selection
    col_channels, col_spacer, col_xaxis = st.columns([6, 1, 2])
    
    with col_channels:
        st.markdown("**Channels**")
        
        # Create chip-style buttons for channel selection
        channels_data = {
            'FTF_Standalone': {'name': 'FTF_Standalone', 'color': '#8B5CF6'},
            'SRP': {'name': 'SRP', 'color': '#F97316'},
            'Remote_Telephone': {'name': 'Remote_Telephone', 'color': '#7C3AED'}
        }
        
        col1, col2, col3 = st.columns([1.5, 1, 2])
        
        with col1:
            # FTF_Standalone button
            if 'FTF_Standalone' in st.session_state.selected_channels:
                if st.button("● FTF_Standalone", key="ftf_btn", use_container_width=True, type="primary"):
                    st.session_state.selected_channels.remove('FTF_Standalone')
                    st.rerun()
            else:
                if st.button("○ FTF_Standalone", key="ftf_btn", use_container_width=True):
                    st.session_state.selected_channels.append('FTF_Standalone')
                    st.rerun()
        
        with col2:
            # SRP button
            if 'SRP' in st.session_state.selected_channels:
                if st.button("● SRP", key="srp_btn", use_container_width=True, type="primary"):
                    st.session_state.selected_channels.remove('SRP')
                    st.rerun()
            else:
                if st.button("○ SRP", key="srp_btn", use_container_width=True):
                    st.session_state.selected_channels.append('SRP')
                    st.rerun()
        
        with col3:
            # Remote_Telephone button
            if 'Remote_Telephone' in st.session_state.selected_channels:
                if st.button("● Remote_Telephone", key="remote_btn", use_container_width=True, type="primary"):
                    st.session_state.selected_channels.remove('Remote_Telephone')
                    st.rerun()
            else:
                if st.button("○ Remote_Telephone", key="remote_btn", use_container_width=True):
                    st.session_state.selected_channels.append('Remote_Telephone')
                    st.rerun()
    
    with col_xaxis:
        st.markdown("**X-Axis**")
        
        col_inv, col_freq = st.columns(2)
        
        with col_inv:
            investment_selected = st.button("Investment", key="x_investment", use_container_width=True, type="primary")
        
        with col_freq:
            frequency_selected = st.button("Avg. Frequency", key="x_frequency", use_container_width=True)
    
    st.markdown("---")
    
    # Generate response curve data
    x_values = np.linspace(0, 16, 100)
    
    # Different curves for each channel
    curves = {
        'FTF_Standalone': {
            'line': 5 + 55 * (1 - np.exp(-0.3 * x_values)),
            'base_point': (7, 35),
            'scenario_point': (13, 38),
            'color': '#8B5CF6'
        },
        'SRP': {
            'line': 3 + 45 * (1 - np.exp(-0.35 * x_values)),
            'base_point': (8, 29),
            'scenario_point': (13, 30),
            'color': '#F97316'
        },
        'Remote_Telephone': {
            'line': 2 + 40 * (1 - np.exp(-0.4 * x_values)),
            'base_point': (6, 28),
            'scenario_point': (10, 32),
            'color': '#7C3AED'
        }
    }
    
    # Create figure
    fig = go.Figure()
    
    # Add lines for selected channels
    for channel in st.session_state.selected_channels:
        if channel in curves:
            curve_data = curves[channel]
            
            # Add line
            fig.add_trace(go.Scatter(
                x=x_values,
                y=curve_data['line'],
                mode='lines',
                name=channel,
                line=dict(color=curve_data['color'], width=2.5),
                hovertemplate='<b>' + channel + '</b><br>X: %{x:.1f}<br>Sales: $%{y:.1f}M<extra></extra>'
            ))
            
            # Add base case point
            fig.add_trace(go.Scatter(
                x=[curve_data['base_point'][0]],
                y=[curve_data['base_point'][1]],
                mode='markers',
                name=f'{channel} (Base)',
                marker=dict(
                    color=curve_data['color'],
                    size=12,
                    symbol='circle',
                    line=dict(color='white', width=2)
                ),
                hovertemplate='<b>' + channel + ' (Base)</b><br>X: %{x:.1f}<br>Sales: $%{y:.1f}M<extra></extra>',
                showlegend=False
            ))
            
            # Add scenario point
            fig.add_trace(go.Scatter(
                x=[curve_data['scenario_point'][0]],
                y=[curve_data['scenario_point'][1]],
                mode='markers',
                name=f'{channel} (Scenario)',
                marker=dict(
                    color=curve_data['color'],
                    size=12,
                    symbol='circle',
                    line=dict(color='white', width=2)
                ),
                hovertemplate='<b>' + channel + ' (Scenario)</b><br>X: %{x:.1f}<br>Sales: $%{y:.1f}M<extra></extra>',
                showlegend=False
            ))
    
    # Update layout
    fig.update_layout(
        height=500,
        xaxis=dict(
            title="Avg. Frequency" if frequency_selected else "Investment",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(200, 200, 200, 0.3)',
            zeroline=False,
            range=[0, 16]
        ),
        yaxis=dict(
            title="m. Impactable Sales ($M)",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(200, 200, 200, 0.3)',
            zeroline=False,
            range=[0, 60]
        ),
        plot_bgcolor='white',
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="left",
            x=0
        ),
        margin=dict(l=60, r=40, t=40, b=80)
    )
    
    # Add legend items
    legend_items = []
    
    # Base Case
    legend_items.append(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color='#9CA3AF', symbol='circle'),
        name='Base Case',
        showlegend=True
    ))
    
    # Modelled Scenario
    legend_items.append(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color='#8B5CF6', symbol='circle'),
        name='Modelled Scenario',
        showlegend=True
    ))
    
    # Channel lines
    for channel in ['FTF_Standalone', 'SRP']:
        if channel in curves:
            legend_items.append(go.Scatter(
                x=[None], y=[None],
                mode='lines',
                line=dict(color=curves[channel]['color'], width=2.5),
                name=channel,
                showlegend=True
            ))
    
    for item in legend_items:
        fig.add_trace(item)
    
    # Display chart
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Additional info
    with st.expander("💡 How This Works"):
        st.markdown("""
        **Interactive Features:**
        - **Toggle Channels**: Click the colored buttons above to show/hide channel lines
        - **Hover on Lines**: See exact values at any point on the curve
        - **Hover on Points**: See Base Case vs Scenario values
        - **Switch X-Axis**: Toggle between Investment and Avg. Frequency
        
        **What It Shows:**
        - Relationship between frequency/investment and sales
        - Diminishing returns (curve flattens at high frequency)
        - Different response curves for each channel
        - Base case (current state) vs Scenario (optimized)
        """)

# ============ TAB 2: MORE CHARTS ============
with tab2:
    st.header("🎯 More Advanced Chart Examples")
    
    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Multi-Line with Annotations",
            "Stacked Area Chart",
            "Grouped Bar with Patterns",
            "Bubble Chart (3D Data)",
            "Heatmap with Annotations"
        ]
    )
    
    st.markdown("---")
    
    if chart_type == "Multi-Line with Annotations":
        # Multiple lines with text annotations
        
        x = np.arange(0, 12)
        
        fig = go.Figure()
        
        # Add multiple lines
        for i, (name, color) in enumerate([('Product A', '#3B82F6'), ('Product B', '#10B981'), ('Product C', '#F59E0B')]):
            y = 10 + i*5 + np.random.randn(12).cumsum()
            
            fig.add_trace(go.Scatter(
                x=x,
                y=y,
                mode='lines+markers',
                name=name,
                line=dict(color=color, width=2),
                marker=dict(size=8),
                hovertemplate=f'<b>{name}</b><br>Month: %{{x}}<br>Value: $%{{y:.1f}}M<extra></extra>'
            ))
            
            # Add annotation at peak
            peak_idx = np.argmax(y)
            fig.add_annotation(
                x=x[peak_idx],
                y=y[peak_idx],
                text=f"Peak: ${y[peak_idx]:.1f}M",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=color,
                bgcolor="white",
                bordercolor=color,
                borderwidth=2,
                font=dict(size=11)
            )
        
        fig.update_layout(
            title="Monthly Revenue by Product",
            xaxis_title="Month",
            yaxis_title="Revenue ($M)",
            height=500,
            hovermode='x unified',
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Stacked Area Chart":
        # Stacked area showing composition over time
        
        months = pd.date_range('2024-01', periods=12, freq='M')
        
        data = {
            'Digital': np.random.randint(20, 40, 12),
            'Field': np.random.randint(30, 50, 12),
            'Events': np.random.randint(10, 25, 12)
        }
        
        fig = go.Figure()
        
        colors = ['#8B5CF6', '#F97316', '#10B981']
        
        for i, (channel, values) in enumerate(data.items()):
            fig.add_trace(go.Scatter(
                x=months,
                y=values,
                mode='lines',
                name=channel,
                stackgroup='one',
                fillcolor=colors[i],
                line=dict(width=0.5, color=colors[i]),
                hovertemplate=f'<b>{channel}</b><br>%{{x|%b %Y}}<br>Value: %{{y}}<extra></extra>'
            ))
        
        fig.update_layout(
            title="Investment Mix Over Time",
            xaxis_title="Month",
            yaxis_title="Investment ($M)",
            height=500,
            hovermode='x unified',
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Grouped Bar with Patterns":
        # Grouped bar chart comparing channels
        
        channels = ['FTF', 'SRP', 'Remote', 'Digital']
        
        fig = go.Figure()
        
        # Q1 data
        fig.add_trace(go.Bar(
            x=channels,
            y=[45, 35, 28, 52],
            name='Q1 2024',
            marker_color='#8B5CF6',
            hovertemplate='<b>%{x}</b><br>Q1 2024: $%{y}M<extra></extra>'
        ))
        
        # Q2 data
        fig.add_trace(go.Bar(
            x=channels,
            y=[52, 38, 32, 58],
            name='Q2 2024',
            marker_color='#F97316',
            hovertemplate='<b>%{x}</b><br>Q2 2024: $%{y}M<extra></extra>'
        ))
        
        fig.update_layout(
            title="Sales by Channel - Quarterly Comparison",
            xaxis_title="Channel",
            yaxis_title="Sales ($M)",
            barmode='group',
            height=500,
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Bubble Chart (3D Data)":
        # Bubble chart with 3 dimensions
        
        np.random.seed(42)
        
        df_bubble = pd.DataFrame({
            'channel': ['FTF', 'SRP', 'Remote', 'Digital', 'Events'] * 4,
            'investment': np.random.uniform(5, 50, 20),
            'roi': np.random.uniform(1.5, 5.0, 20),
            'sales': np.random.uniform(10, 100, 20)
        })
        
        fig = go.Figure()
        
        colors = {'FTF': '#8B5CF6', 'SRP': '#F97316', 'Remote': '#7C3AED', 'Digital': '#10B981', 'Events': '#F59E0B'}
        
        for channel in df_bubble['channel'].unique():
            channel_data = df_bubble[df_bubble['channel'] == channel]
            
            fig.add_trace(go.Scatter(
                x=channel_data['investment'],
                y=channel_data['roi'],
                mode='markers',
                name=channel,
                marker=dict(
                    size=channel_data['sales'] * 0.5,
                    color=colors[channel],
                    opacity=0.6,
                    line=dict(width=2, color='white')
                ),
                hovertemplate=f'<b>{channel}</b><br>Investment: $%{{x:.1f}}M<br>ROI: %{{y:.1f}}<br>Sales: %{{marker.size:.0f}}M<extra></extra>'
            ))
        
        fig.update_layout(
            title="Investment vs ROI vs Sales (Bubble Size = Sales)",
            xaxis_title="Investment ($M)",
            yaxis_title="ROI",
            height=500,
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Heatmap with Annotations":
        # Heatmap showing ROI by channel and region
        
        channels = ['FTF', 'SRP', 'Remote', 'Digital']
        regions = ['North', 'South', 'East', 'West']
        
        # Generate data
        roi_data = np.random.uniform(1.5, 4.5, (len(regions), len(channels)))
        
        # Create annotations
        annotations = []
        for i, region in enumerate(regions):
            for j, channel in enumerate(channels):
                annotations.append(
                    dict(
                        x=channel,
                        y=region,
                        text=f"{roi_data[i, j]:.1f}",
                        showarrow=False,
                        font=dict(color='white' if roi_data[i, j] > 3 else 'black', size=13)
                    )
                )
        
        fig = go.Figure(data=go.Heatmap(
            z=roi_data,
            x=channels,
            y=regions,
            colorscale='RdYlGn',
            hovertemplate='<b>%{y} - %{x}</b><br>ROI: %{z:.2f}<extra></extra>',
            colorbar=dict(title="ROI")
        ))
        
        fig.update_layout(
            title="ROI Heatmap by Channel and Region",
            height=500,
            annotations=annotations
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============ TAB 3: LEARN ============
with tab3:
    st.header("💡 Advanced Chart Concepts")
    
    with st.expander("📊 Multi-Line Chart with Toggle", expanded=True):
        st.markdown("""
        **Response Curve Chart Features:**
        
        1. **Channel Selection (Chips)**
           - Click to toggle channels on/off
           - Each channel has its own color
           - Shows/hides the corresponding line
        
        2. **Multiple Lines**
           - Different response curves for each channel
           - Each line represents relationship between X and Y
        
        3. **Markers**
           - Circular points for Base Case
           - Circular points for Scenario
           - Different colors per channel
        
        4. **Hover Tooltips**
           - Shows exact values on hover
           - Channel name, X value, Y value
           - Custom formatted text
        
        5. **Interactive Legend**
           - Click to show/hide lines
           - Positioned at bottom
        """)
        
        st.code("""
import plotly.graph_objects as go

fig = go.Figure()

# Add line for each channel
for channel in selected_channels:
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        name=channel,
        line=dict(color=channel_color, width=2.5),
        hovertemplate='<b>' + channel + '</b><br>X: %{x:.1f}<br>Y: %{y:.1f}<extra></extra>'
    ))
    
    # Add base case point
    fig.add_trace(go.Scatter(
        x=[base_x],
        y=[base_y],
        mode='markers',
        marker=dict(size=12, color=channel_color),
        hovertemplate='<b>Base Case</b><br>X: %{x:.1f}<br>Y: %{y:.1f}<extra></extra>',
        showlegend=False
    ))

fig.update_layout(
    hovermode='closest',  # Hover on nearest point
    plot_bgcolor='white'
)

st.plotly_chart(fig, use_container_width=True)
        """, language="python")
    
    with st.expander("🎨 Custom Hover Templates"):
        st.markdown("""
        **Hover templates allow custom formatting:**
        
        ```python
        hovertemplate='<b>%{fullData.name}</b><br>X: %{x:.1f}<br>Y: $%{y:.2f}M<extra></extra>'
        ```
        
        **Template Variables:**
        - `%{x}` - X value
        - `%{y}` - Y value
        - `%{fullData.name}` - Trace name
        - `:.1f` - Format to 1 decimal place
        - `:.2f` - Format to 2 decimal places
        - `<extra></extra>` - Hide secondary box
        - `<br>` - Line break
        - `<b>text</b>` - Bold text
        """)
    
    with st.expander("🔘 Creating Toggle Buttons (Chips)"):
        st.code("""
import streamlit as st

# Initialize selected items
if 'selected_items' not in st.session_state:
    st.session_state.selected_items = ['Item1', 'Item2']

# Create toggle buttons
col1, col2, col3 = st.columns(3)

with col1:
    if 'Item1' in st.session_state.selected_items:
        # Selected state - primary button
        if st.button("● Item1", type="primary"):
            st.session_state.selected_items.remove('Item1')
            st.rerun()
    else:
        # Unselected state - regular button
        if st.button("○ Item1"):
            st.session_state.selected_items.append('Item1')
            st.rerun()

# Then use selected_items to filter data
if 'Item1' in st.session_state.selected_items:
    # Show Item1 data
    pass
        """, language="python")
    
    with st.expander("📍 Adding Points/Markers"):
        st.code("""
# Add scatter points on top of line
fig.add_trace(go.Scatter(
    x=[point_x],
    y=[point_y],
    mode='markers',
    name='Special Point',
    marker=dict(
        size=12,
        color='red',
        symbol='circle',  # Options: circle, square, diamond, cross, etc.
        line=dict(color='white', width=2)  # White outline
    ),
    hovertemplate='<b>Point Name</b><br>Value: %{y:.2f}<extra></extra>'
))
        """, language="python")

# ============ TAB 4: QUIZ ============
with tab4:
    st.header("🧪 Knowledge Check")
    
    q1 = st.radio(
        "Q1: How to show exact values on hover?",
        [
            "Add text annotations",
            "Use hovertemplate parameter",
            "Use title parameter"
        ]
    )
    
    q2 = st.radio(
        "Q2: What's the best way to toggle chart elements?",
        [
            "Use session state + conditional rendering",
            "Create separate charts",
            "Use CSS display none"
        ]
    )
    
    q3 = st.radio(
        "Q3: For smooth curves, you should:",
        [
            "Use few data points",
            "Use many data points (100+)",
            "Data points don't matter"
        ]
    )
    
    q4 = st.checkbox("Q4: hovermode='closest' shows tooltip for nearest point")
    
    q5 = st.radio(
        "Q5: To add marker points on a line, use:",
        [
            "mode='lines'",
            "mode='markers'",
            "Add separate scatter trace"
        ]
    )
    
    if st.button("✅ Check Answers", type="primary"):
        score = 0
        feedback = []
        
        if q1 == "Use hovertemplate parameter":
            score += 1
            feedback.append("✅ Q1: Correct!")
        else:
            feedback.append("❌ Q1: Use hovertemplate")
        
        if q2 == "Use session state + conditional rendering":
            score += 1
            feedback.append("✅ Q2: Correct!")
        else:
            feedback.append("❌ Q2: Use session state to track selections")
        
        if q3 == "Use many data points (100+)":
            score += 1
            feedback.append("✅ Q3: Correct! More points = smoother")
        else:
            feedback.append("❌ Q3: Use 100+ points for smooth curves")
        
        if q4:
            score += 1
            feedback.append("✅ Q4: Correct!")
        else:
            feedback.append("❌ Q4: hovermode='closest' shows nearest")
        
        if q5 == "Add separate scatter trace":
            score += 1
            feedback.append("✅ Q5: Correct!")
        else:
            feedback.append("❌ Q5: Add separate scatter trace for markers")
        
        st.markdown("---")
        st.write(f"### 🎯 Score: {score}/5")
        
        for fb in feedback:
            st.write(fb)
        
        if score == 5:
            st.success("🎉 Perfect! You mastered advanced charts!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Good! Review interactive features.")
        else:
            st.warning("📖 Please review chart concepts.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 16 - Databricks Integration")
with col2:
    st.success("✅ **Advanced Charts Complete!**")