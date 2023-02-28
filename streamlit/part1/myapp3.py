import yfinance as yf
import streamlit as st
import pandas as pd
import altair as alt
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("code\streamlit\part1\machine1.csv")
df['index'] = df['Time']
df= df.set_index('index')
st. set_page_config(layout="wide")
#st.write(df)
ct1 = st.container()
col11, col21, col31,col41 =  ct1.columns(4)
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
    df['Machine'].unique(),default=df['Machine'].unique()[0])

#st.write('You selected:', option1)
df1 = df[df['Machine'].isin(option4)]

ct = st.container()
col1, col2, col3 =  ct.columns(3)


line1 = alt.Chart(df1, title="Availability").mark_line(point=alt.OverlayMarkDef(color="red"),text='Availability').encode(x='Time', y='Availability', color=alt.Color('Machine', legend=alt.Legend(
        orient='bottom',
        title=" ")))
label1 = alt.Chart(df1, title="Availability").mark_text(align= 'left',dx=4).encode(x='Time', y='Availability',text = 'Availability')

c = alt.layer(line1, label1).resolve_scale(color='independent')
col1.altair_chart(c, use_container_width=True)

line2 = alt.Chart(df1, title="Performance").mark_line(point=alt.OverlayMarkDef(color="red")).encode(x='Time', y='Performance',color=alt.Color('Machine', legend=alt.Legend(
        orient='bottom',
        title=" ")))
label2 = alt.Chart(df1, title="Performance").mark_text(align= 'left',dx=4).encode(x='Time', y='Performance',text = 'Performance')

d = alt.layer(line2, label2).resolve_scale(color='independent')
col2.altair_chart(d, use_container_width=True)
col4,col5=col3.columns([9,1])
chart_style_1 = col5.radio("this",['Quality', 'Reject Reason', 'Combined'],format_func=lambda x:"",label_visibility="hidden")

if chart_style_1 == "Quality":
    line3 = alt.Chart(df1, title="Quality").mark_line(point=alt.OverlayMarkDef(color="red")).encode(x='Time', y='Quality',color=alt.Color('Machine', legend=alt.Legend(
            orient='bottom',
            title=" ")))
    label3 = alt.Chart(df1, title="Quality").mark_text(align= 'left',dx=4).encode(x='Time', y='Quality',text = 'Quality')

    e = alt.layer(line3, label3).resolve_scale(color='independent')
    col4.altair_chart(e, use_container_width=True)
    
elif chart_style_1 == "Reject Reason":
    line3 = alt.Chart(
        df1, title="Reject Reason",width=40, height=195).mark_bar().encode(
                x =alt.X(
                    'Machine', sort = ["H4", "H5", "H6"],  axis=None), y='Reject Reason',column = alt.Column(
                    'Time', spacing = 0, header = alt.Header(labelOrient = "bottom"),title= None),color=alt.Color(
                    'Machine', legend=alt.Legend(
            orient='bottom',
            title=" ")))
    label3 = alt.Chart(df1, title="Reject Reason").mark_text(align= 'left',dx=4).encode(x='Time', y='Reject Reason',text = 'Reject Reason')

    #e = alt.layer(line3, label3).resolve_scale(color='independent')
    col4.altair_chart(line3)
ct2 = st.container()
col6, col7, col8 =  ct2.columns(3)
col6.metric('Scheduled Units',df1['Scheduled Units'].sum())
col6.metric('Actual Units',df1['Actual Units'].sum())
col6.metric('Good Units',df1['Good Units'].sum())
col6.metric('Scrap Units',df1['Scrap Units'].sum())
vl= df1['Scheduled Units'].sum() 
dict = {}
dict["Scheduled Units"] = vl
print(dict)
pdf = pd.DataFrame(dict,index=[0,])
fig = px.scatter(
    pdf, x= None,y= None,range_x=None,range_y=None,labels=["Scheduled Units",]
)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)

col7.plotly_chart(fig, theme="streamlit", use_container_width=True)
#bar_chart(pd.DataFrame(dict,index=[0,]))
chart_style_1 = col5.radio("this",['Quality', 'Reject Reason', 'Combined'],format_func=lambda x:"",label_visibility="hidden")

if chart_style_1 == "Quality":
    line3 = alt.Chart(df1, title="Quality").mark_line(point=alt.OverlayMarkDef(color="red")).encode(x='Time', y='Quality',color=alt.Color('Machine', legend=alt.Legend(
            orient='bottom',
            title=" ")))
    label3 = alt.Chart(df1, title="Quality").mark_text(align= 'left',dx=4).encode(x='Time', y='Quality',text = 'Quality')

    e = alt.layer(line3, label3).resolve_scale(color='independent')
    col4.altair_chart(e, use_container_width=True)
    
elif chart_style_1 == "Reject Reason":
    line3 = alt.Chart(
        df1, title="Reject Reason",width=40, height=195).mark_bar().encode(
                x =alt.X(
                    'Machine', sort = ["H4", "H5", "H6"],  axis=None), y='Reject Reason',column = alt.Column(
                    'Time', spacing = 0, header = alt.Header(labelOrient = "bottom"),title= None),color=alt.Color(
                    'Machine', legend=alt.Legend(
            orient='bottom',
            title=" ")))
    label3 = alt.Chart(df1, title="Reject Reason").mark_text(align= 'left',dx=4).encode(x='Time', y='Reject Reason',text = 'Reject Reason')

    #e = alt.layer(line3, label3).resolve_scale(color='independent')
    col4.altair_chart(line3)





