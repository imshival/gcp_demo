import csv
import io

import apache_beam as beam
from apache_beam.io import fileio, BigQueryDisposition
from apache_beam.options.pipeline_options import (
    PipelineOptions, GoogleCloudOptions, StandardOptions, SetupOptions)

DATASET = 'airbnb'

RAW_TABLE_NAME = 'raw_data'
RAW_TABLE_SCHEMA = {
    'fields': [
        {"name": "id", "type": "NUMERIC"},
        {"name": "name", "type": "STRING"},
        {"name": "host_id", "type": "NUMERIC"},
        {"name": "host_name", "type": "STRING"},
        {"name": "neighbourhood_group", "type": "STRING"},
        {"name": "neighbourhood", "type": "STRING"},
        {"name": "latitude", "type": "STRING"},
        {"name": "longitude", "type": "STRING"},
        {"name": "room_type", "type": "STRING"},
        {"name": "price", "type": "NUMERIC"},
        {"name": "minimum_nights", "type": "NUMERIC"},
        {"name": "number_of_reviews", "type": "NUMERIC"},
        {"name": "last_review", "type": "DATE"},
        {"name": "reviews_per_month", "type": "FLOAT"},
        {"name": "calculated_host_listings_count", "type": "NUMERIC"},
        {"name": "availability_365", "type": "NUMERIC", "mode": "NULLABLE"},
    ]
}

TOTAL_TABLE_NAME = 'total_data'
TOTAL_TABLE_SCHEMA = {
    'fields': [
        {"name": "neighbourhood", "type": "STRING"},
        {"name": "total", "type": "NUMERIC"},
    ]
}

CSV_FILE = 'gs://airbnb-dataset123/AB_NYC_2019.csv'

# Declare pipeline options
options = PipelineOptions()
google_cloud_options = options.view_as(GoogleCloudOptions)
google_cloud_options.project = 'prefab-envoy-300922'
google_cloud_options.region = 'us-central1'
google_cloud_options.job_name = 'load-airbnb-data'
google_cloud_options.staging_location = 'gs://airbnb-dataset123/dataflow_jobs/staging'
google_cloud_options.temp_location = 'gs://airbnb-dataset123/dataflow_jobs/temp'
options.view_as(StandardOptions).runner = 'DataflowRunner'
options.view_as(SetupOptions).save_main_session = True


class FormatDoFn(beam.DoFn):

    def process(self, element, *args, **kwargs):
        """
        :param element: tuple of neighbourhood and total values
        :return: dictionary
        """
        return [{
            'neighbourhood': element[0],
            'total': element[1]
        }]


with beam.Pipeline(options=options) as p:
    # Read csv file to data PCollection
    data = (p |
            "Find matched files" >> fileio.MatchFiles(CSV_FILE) |
            "Get files" >> fileio.ReadMatches() |
            "Read content" >> beam.FlatMap(
                lambda x: csv.DictReader(io.TextIOWrapper(x.open()))))

    # Store raw csv data to Big Query
    data | 'Write raw to BQ' >> beam.io.Write(beam.io.WriteToBigQuery(
        dataset=DATASET,
        table=RAW_TABLE_NAME,
        schema=RAW_TABLE_SCHEMA,
        write_disposition=BigQueryDisposition.WRITE_TRUNCATE,
        create_disposition=BigQueryDisposition.CREATE_IF_NEEDED))

    # Get totals by neighbourhood and store to BQ
    (data |
     'Group data' >> beam.GroupBy(lambda x: x["neighbourhood"]) |
     'Count neighbours' >> beam.CombineValues(beam.combiners.CountCombineFn()) |
     'Format values' >> beam.ParDo(FormatDoFn()) |
     'Write total to BQ' >> beam.io.Write(beam.io.WriteToBigQuery(
                dataset=DATASET,
                table=TOTAL_TABLE_NAME,
                schema=TOTAL_TABLE_SCHEMA,
                write_disposition=BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=BigQueryDisposition.CREATE_IF_NEEDED)))
