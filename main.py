import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

st.title("Ineos Data Exploration")
st.markdown('Features vs failures reports')
st.markdown('------------------------------------------------------')

st.sidebar.header("Choose your features")

df = pd.read_pickle('df_for_st.pkl')

pump_list = df['pump_name'].unique().tolist()

pkpk = "Pk-Pk Waveform"
x1rpm = "1xRPM"
x2rpm = "2xRPM"
overall = "Overall Value"
sub = "SUBHARMONICS"
x34rpm = "3-4 x RPM"
x510rpm = "5-10 x RPM"
hfd = "HFD"
speed = "speed"

pkpk_select  = st.sidebar.checkbox(pkpk, False)
x1_select  = st.sidebar.checkbox(x1rpm, False)
x2_select  = st.sidebar.checkbox(x2rpm, False)
overall_select  = st.sidebar.checkbox(overall, False)
sub_select  = st.sidebar.checkbox(sub, False)
x34rpm_select  = st.sidebar.checkbox(x34rpm, False)
x510rpm_select  = st.sidebar.checkbox(x510rpm, False)
hfd_select  = st.sidebar.checkbox(hfd, False)
speed_select  = st.sidebar.checkbox(speed, False)

features_list_dico = {pkpk : pkpk_select, x1rpm : x1_select, x2rpm : x2_select,
overall: overall_select, sub: sub_select, x34rpm:x34rpm_select, x510rpm: x510rpm_select,
hfd: hfd_select, speed: speed_select}

ft_list_cho = []

for elem in features_list_dico:
    if features_list_dico[elem]:
        ft_list_cho.append(elem)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Pump selection")
    pump_selection = st.selectbox(
     '',
     pump_list)

df = df[df['pump_name'] == pump_selection]   
#mp_list = df['name'].unique().tolist()

df['mp_loc'] = df['name'].str[:2]
mp_list_loc = df['mp_loc'].unique().tolist()

with col2:
    st.subheader("MP selection")
    mp_selection = st.selectbox(
     '',
     mp_list_loc)

df['axis'] = df['name'].str[2:3]
axis_list = df['axis'].unique().tolist()

df_report = pd.read_pickle('df_report_melted.pkl')
df_report = df_report[df_report['Pumps'] == pump_selection]
report_type_list = df_report['variable'].unique().tolist()

with col3:
    st.subheader("Report selection")
    report_selection = st.selectbox(
     '',
     report_type_list)

df_report_gray = df_report[df_report['variable'] != report_selection]
df_report = df_report[df_report['variable'] == report_selection]

st.write('You selected:', str(pump_selection) + " & " + mp_selection + " & " + report_selection)


st.markdown('------------------------------------------------------')

#download_select  = st.checkbox("Display data", False)

graph_options = st.selectbox(
     'Graphical vizualisation?',
     ('Display 1 graph by axis', 'Select axis'))

if graph_options == 'Display 1 graph by axis': 

    df = df[df['label'].isin(ft_list_cho)]
    df = df[df['mp_loc'] == mp_selection]
    df.index = pd.to_datetime(df['date'])
    df = df.sort_index()

    for axis in axis_list:
        df_specific_axis = df[df['axis'] == axis]
        if axis == 'V':
            axis = '--> Vertical axis'
        elif axis == 'A':
            axis = '--> Axial axis'
        elif axis == 'H':
            axis = '--> Horizontal axis'
        elif axis == 'P':
            axis = '--> PeakVue'

        st.markdown('------------------------------------------------------')
        st.markdown(axis)
        
        fig = px.line(df_specific_axis, x=df_specific_axis.index, y="value", color = 'label')
        #datelist = ['09/19/18', '09/19/19']

        #Do filtering here

        datelist = df_report['Report_Date'].unique().tolist()
        datelist_gray = df_report_gray['Report_Date'].unique().tolist()

        for date in datelist_gray:
                datetime_str = str(date) #'09/19/18 13:55:26' #elem
                datetime_object = datetime.strptime(datetime_str, '%m/%d/%Y')
                fig.add_vline(x=datetime_object, line_width=1, line_dash="dash", line_color="gray")

        for date in datelist:
                datetime_str = str(date) #'09/19/18 13:55:26' #elem
                datetime_object = datetime.strptime(datetime_str, '%m/%d/%Y')
                fig.add_vline(x=datetime_object, line_width=2, line_dash="dash", line_color="green")

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        st.plotly_chart(fig, use_container_width=True)

elif graph_options == 'Select axis':
    axis_selection = st.selectbox(
     'Axis: ',
     axis_list)

    df = df[df['label'].isin(ft_list_cho)]
    df = df[df['mp_loc'] == mp_selection]
    df = df[df['axis'] == axis_selection]

    df.index = pd.to_datetime(df['date'])
    df = df.sort_index()

    fig = px.line(df, x=df.index, y="value", color = 'label')
    #datelist = ['09/19/18', '09/19/19']

    #Do filtering here

    datelist = df_report['Report_Date'].unique().tolist()
    datelist_gray = df_report_gray['Report_Date'].unique().tolist()

    for date in datelist_gray:
            datetime_str = str(date) #'09/19/18 13:55:26' #elem
            datetime_object = datetime.strptime(datetime_str, '%m/%d/%Y')
            fig.add_vline(x=datetime_object, line_width=1, line_dash="dash", line_color="gray")

    for date in datelist:
            datetime_str = str(date) #'09/19/18 13:55:26' #elem
            datetime_object = datetime.strptime(datetime_str, '%m/%d/%Y')
            fig.add_vline(x=datetime_object, line_width=2, line_dash="dash", line_color="green")

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    st.plotly_chart(fig, use_container_width=True)