import keras
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras import layers
import tensorflow as tf




st.title("Energy market prices in Spain")
st.header("Predicting the price of electricity")


# Relative route to the CSV file
csv_file = "../data/df_yearly_prices.csv"  


try:
    df = pd.read_csv(csv_file)
    df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
    df['datetime'] = df['datetime'].dt.tz_localize(None)

    

    min_date = df['datetime'].min()
    max_date = df['datetime'].max()

    # Predetermined values for the date range filter
    pred_start_date = min_date
    pred_end_date = max_date

    start_date = st.date_input("Start date", min_value=min_date.date(), max_value=max_date.date(), value=pred_start_date.date())
    end_date = st.date_input("End Date", min_value=min_date.date(), max_value=max_date.date(), value=pred_end_date.date())

    # Convert the dates to datetime format
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the dataframe by date
    df_filter = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

    model = tf.keras.models.load_model('../data/model/model.keras')

    y_pred = model.predict(df_filter['value'])

    df_predictions = pd.DataFrame({'Date': df_filter['datetime'], 'Prediction': y_pred.flatten()})


    col1, col2 = st.columns(2)



    # Show the predictions
    with col1:
        st.subheader("Precios para 2023:")
        st.write(df_predictions)

    with col2:
        # create dataframe with min, max, mean, median and std of the predictions.structure [5,1]
        df_predictions_stats = pd.DataFrame({'Min': df_predictions['Prediction'].min(),
                                                'Max': df_predictions['Prediction'].max(),
                                                'Mean': df_predictions['Prediction'].mean(),
                                                'Median': df_predictions['Prediction'].median(),
                                                'Std': df_predictions['Prediction'].std()}, index=[0])
        # Columns to rows
        df_predictions_stats = df_predictions_stats.transpose()                            
        st.subheader("Statistics:")
        st.write(df_predictions_stats)



        avg_day = df_predictions.groupby('Date')['Prediction'].mean().reset_index()
        monthly_avg = df_predictions.groupby(df_predictions['Date'].dt.month)['Prediction'].mean().reset_index()

    fig, ax = plt.subplots()
    ax.scatter(avg_day["Date"], avg_day['Prediction'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title('Average price')
                
    plt.xticks(rotation=45)
    st.subheader("Scatter plot graph:")
    st.pyplot(fig)

except FileNotFoundError:
    st.write("The CSV file is nos in the specified route:", csv_file)
except Exception as e:
    st.write("Error while loading the file:", str(e))

