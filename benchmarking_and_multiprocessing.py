import multiprocessing
import random
import pandas as pd
from datetime import datetime
import time

def generate_sales_data(num_records):
    data = {
        'SaleID': range(1, num_records + 1),
        'Product': [random.choice(['ProductA', 'ProductB', 'ProductC']) for _ in range(num_records)],
        'Quantity': [random.randint(1, 10) for _ in range(num_records)],
        'Price': [random.uniform(10.0, 100.0) for _ in range(num_records)],
        'SaleDate': [datetime.now() for _ in range(num_records)]
    }
    return pd.DataFrame(data)

def process_chunk(chunk):
    print(f"Processing chunk with {len(chunk)} records...")
    result = chunk.groupby('Product')['Price'].sum().to_dict()
    return result

def process_data_single_thread(sales_data):
    print("Processing data in single thread...")
    start_time = time.time()
    result = process_chunk(sales_data)
    end_time = time.time()
    print(f"Total Sales Per Product in single thread:")
    for product, sales in result.items():
        print(f"{product}: ${sales:.2f}")
    print(f"Time taken in single thread: {end_time - start_time:.2f} seconds")

def process_data_multi_thread(sales_data, chunks, num_workers):
    print(f"Processing data using {num_workers} workers...")
    start_time = time.time()
    with multiprocessing.Pool(processes=num_workers) as pool:
        results = pool.map(process_chunk, chunks)
    end_time = time.time()

    # Combine the results from all workers
    total_sales = {}
    for result in results:
        for product, sales in result.items():
            total_sales[product] = total_sales.get(product, 0) + sales

    print("Total Sales Per Product with multiprocessing:")
    for product, sales in total_sales.items():
        print(f"{product}: ${sales:.2f}")
    print(f"Time taken with multiprocessing: {end_time - start_time:.2f} seconds")

def main():
    num_records = 1000000  # Number of sales records to simulate
    # num_workers = multiprocessing.cpu_count()  # Number of worker processes
    num_workers = 2  # Manually setting the number of worker processes

    print(f"Generating {num_records} sales records...")
    sales_data = generate_sales_data(num_records)

    # Split the dataset into chunks for parallel processing
    chunk_size = len(sales_data) // num_workers
    chunks = [sales_data.iloc[i:i + chunk_size] for i in range(0, len(sales_data), chunk_size)]

    # Process data in a single thread
    process_data_single_thread(sales_data)

    # Process data using multiprocessing
    process_data_multi_thread(sales_data, chunks, num_workers)

if __name__ == "__main__":
    main()
