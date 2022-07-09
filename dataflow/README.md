
[comment]: <> (build command)

[comment]: <> (deploy build script to gcr.io)

deploy build script to gcr.io
gcloud builds submit --tag us-central1-docker.pkg.dev/stone-lodge-353709/gcs-bq/dataflow_script:latest .


[comment]: <> (build template command)
build template command

gcloud dataflow flex-template build gs://main_covid_storage_bucket/dataflow_templates/bqcsv.json --image=us-central1-docker.pkg.dev/stone-lodge-353709/gcs-bq/dataflow_script:latest --sdk-language=PYTHON --metadata-file=metadata.json



[comment]: <> (run job)

Run job 

gcloud dataflow flex-template run gcstobq \
--template-file-gcs-location=gs://main_covid_storage_bucket/dataflow_templates/bqcsv.json \
--parameters output_table_name=health_data.sampletable \
--parameters input_file_path=gs://ad_data_raw/api/test.csv \
--parameters temp_location=gs://ad_data_raw/temp \
--parameters service_account_email=ad-project-service-account@stone-lodge-353709.iam.gserviceaccount.com \
--region=us-east1 \
--project=stone-lodge-353709