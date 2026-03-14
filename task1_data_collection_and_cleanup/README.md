# Data Collection and Cleanup

This directory contains scripts and notebooks for collecting YouTube data from the YouTube Data API v3 and uploading it to Google Cloud Platform BigQuery for the YouTube Misinformation Classifier project.

## Structure

The data collection pipeline is organized into three main components:

### Channels (`channels/`)
- **`channel_data_collection.ipynb`**: Fetches channel metadata (channel details, statistics, branding info) from the YouTube API using channel IDs
- **`channel_data_to_gcp_bq.ipynb`**: Uploads collected channel data to Google BigQuery

### Videos (`videos/`)
- **`video_data_collection.ipynb`**: Collects video metadata (title, description, statistics, snippet info) from the YouTube API
- **`video_data_to_gcp_bq.ipynb`**: Uploads collected video data to Google BigQuery
- **`completed_ids.txt`**: Tracks successfully processed video IDs
- **`invalid_ids.txt`**: Tracks video IDs that failed validation or retrieval

### Comments (`comments/`)
- **`comments_data_collection.ipynb`**: Collects comment data from videos using asynchronous requests for efficient data retrieval
- **`comment_data_to_gcp_bq.ipynb`**: Uploads collected comment data to Google BigQuery
- **`all_video_ids.txt`**: Complete list of video IDs to process
- **`video_ids.txt`**: Validated video IDs for comment collection
- **`completed_ids.txt`**: Tracks video IDs that have been fully processed
- **`invalid_video_ids.txt`**: Tracks video IDs that failed during comment collection

## Requirements

- YouTube Data API v3 key
- Google Cloud Platform account with BigQuery access
- Python packages: `pandas`, `requests`, `google-cloud-bigquery`, `pandas-gbq`, `aiohttp`

## Usage

1. Configure your YouTube API key in the respective collection notebooks
2. Run the data collection notebooks to fetch data from the YouTube API
3. Run the corresponding BigQuery upload notebooks to store the collected data in GCP

## Notes

- The collection notebooks implement progress tracking to resume interrupted data collection
- Comment collection uses asynchronous requests to handle large-scale data collection efficiently
- All data is validated and cleaned before upload to BigQuery