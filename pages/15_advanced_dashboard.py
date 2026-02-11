import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Chapter 15: Advanced Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Chapter 15: Advanced Investment ROI Dashboard")
st.markdown("---")

# Initialize session state for dynamic table
if 'investment_data' not in st.session_state:
    st.session_state.investment_data = {
        'FTF_Standalone': {
            'allocated': 2.5,
            'impactable_sales': 7.8,
            'roi': 2.1,
            'mroi': 1,
            'investment_in': -250,
            'investment_out': 490,
            'revenue_out': -319,
            'revenue_change': 4.1
        },
        'Speaker_Sequence_FTF': {
            'allocated': 0.8,
            'impactable_sales': 3.4,
            'roi': 3.2,
            'mroi': 1,
            'investment_in': -80,
            'investment_out': 490,
            'revenue_out': -289,
            'revenue_change': 8.5
        },
        'SRP': {
            'allocated': 1.1,
            'impactable_sales': 5.1,
            'roi': 3.6,
            'mroi': 1,
            'investment_in': -110,
            'investment_out': 490,
            'revenue_out': -200,
            'revenue_change': 4.1
        },
        'Remote_Telephone': {
            'allocated': 0.5,
            'impactable_sales': 2.6,
            'roi': 4.2,
            'mroi': 1,
            'investment_in': -50,
            'investment_out': 490,
            'revenue_out': -105,
            'revenue_change': 4.1
        }
    }

# Tabs
tab1, tab2, tab3 = st.tabs([
    "📈 Chart 1: Dual Axis",
    "📊 Chart 2: Waterfall",
    "📋 Chart 3: Dynamic Table"
])

