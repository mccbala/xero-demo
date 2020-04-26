echo Transforming JSON into single file
./transform_json.py
echo Loading the data into Google Bigquery
bq load --source_format=NEWLINE_DELIMITED_JSON xero-demo-mccbala:hubdoc.activity_log ./temp/2019-activity.log ./schema.json
