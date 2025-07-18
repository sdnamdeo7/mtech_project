# data_engineering.py

import pandas as pd
import boto3
import os

def load_csv_from_s3(bucket, file_key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=file_key)
    df = pd.read_csv(obj['Body'])
    return df

def transform_data(df):
    df['total_amount'] = df['quantity'] * df['price']
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['year'] = df['order_date'].dt.year
    df['month'] = df.order_date.dt.month
    df['day'] = df.order_date.dt.day
    return df

def save_to_local(df, path):
    df.to_csv(path, index=False)
    print(f"Data saved to {path}")

if __name__ == '__main__':
    BUCKET_NAME = 'my-bucket'
    FILE_KEY = 'data/orders.csv'
    OUTPUT_PATH = "outputs/orders_clean.csv"

    df = load_csv_from_s3(BUCKET_NAME, FILE_KEY)

    df_cleaned = transform_data(df)

    # Save data
    save_to_local(df_clean, OUTPUT_PATH)
