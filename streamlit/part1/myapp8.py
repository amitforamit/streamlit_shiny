import yfinance as yf
import streamlit as st
import pandas as pd
import altair as alt
import datetime
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from streamlit.components.v1 import html
from plotly import data
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Define your javascript
#my_js = """
#document.querySelectorAll(".css-6awftf.e19lei0e1").forEach(el => el.remove());
#"""

# Wrap the javascript as html code
#my_html = f"<script>{my_js}</script>"

#html(my_html)

df_raw = pd.read_csv("DATA_NEW.csv")
df_raw['Date']= pd.to_datetime(df_raw['Date'])
df_group = df_raw.groupby(["Date","Product","Division","Location","Machine"]).agg({"Availability":"mean", 
                                                                                  "Quality":"mean",
                                                                                  "Performance":"mean",
                                                                                  "Reject Reason":"mean",
                                                                                  "OEE" : "mean",
                                                                                  "Scheduled Units":"sum",
                                                                                  "Actual Units":"sum",
                                                                                  "Good Units":"sum",
                                                                                  "Scrap Units":"sum"}).round(2)
df_group.reset_index(inplace=True)
df_group['index'] = df_group['Date']
df_group.set_index('index',inplace=True)
df= df_group

#st.write(df)
st.title("Performance Dashboard")
#st.sidebar.title("Share Price analysis for May 2019 to May 2020:")
st.markdown("This application shows an overview of performance.")
ct = st.container()
col11, col21, col31,col41 =  ct.columns(4)
option1 = col11.selectbox(
    'Location',
    df['Location'].unique())
option2 = col21.selectbox(
    'Product',
    df['Product'].unique())
option3 = col31.selectbox(
    'Division',
    df['Division'].unique())
option4 = col41.multiselect(
    'Machine',
    sorted(df['Machine'].unique()),default=sorted(df['Machine'].unique())[0])


df1 = df[df['Machine'].isin(option4)]
stdate,enddate =  ct.columns(2)
start_date = pd.to_datetime(stdate.date_input(
    "Start Date",
    #datetime.datetime.today()- datetime.timedelta(days=7)
    df1['Date'].max()- datetime.timedelta(days=7)
    ))
end_date = pd.to_datetime(enddate.date_input(
    "End Date",
    #datetime.datetime.today()
    df1['Date'].max()
    ))


#st.write('You selected:', option1)

date_mask = (df1['Date'] >= start_date) & (df1['Date'] <= end_date)

df1 = df1[date_mask]

col12,col13,col14,col15 =  ct.columns(4)
col12.metric('Scheduled Units',df1['Scheduled Units'].sum())
col13.metric('Actual Units',df1['Actual Units'].sum())
col14.metric('Good Units',df1['Good Units'].sum())
col15.metric('Scrap Units',df1['Scrap Units'].sum())
col1, col2, col3 =  ct.columns(3)

line1 = alt.Chart(df1, title="Availability").mark_line(point=alt.OverlayMarkDef(color="red"),text='Availability').encode(alt.X('Date:T', axis=alt.Axis(format="%y/%m/%d")), y='Availability', color=alt.Color('Machine', legend=alt.Legend(
        orient='bottom',
        title=" ")))
label1 = alt.Chart(df1, title="Availability").mark_text(align= 'left',dx=4).encode(alt.X('Date:T', axis=alt.Axis(format="%y/%m/%d")), y='Availability',text = 'Availability')

c = alt.layer(line1, label1).resolve_scale(color='independent')
col1.altair_chart(c, use_container_width=True)

line2 = alt.Chart(df1, title="Performance").mark_line(point=alt.OverlayMarkDef(color="red")).encode(alt.X('Date:T', axis=alt.Axis(format="%y/%m/%d")), y='Performance',color=alt.Color('Machine', legend=alt.Legend(
        orient='bottom',
        title=" ")))
