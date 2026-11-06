import streamlit as st
import pandas as pd
import numpy as np

st.title("Development of an Interactive Educational Tool for Kinetic Modeling and Diffusivity Analysis in Thin-Layer Drying Processes")

# 1. RAW USER DATA
st.header("1. Raw User Data")
st.write("Upload your time and weight data [csv/excel].")

uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Read the file based on extension
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.write("Raw Data Preview:")
    
    # --- STYLE THE FIRST TABLE ---
    # Applies a soft blue background with black text to the preview table
    styled_preview = df.head().style.set_properties(**{
        'background-color': '#E8F0FE', 
        'color': 'black',
        'border-color': 'white'
    })
    st.dataframe(styled_preview, use_container_width=True)

    # 2. Calculate Mt, MR, DR
    st.header("2. Calculate Mt, MR, DR")
    
    # User input for Dry Bone Weight only
    dry_weight = st.number_input("Enter Dry Bone Weight (Wd):", min_value=0.001, value=1.000)
    
    # --- EDUCATIONAL INFO DROPDOWN ---
    with st.expander("ℹ️ How are these calculated?"):
        st.markdown("""
        **1. Moisture Content, Dry Basis ($M_t$)**
        Calculates the ratio of water mass to dry solid mass at any given time.
        """)
        st.latex(r"M_t = \frac{W_t - W_d}{W_d}")
        st.markdown("""
        * $W_t$ = Weight of sample at time $t$
        * $W_d$ = Dry bone weight of the sample. *(Obtained by drying the sample completely, typically in an oven at 105°C, until no further weight change occurs).*
        
        **2. Moisture Ratio ($MR$)**
        Calculates the proportion of removable moisture still left in the sample. The standard equation includes the Equilibrium Moisture Content ($M_e$):
        """)
        st.latex(r"MR = \frac{M_t - M_e}{M_0 - M_e}")
        st.markdown("""
        However, in practical thin-layer drying experiments using continuous high-temperature convective hot air, $M_e$ is often extremely small and considered negligible ($M_e \\approx 0$). Therefore, the equation simplifies to:
        """)
        st.latex(r"MR = \frac{M_t}{M_0}")
        st.markdown("""
        * $M_t$ = Moisture content at time $t$
        * $M_0$ = Initial moisture content (at $t=0$)
        * $M_e$ = Equilibrium moisture content (assumed to be 0)
        
        **3. Drying Rate ($DR$)**
        Measures the speed of moisture loss over a specific time interval.
        """)
        st.latex(r"DR = -\frac{\Delta M_t}{\Delta t}")
    # -----------------------------------

    if st.button("Calculate Data"):
        try:
            # Calculate Moisture Content (Mt) - Dry Basis
            df['Mt'] = (df['weight'] - dry_weight) / dry_weight
            
            # Calculate Moisture Ratio (MR) - Assuming Me is negligible (Mt / M0)
            M0 = df['Mt'].iloc[0] # Initial moisture content at t=0
            df['MR'] = df['Mt'] / M0
            
            # Calculate Drying Rate (DR)
            df['DR'] = -df['Mt'].diff() / df['time'].diff()
            df['DR'] = df['DR'].fillna(0) # Fill the first row NaN with 0
            
            st.success("Calculations complete!")
            st.write("Calculated Data Table:")
            
            # --- STYLE THE CALCULATED TABLE ---
            # Applies the same professional blue background to the final results
            styled_results = df.style.set_properties(**{
                'background-color': '#E8F0FE', 
                'color': 'black',
                'border-color': 'white'
            })
            st.dataframe(styled_results, use_container_width=True)
            
        except KeyError:
            st.error("Error: Please ensure your uploaded file has columns named exactly 'time' and 'weight'.")