# ============ TAB 1: DUAL AXIS CHART ============
with tab1:
    st.header("Chart 1: Revenue vs mROI (Dual Y-Axis)")
    
    st.info("💡 This chart shows Revenue and mROI on different scales using two Y-axes")
    
    # Sample data for dual axis chart
    cumulative_investment = np.linspace(0, 5, 50)
    
    # Revenue curve (increasing)
    revenue = 11.5 * (1 - np.exp(-1.5 * cumulative_investment))
    
    # mROI curve (decreasing)
    mroi_values = 2300 * np.exp(-2 * cumulative_investment)
    
    # Create dual axis chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add Revenue trace (left y-axis)
    fig.add_trace(
        go.Scatter(
            x=cumulative_investment,
            y=revenue,
            name="Revenue",
            line=dict(color='#666666', width=3),
            mode='lines'
        ),
        secondary_y=False,
    )
    
    # Add mROI trace (right y-axis)
    fig.add_trace(
        go.Scatter(
            x=cumulative_investment,
            y=mroi_values,
            name="mROI",
            line=dict(color='#D946EF', width=3),
            mode='lines'
        ),
        secondary_y=True,
    )
    
    # Update layout
    fig.update_xaxes(
        title_text="Cumulative Investment (€M)",
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128, 128, 128, 0.2)'
    )
    
    fig.update_yaxes(
        title_text="m. Impactable Sales ie (€M)",
        secondary_y=False,
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128, 128, 128, 0.2)',
        range=[0, 15]
    )
    
    fig.update_yaxes(
        title_text="mROI (%)",
        secondary_y=True,
        showgrid=False,
        range=[-500, 2500]
    )
    
    fig.update_layout(
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.15,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor='white',
        margin=dict(l=80, r=80, t=80, b=80)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Interactive controls
    st.subheader("🎛️ Adjust Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_investment = st.slider("Max Investment (€M)", 3.0, 10.0, 5.0, 0.5)
        revenue_growth = st.slider("Revenue Growth Factor", 8.0, 15.0, 11.5, 0.5)
    
    with col2:
        mroi_start = st.slider("Initial mROI (%)", 1000, 3000, 2300, 100)
        mroi_decay = st.slider("mROI Decay Rate", 1.0, 3.0, 2.0, 0.1)
    
    if st.button("🔄 Update Chart"):
        # Recalculate with new parameters
        cumulative_investment_new = np.linspace(0, max_investment, 50)
        revenue_new = revenue_growth * (1 - np.exp(-1.5 * cumulative_investment_new))
        mroi_values_new = mroi_start * np.exp(-mroi_decay * cumulative_investment_new)
        
        # Create new chart
        fig_new = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_new.add_trace(
            go.Scatter(x=cumulative_investment_new, y=revenue_new, name="Revenue",
                      line=dict(color='#666666', width=3)),
            secondary_y=False,
        )
        
        fig_new.add_trace(
            go.Scatter(x=cumulative_investment_new, y=mroi_values_new, name="mROI",
                      line=dict(color='#D946EF', width=3)),
            secondary_y=True,
        )
        
        fig_new.update_xaxes(title_text="Cumulative Investment (€M)")
        fig_new.update_yaxes(title_text="m. Impactable Sales ie (€M)", secondary_y=False)
        fig_new.update_yaxes(title_text="mROI (%)", secondary_y=True)
        fig_new.update_layout(height=500, hovermode='x unified', plot_bgcolor='white')
        
        st.plotly_chart(fig_new, use_container_width=True)

# ============ TAB 2: WATERFALL CHART ============
with tab2:
    st.header("Chart 2: Investment Waterfall Analysis")
    
    st.info("💡 Waterfall chart showing how investment flows across different channels")
    
    # Waterfall data
    channels = ['FTF Standalone', 'Speaker Sequence FTF', 'SRP', 'Remote Telephone']
    values = [7.8, 3.4, 5.1, 2.6]
    
    # Create figure
    fig_waterfall = go.Figure()
    
    # Add base bar (Total Budget - gray)
    fig_waterfall.add_trace(go.Bar(
        x=[''],
        y=[18.9],
        name='Total Budget',
        marker_color='#CCCCCC',
        text=['$18.9M'],
        textposition='outside',
        textfont=dict(size=14, color='black', family='Arial'),
        width=0.5,
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Calculate positions for waterfall
    base_positions = [18.9 - 7.8, 18.9 - 7.8 - 3.4, 18.9 - 7.8 - 3.4 - 5.1, 18.9 - 7.8 - 3.4 - 5.1 - 2.6]
    
    # Add waterfall bars (cyan)
    bar_texts = ['$7.8M', '$3.4M', '$5.1M', '$2.6M']
    
    for i, (channel, value, text, base) in enumerate(zip(channels, values, bar_texts, base_positions)):
        fig_waterfall.add_trace(go.Bar(
            x=[channel],
            y=[value],
            base=base,
            name=channel,
            marker_color='#5FD4D4',
            text=[text],
            textposition='outside',
            textfont=dict(size=14, color='black', family='Arial'),
            width=0.5,
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add connector line (dashed line from previous bar to current)
        if i == 0:
            # Line from Total Budget to first bar
            fig_waterfall.add_shape(
                type="line",
                x0=-0.3, y0=base_positions[0] + values[0],
                x1=0.7, y1=base_positions[0] + values[0],
                line=dict(color="gray", width=1, dash="dot")
            )
        else:
            # Line from previous bar to current bar
            fig_waterfall.add_shape(
                type="line",
                x0=i-0.3, y0=base_positions[i] + values[i],
                x1=i+0.7, y1=base_positions[i] + values[i],
                line=dict(color="gray", width=1, dash="dot")
            )
    
    # Update layout
    fig_waterfall.update_layout(
        yaxis_title="Impactable Sales ($M)",
        height=450,
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=80, r=50, t=50, b=20),
        xaxis=dict(
            showgrid=False,
            tickangle=0,  # Straight labels, not slanted
            tickfont=dict(size=11, family='Arial')
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(200, 200, 200, 0.3)',
            range=[0, 20]
        )
    )
    
    st.plotly_chart(fig_waterfall, use_container_width=True)
    
    # KPI Tables ALIGNED below chart (no markdown separator)
    # Create 5 columns: empty space, then 4 data columns aligned with bars
    col_spacer, col1, col2, col3, col4 = st.columns([1, 2, 2, 2, 2])
        
    # ============ UNIFIED TABLE BELOW CHART ============
    # Single table with metrics as rows and channels as columns
        
    st.markdown("<br>", unsafe_allow_html=True)  # Small spacing
        
    # Create the unified table using HTML for perfect alignment
    table_html = """
    <style>
        .kpi-table {
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
            font-size: 13px;
            margin-top: 10px;
        }
        .kpi-table td {
            padding: 8px 12px;
            text-align: center;
        }
        .kpi-table td:first-child {
            text-align: left;
            font-weight: normal;
            padding-left: 40px;
        }
        .kpi-table tr {
            border-bottom: 1px solid #e5e7eb;
        }
    </style>

    <table class="kpi-table">
        <tr>
            <td></td>
            <td><strong>FTF Standalone</strong></td>
            <td><strong>Speaker Sequence FTF</strong></td>
            <td><strong>SRP</strong></td>
            <td><strong>Remote Telephone</strong></td>
        </tr>
        <tr>
            <td>Impactable Sales</td>
            <td>$7.8M</td>
            <td>$3.4M</td>
            <td>$5.1M</td>
            <td>$2.6M</td>
        </tr>
        <tr>
            <td>Investment</td>
            <td>$2.5M</td>
            <td>$0.8M</td>
            <td>$1.1M</td>
            <td>$0.5M</td>
        </tr>
        <tr>
            <td>Margin Adj Revenue</td>
            <td>$6.2M</td>
            <td>$2.7M</td>
            <td>$4.1M</td>
            <td>$2.1M</td>
        </tr>
        <tr>
            <td>ROI</td>
            <td>2.1</td>
            <td>3.2</td>
            <td>3.6</td>
            <td>4.2</td>
        </tr>
        <tr>
            <td>mROI</td>
            <td>1</td>
            <td>1</td>
            <td>1.3</td>
            <td>2.5</td>
        </tr>
        <tr>
            <td>Touchpoints</td>
            <td>7000</td>
            <td>3000</td>
            <td>2000</td>
            <td>4200</td>
        </tr>
        <tr>
            <td>Avg Frequency</td>
            <td>7.0</td>
            <td>3.0</td>
            <td>2.0</td>
            <td>3.5</td>
        </tr>
    </table>
    """

    st.markdown(table_html, unsafe_allow_html=True)
# ============ TAB 3: DYNAMIC TABLE ============
with tab3:
    st.header("Chart 3: Dynamic Investment & Revenue Table")
    
    st.info("💡 Adjust investment inputs to see real-time changes in revenue outputs")
    
    # Calculate overall totals
    total_allocated = sum(data['allocated'] for data in st.session_state.investment_data.values())
    total_impactable = sum(data['impactable_sales'] for data in st.session_state.investment_data.values())
    total_inv_in = sum(data['investment_in'] for data in st.session_state.investment_data.values())
    total_inv_out = sum(data['investment_out'] for data in st.session_state.investment_data.values())
    total_rev_out = sum(data['revenue_out'] for data in st.session_state.investment_data.values())
    
    overall_roi = total_impactable / total_allocated if total_allocated > 0 else 0
    
    # Overall row
    st.markdown("### Overall Summary")
    
    with st.container(border=True):
        cols = st.columns([2, 1.5, 1.5, 1, 1, 2, 2, 1])
        
        with cols[0]:
            st.markdown("**Overall**")
        with cols[1]:
            st.metric("Allocated Investment", f"${total_allocated:.1f}M")
        with cols[2]:
            st.metric("Impactable Sales", f"${total_impactable:.1f}M")
        with cols[3]:
            st.metric("ROI", f"{overall_roi:.2f}")
        with cols[4]:
            st.write("**-**")
        with cols[5]:
            col_in, col_out = st.columns(2)
            with col_in:
                st.markdown(f"<span style='color: red;'>In: $-{abs(total_inv_in)}K</span>", unsafe_allow_html=True)
            with col_out:
                st.markdown(f"<span style='color: green;'>In: ${total_inv_out}K</span>", unsafe_allow_html=True)
        with cols[6]:
            st.markdown(f"<span style='color: red;'>Out: ${total_rev_out}K</span>", unsafe_allow_html=True)
        with cols[7]:
            # Overall bar
            bar_value = 3.8
            bar_color = '#DC2626'
            st.markdown(f"""
            <div style='display: flex; align-items: center; gap: 5px;'>
                <span style='font-size: 12px;'>{bar_value}%</span>
                <div style='width: 60px; height: 20px; background-color: {bar_color}; border-radius: 3px;'></div>
                <span style='font-size: 12px; color: green;'>0.5%</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Individual channel rows
    st.markdown("### Channel Details")
    
    channels = list(st.session_state.investment_data.keys())
    
    for channel in channels:
        data = st.session_state.investment_data[channel]
        
        with st.container(border=True):
            cols = st.columns([2, 1.5, 1.5, 1, 1, 2, 2, 1, 0.5])
            
            with cols[0]:
                st.markdown(f"**{channel.replace('_', ' ')}**")
            
            with cols[1]:
                st.write(f"${data['allocated']:.1f}M")
            
            with cols[2]:
                st.write(f"${data['impactable_sales']:.1f}M")
            
            with cols[3]:
                st.write(f"{data['roi']:.1f}")
            
            with cols[4]:
                st.write(f"{data['mroi']}")
            
            with cols[5]:
                # Investment Inputs with controls
                col_minus, col_val_in, col_plus, col_minus2, col_val_out, col_plus2 = st.columns([1, 3, 1, 1, 3, 1])
                
                with col_minus:
                    if st.button("−", key=f"{channel}_inv_in_minus", use_container_width=True):
                        st.session_state.investment_data[channel]['investment_in'] -= 10
                        st.rerun()
                
                with col_val_in:
                    inv_in_color = 'red' if data['investment_in'] < 0 else 'green'
                    st.markdown(f"<div style='text-align: center; color: {inv_in_color};'>In: ${data['investment_in']}K</div>", 
                               unsafe_allow_html=True)
                
                with col_plus:
                    if st.button("+", key=f"{channel}_inv_in_plus", use_container_width=True):
                        st.session_state.investment_data[channel]['investment_in'] += 10
                        st.rerun()
                
                with col_minus2:
                    if st.button("−", key=f"{channel}_inv_out_minus", use_container_width=True):
                        st.session_state.investment_data[channel]['investment_out'] -= 10
                        st.rerun()
                
                with col_val_out:
                    inv_out_color = 'red' if data['investment_out'] < 0 else 'green'
                    st.markdown(f"<div style='text-align: center; color: {inv_out_color};'>In: ${data['investment_out']}K</div>", 
                               unsafe_allow_html=True)
                
                with col_plus2:
                    if st.button("+", key=f"{channel}_inv_out_plus", use_container_width=True):
                        st.session_state.investment_data[channel]['investment_out'] += 10
                        st.rerun()
            
            with cols[6]:
                # Revenue Output (calculated from investment)
                # Simple formula: revenue_out = investment_in * roi + investment_out * 0.5
                calculated_revenue = (data['investment_in'] * data['roi'] + data['investment_out'] * 0.5)
                st.session_state.investment_data[channel]['revenue_out'] = int(calculated_revenue)
                
                rev_color = 'red' if calculated_revenue < 0 else 'green'
                st.markdown(f"<span style='color: {rev_color};'>Out: ${int(calculated_revenue)}K</span>", 
                           unsafe_allow_html=True)
            
            with cols[7]:
                # Bar visualization
                bar_color = '#DC2626'  # Red
                bar_width = min(abs(data['revenue_change']) * 10, 60)
                
                st.markdown(f"""
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <span style='font-size: 11px;'>{data['revenue_change']:.1f}%</span>
                    <div style='width: {bar_width}px; height: 18px; background-color: {bar_color}; border-radius: 2px;'></div>
                    <span style='font-size: 11px; color: green;'>Out: $0</span>
                </div>
                """, unsafe_allow_html=True)
            
            with cols[8]:
                # Edit icon
                st.markdown("✏️")
    
    st.markdown("---")
    
    # Reset button
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🔄 Reset All Values", use_container_width=True, type="secondary"):
            # Reset to default values
            st.session_state.investment_data = {
                'FTF_Standalone': {
                    'allocated': 2.5, 'impactable_sales': 7.8, 'roi': 2.1, 'mroi': 1,
                    'investment_in': -250, 'investment_out': 490, 'revenue_out': -319, 'revenue_change': 4.1
                },
                'Speaker_Sequence_FTF': {
                    'allocated': 0.8, 'impactable_sales': 3.4, 'roi': 3.2, 'mroi': 1,
                    'investment_in': -80, 'investment_out': 490, 'revenue_out': -289, 'revenue_change': 8.5
                },
                'SRP': {
                    'allocated': 1.1, 'impactable_sales': 5.1, 'roi': 3.6, 'mroi': 1,
                    'investment_in': -110, 'investment_out': 490, 'revenue_out': -200, 'revenue_change': 4.1
                },
                'Remote_Telephone': {
                    'allocated': 0.5, 'impactable_sales': 2.6, 'roi': 4.2, 'mroi': 1,
                    'investment_in': -50, 'investment_out': 490, 'revenue_out': -105, 'revenue_change': 4.1
                }
            }
            st.success("✅ Values reset to defaults!")
            st.rerun()
    
    # Instructions
    st.markdown("---")
    st.info("""
    **💡 How to use:**
    - Click **+** or **−** buttons to adjust investment inputs (red/green values)
    - Revenue outputs automatically recalculate based on formula: `Revenue = (Investment_In × ROI) + (Investment_Out × 0.5)`
    - The bar chart shows the revenue change percentage
    - Click **Reset** to restore default values
    """)

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 14 - Deployment")
with col2:
    st.success("🎉 **Advanced Dashboard Complete!**")