label2 = alt.Chart(df1, title="Performance").mark_text(align= 'left',dx=4).encode(alt.X('Date:T', axis=alt.Axis(format="%y/%m/%d")), y='Performance',text = 'Performance')

d = alt.layer(line2, label2).resolve_scale(color='independent')
col2.altair_chart(d, use_container_width=True)


lineoee = alt.Chart(df1, title="OEE").mark_line(point=alt.OverlayMarkDef(color="red"),text='OEE').encode(alt.X('Date:T', axis=alt.Axis(format="%y/%m/%d")), y='OEE', color=alt.Color('Machine', legend=alt.Legend(
        orient='bottom',
        title=" ")))
labeloee = alt.Chart(df1, title="OEE").mark_text(align= 'left',dx=4).encode(alt.X('Date:T', axis=alt.Axis(format="%y/%m/%d")), y='OEE',text = 'OEE')

col3a = alt.layer(lineoee, labeloee).resolve_scale(color='independent')
col3.altair_chart(col3a, use_container_width=True)

col6, col9 =  ct.columns(2)
col7,col8 = col9.columns([11,1])
col6_1,col6_2=  col6.columns([9,1])
chart_style_1 = col6_2.radio("this",['Quality', 'Reject Reason', 'Combined'],format_func=lambda x:"",label_visibility="hidden")

if chart_style_1 == "Quality":
    line3 = alt.Chart(df1, title="Quality").mark_line(point=alt.OverlayMarkDef(color="red")).encode(alt.X('Date:T', axis=alt.Axis(format="%y/%m/%d")), y='Quality',color=alt.Color('Machine', legend=alt.Legend(
            orient='bottom',
            title=" ")))
    label3 = alt.Chart(df1, title="Quality").mark_text(align= 'left',dx=4).encode(alt.X('Date:T', axis=alt.Axis(format="%y/%m/%d")), y='Quality',text = 'Quality')

    e = alt.layer(line3, label3).resolve_scale(color='independent')
    col6_1.altair_chart(e, use_container_width=True)
    
elif chart_style_1 == "Reject Reason":
    line3 = alt.Chart(
        df1, title="Reject Reason",width=40, height=195).mark_bar().encode(
                x =alt.X(
                    'Machine', sort = ["H4", "H5", "H6"],  axis=None), y='Reject Reason',column = alt.Column(
                    'Date', spacing = 0, header = alt.Header(labelOrient = "bottom"),title= None),color=alt.Color(
                    'Machine', legend=alt.Legend(
            orient='bottom',
            title=" ")))
    label3 = alt.Chart(df1, title="Reject Reason").mark_text(align= 'left',dx=4).encode(alt.X('Date:T', axis=alt.Axis(format="%y/%m/%d")), y='Reject Reason',text = 'Reject Reason')

    #e = alt.layer(line3, label3).resolve_scale(color='independent')
    col6_1.altair_chart(line3)


#bar_chart(pd.DataFrame(dict,index=[0,]))

chart_style_2 = col8.radio("this",['Performance', 'Availability', 'Quality'],key="rad1",format_func=lambda x:"",label_visibility="hidden")

if chart_style_2 == "Quality":
    lineQuality = alt.Chart(
        df1, title="Quality",width=45, height=195).mark_bar().encode(
                x =alt.X(
                    'Machine', sort = ["H4", "H5", "H6"],  axis=None), y='Quality',column = alt.Column(
                    'Date', spacing = 0, header = alt.Header(labelOrient = "bottom"),title= None),color=alt.Color(
                    'Machine', legend=alt.Legend(
            orient='bottom',
            title=" ")))
    labelQuality = alt.Chart(df1, title="Quality").mark_text(align= 'left',dx=4).encode(alt.X('Date:T', axis=alt.Axis(format="%y/%m/%d")), y='Quality',text = 'Quality')

    #e = alt.layer(lineQuality, labelQuality).resolve_scale(color='independent')
    col7.altair_chart(lineQuality)
