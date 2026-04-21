# --------------PROGETTO FINALE----------------------


# --------------ESERCIZIO 1------------------------------
import pandas as pd
import glob
import time
import dask.dataframe as dd

# lettura singoli JSON, calcolo somma "amount" e ottimizzazione della RAM
t0 = time.time()

files = glob.glob("./data_local/json/transactions_part_*.jsonl")   # trova i files

dfs = []
total_amount = 0.0
for f in sorted(files):
    df_part = pd.read_json(f, lines=True)    # formato JSONL json line: 1 riga=1 record JSON
    partial_sum = df_part["amount"].sum()
    total_amount += partial_sum
    dfs.append(df_part)

df = pd.concat(dfs, ignore_index=True)

# ottimizzazione tipi
df["transaction_id"] = df["transaction_id"].astype("string")
df["customer_id"] = df["customer_id"].astype("int32")
df["product_id"] = df["product_id"].astype("int32")
df["region_id"] = df["region_id"].astype("int8")   # solo 5 valori
df["quantity"] = df["quantity"].astype("int8")     # valori interi da 1 a 5
df["amount"] = df["amount"].astype("float32")
df["ts"] = pd.to_datetime(df["ts"]).astype("datetime64[us]")   # spark supporta microsecondi(us) non nanosecondi(ns)
df["year"] = df["year"].astype("int16")
df["month"] = df["month"].astype("int8")    # valori interi da 1 a 12

t1 = time.time()

print(f"Totale importo: {total_amount:.2f}€")
print(f"Tempo di lettura file JSON ottimizzati: {t1 - t0:.2f} s")
print("RAM stimata (MB):", (df.memory_usage(deep=True).sum() / 1024 ** 2).round(2))

# lettura JSON con Dask e media degli importi
t2 = time.time()

ddf = dd.read_json("./data_local/json/transactions_part_*.jsonl", lines=True)   # lines necessario per file di tipo JSONL
media_importi = ddf.groupby("region_id")["amount"].mean().compute()

t3 = time.time()

print("\nMedia degli importi per regione con Dask: \n", media_importi.head())
print(f"Tempo di lettura e modifica file JSON con Dask: {t3 - t2:.2f} s\n")     
# su file di queste dimensioni conviene utilizzare Pandas
# Dask introduce overhead perchè pianifica grafo di esecuzione, deve far comunicare tra loro i worker e deve serializzare/desarializzare dati



# --------------ESERCIZIO 2------------------------------
from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast, col

# aggiunte config per attivazione Arrow (protocollo di trasferimento dati ad alta velocità)
# (necessario per evitare interruzioni che avevo nello scambio dati tra Pandas e Spark)
spark = SparkSession.builder \
    .appName("Pipeline_ETL") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.sql.execution.arrow.pyspark.fallback.enabled", "true") \
    .getOrCreate()

# pipeline ETL
# Extract
batch_files = glob.glob("./data_local/parquet/transactions_batch_*.parquet")  # recupero lista batch con glob
# problema con i ts del generator.py. Forzo da Pandas la conversione dei ts da nanosecondi (ns) a microsecondi (us) per evitare problema in Spark
pdf_list = [pd.read_parquet(f) for f in batch_files]
full_pdf = pd.concat(pdf_list, ignore_index=True)
for col in full_pdf.select_dtypes(include=['datetime64[ns]']).columns:
    full_pdf[col] = full_pdf[col].astype('datetime64[us]')

# creo df Spark partendo dai dati Pandas con ts in microsecondi
df_trans = spark.createDataFrame(full_pdf)

# lettura restanti file parquet
df_prod = spark.read.parquet("./data_local/parquet/products.parquet")
df_reg = spark.read.parquet("./data_local/parquet/regions.parquet")

# Transform
# ottimizzo il join con broadcast per evitare shuffle (spostamento di molti dati tra nodi) avendo df_trans 500_000 righe e df_prod 5_000 righe e df_prod 5 righe
df_joined = df_trans.join(broadcast(df_prod), on="product_id", how="left")  
df_joined = df_joined.join(broadcast(df_reg), on="region_id", how="left")

df_clean = df_joined.select("transaction_id", "region_name", "category", "amount", "year")

# Load
df_clean.write.mode("overwrite").partitionBy("year").parquet("./data_local/processed_sales")



# --------------ESERCIZIO 3------------------------------
from pyspark.sql.functions import sum
import matplotlib.pyplot as plt


# calcolo fatturato totale per categoria
df_transformed = df_clean.groupBy("category").agg(sum("amount").alias("total_amount"))

# salvataggio in Pandas
pdf_transformed = df_transformed.toPandas()


# bar chart
plt.figure(figsize=(10, 5))
plt.bar(pdf_transformed["category"], pdf_transformed["total_amount"], color="skyblue")
plt.title("Fatturato totale per categoria")
plt.xlabel("Categoria")
plt.xticks(rotation=45)    # ruoto per migliorare la leggibilità delle etichette
plt.ylabel("Fatturato (€)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("fatturato_per_categoria.png", dpi=300)
plt.show()



# --------------ESERCIZIO 4------------------------------

# monitoraggio live della cartella json
stream_df = spark.readStream.format("json").option("header", "true")\
    .schema("transaction_id STRING, customer_id INT, product_id INT, region_id INT, quantity INT, amount DOUBLE, ts TIMESTAMP, year INT, month INT")\
        .load("./data_local/json")

# calcolo in real-time
# il count() genera la nuova colonna count che rinomino in total_transactions
transformed_stream_df = stream_df.groupBy("region_id").count().withColumnRenamed("count", "total_transactions")

# output su console 
# outputmode: complete --> append non funziona con groupBY perchè legge solo i nuovi dati
query = transformed_stream_df.writeStream.outputMode("complete").format("console").option("truncate", False).start()

# programma in ascolto continuo
print("Streaming avviato... In attesa di nuovi file in ./data_local/json")
query.awaitTermination()











              





        