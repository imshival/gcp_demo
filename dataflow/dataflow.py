# Standard imports
import argparse
import os
import csv
# Beam imports
import apache_beam as beam
from apache_beam.options.pipeline_options import GoogleCloudOptions, PipelineOptions, StandardOptions
from apache_beam.io import ReadFromText
from google.cloud import bigquery
from apache_beam.io.filesystems import FileSystems


def parse_file(element):
    for line in csv.reader([element], delimiter=','):
        return line


def original_method(values):
    row1 = dict(
        zip(('patient_id', 'last_name', 'first_name', 'address', 'city'),
            values))
    return row1


def run_pipeline(args, pipeline_args):
    """
    Runs the pipeline based on input arguments
    Parameters
        args: User-defined template arguments
        pipeline_args: Dataflow pipeline execution parameters
    """
    # Set pipeline options
    options = PipelineOptions(pipeline_args, save_main_session=True)
    options.view_as(GoogleCloudOptions)
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    # Initialize the pipeline
    p = beam.Pipeline(options=options)

    # Define pipeline steps
    lines = p | 'Read' >> ReadFromText(known_args.input_file_path, skip_header_lines=1) | 'Parse file' >> beam.Map(
        parse_file)
    originaldata = (lines | 'Ingesting Original Data for Big Query' >> beam.Map(lambda s: original_method(s))
                    | 'Writing Original Data to Big Query' >> beam.io.WriteToBigQuery(
                known_args.output_table_name,
                schema='SCHEMA_AUTODETECT',
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
                    )

    # Run pipeline
    p.run()


if __name__ == '__main__':
    # Get the pipeline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file_path',
                        type=str,
                        required=True,
                        help='Cloud Storage path to the input CSV file')
    parser.add_argument('--output_table_name',
                        type=str,
                        required=True,
                        help='name of the output table in format dataset.table_name')

    known_args, pipeline_args = parser.parse_known_args()
    # Execute pipeline
    run_pipeline(known_args, pipeline_args)