elif chart_style_2 == "Availability":
    lineQuality = alt.Chart(
        df1, title="Availability",width=45, height=195).mark_bar().encode(
                x =alt.X(
                    'Machine', sort = ["H4", "H5", "H6"],  axis=None), y='Availability',column = alt.Column(
                    'Date', spacing = 0, header = alt.Header(labelOrient = "bottom"),title= None),color=alt.Color(
                    'Machine', legend=alt.Legend(
            orient='bottom',
            title=" ")))
    labelQuality = alt.Chart(df1, title="Availability").mark_text(align= 'left',dx=4).encode(alt.X('Date:T', axis=alt.Axis(format="%y/%m/%d")), y='Availability',text = 'Availability')

    #e = alt.layer(lineQuality, labelQuality).resolve_scale(color='independent')
    col7.altair_chart(lineQuality)
elif chart_style_2 == "Performance":
    lineQuality = alt.Chart(
        df1, title="Performance",width=45, height=195).mark_bar().encode(
                x =alt.X(
                    'Machine', sort = ["H4", "H5", "H6"],  axis=None), y='Performance',column = alt.Column(
                    'Date', spacing = 0, header = alt.Header(labelOrient = "bottom"),title= None),color=alt.Color(
                    'Machine', legend=alt.Legend(
            orient='bottom',
            title=" ")))
    labelQuality = alt.Chart(df1, title="Performance").mark_text(align= 'left',dx=4).encode(alt.X('Date:T', axis=alt.Axis(format="%y/%m/%d")), y='Performance',text = 'Performance')

    #e = alt.layer(lineQuality, labelQuality).resolve_scale(color='independent')
    col7.altair_chart(lineQuality)
#--------------
machine_color={
        "H4": "red",
        "H5": "green",
        "H6": "blue",
        "H7": "goldenrod",
        "H8": "magenta"}
fig = go.Figure(
    layout=dict(
        xaxis=dict(tickformat="%y/%m/%d"),
        yaxis=dict(range=[0, 100]),
        scattermode="group",
        legend=dict(groupclick="toggleitem",yanchor="top",
    y=1.50),
        title=go.layout.Title(text="A Combination Chart")
    )
)

fig.add_trace(
    go.Scatter(
        x=df1[df1['Machine']==option4[0]].Date,
        y=df1[df1['Machine']==option4[0]].Quality,
        #mode="markers",
        name=option4[0]+', '+"Quality",
        #marker_color=machine_color[option4[0]],
        marker=dict(color=machine_color[option4[0]], size=5),
        #offsetgroup=ft,
        #legendgroup=ft,
    )
)

fig.add_trace(
        go.Bar(
            x=df1[df1['Machine']==option4[0]].Date,
            y=df1[df1['Machine']==option4[0]].Performance,
            name= option4[0]+', '+"Performance",
            marker_color=machine_color[option4[0]],
            #offsetgroup=ft,
            #legendgroup=ft,
            #legendgrouptitle_text=ft,
        )
    )



for ft in option4[1:]:
    fig.add_trace(
        go.Scatter(
            x=df1[df1['Machine']==ft].Date,
            y=df1[df1['Machine']==ft].Quality,
            #mode="markers",
            name=ft+', '+"Quality",
            marker=dict(color=machine_color[ft], size=5),
            #offsetgroup=ft,
            #legendgroup=ft,
            #showlegend=False,
        )
    )

    fig.add_trace(
        go.Bar(
            x=df1[df1['Machine']==ft].Date,
            y=df1[df1['Machine']==ft].Performance,
            name=ft+', '+"Performance",
            marker_color=machine_color[ft],
            #offsetgroup=ft,
            #legendgroup=ft,
            #legendgrouptitle_text=ft,
        )
    )



config = {'displayModeBar': False}


#fig.show(config=config)
#ct3 = st.container()
#col100, col101 =  ct2.columns([1,1])

# Plot!
col_combo = ct.columns(1)
col_combo[0].plotly_chart(fig, use_container_width=True,config=config,theme="streamlit")




