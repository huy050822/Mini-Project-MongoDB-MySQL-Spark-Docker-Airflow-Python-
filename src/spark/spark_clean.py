from config.logging_config import get_logger
from pyspark.sql import SparkSession
from pyspark.sql.functions import *



logger = get_logger("Spark_clean" , "app.log")



class Data_clean:

    def __init__(self, spark: SparkSession):

        self.spark  = spark

    def clean_data(self, df_raw):
        try:
            df_fact_events = df_raw.select(
                col("id").cast("long").alias("id"),
                col("type"),
                col("actor.id").cast("long").alias("actor_id"),
                col("repo.id").cast("long").alias("repo_id"),
                col("org.id").cast("long").alias("org_id"),
                col("public").cast("boolean").alias("is_public"),
                to_json(col("payload")).alias("payload"),
                col("created_at").cast("timestamp").alias("created_at"),
            ).dropDuplicates(["id"])


            df_actor = df_raw.select(
                    col("actor.id").cast("long").alias("id"),
                    col("actor.login").alias("login"),
                    col("actor.gravatar_id").alias("gravatar_id"),
                    col("actor.url").alias("url"),
                    col("actor.avatar_url").alias("avatar_url")).filter(col("id").isNotNull()).dropDuplicates(["id"])


            
            df_dim_repos = (
                df_raw.select(
                    col("repo.id").cast("long").alias("id"),
                    col("repo.name").alias("name"),
                    col("repo.url").alias("url"),
                )
                .filter(col("id").isNotNull())
                .dropDuplicates(["id"])
            )

            df_dim_orgs = (
                df_raw.select(
                    col("org.id").cast("long").alias("id"),
                    col("org.login").alias("login"),
                    col("org.gravatar_id").alias("gravatar_id"),
                    col("org.url").alias("url"),
                    col("org.avatar_url").alias("avatar_url"),
                )
                .filter(col("id").isNotNull())
                .dropDuplicates(["id"])
            )

            return df_actor, df_dim_repos, df_dim_orgs, df_fact_events

        
        except Exception as e:
            logger.error(f"Error during data cleaning: {str(e)}")
            raise e



