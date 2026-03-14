# Channel, Video, and Comment Data README

This README provides an overview of the datasets for YouTube channels, videos, and comments. These datasets are organized into separate files, each containing specific information related to its respective entity.

# Data Organization

The data is structured into three primary categories:

* **Channels Data:** Information pertaining to individual YouTube channels.  
* **Videos Data:** Details about specific YouTube videos.  
* **Comments Data:** Content and metadata for comments made on YouTube videos.

# File Naming Convention

Each dataset is typically found in a CSV file, following a clear naming convention:

* `channels_data.csv`  
* `videos_data.csv`  
* `comments_data.csv`

# Dataset Details

## 1\. Channels Data (`channels_data.json`)

This file contains information about various YouTube channels. Each row represents a unique channel.

| Column Name | Description | Data Type | Example |
| :---- | :---- | :---- | :---- |
| `channel_id` | Unique identifier for the YouTube channel. | String | `UC-lHJZR3Gqxm24_Vd_D_KA` |
| `channel_name` | Name of the YouTube channel. | String | `PewDiePie` |
| `subscribers` | Number of subscribers the channel has. | Integer | `111000000` |
| `views` | Total views across all videos on the channel. | Integer | `30000000000` |
| `video_count` | Number of videos uploaded to the channel. | Integer | `4500` |
| `description` | Description provided by the channel owner. | String | `Just a guy and his videos.` |
| `country` | Country where the channel is based (if available). | String | `Sweden` |

## 2\. Videos Data (`videos_data.json`)

This file contains details about individual YouTube videos. Each row represents a unique video.

| Column Name | Description | Data Type | Example |
| :---- | :---- | :---- | :---- |
| `video_id` | Unique identifier for the YouTube video. | String | `dQw4w9WgXcQ` |
| `channel_id` | ID of the channel that uploaded the video. | String | `UC-lHJZR3Gqxm24_Vd_D_KA` |
| `title` | Title of the video. | String | `Never Gonna Give You Up` |
| `description` | Description of the video. | String | `Official music video...` |
| `published_at` | Date and time the video was published. | Timestamp | `2009-10-25T06:57:42Z` |
| `views` | Number of views the video has received. | Integer | `1200000000` |
| `likes` | Number of likes the video has received. | Integer | `15000000` |
| `comments` | Number of comments on the video. | Integer | `1500000` |
| `duration` | Duration of the video in ISO 8601 format. | String | `PT3M32S` |
| `tags` | Keywords associated with the video (comma-separated). | String | `music,rick astley,80s` |

## 3\. Comments Data (`commentsX.csv`)

This file contains information about comments made on YouTube videos. Each row represents a unique comment.

| Column Name | Description | Data Type | Example |
| :---- | :---- | :---- | :---- |
| `comment_id` | Unique identifier for the comment. | String | `Ugx-W-gX_3vW-m-p-Vd_D_KA` |
| `video_id` | ID of the video the comment was made on. | String | `dQw4w9WgXcQ` |
| `author_display_name` | Display name of the comment author. | String | `User123` |
| `published_at` | Date and time the comment was published. | Timestamp | `2023-01-15T10:30:00Z` |
| `text_display` | The actual text content of the comment. | String | `Great video!` |
| `like_count` | Number of likes the comment has received. | Integer | `10` |
| `reply_count` | Number of replies to the comment. | Integer | `2` |
| `parent_id` | If it's a reply, the ID of the parent comment. | String | `Ugx-W-gX_3vW-m-p-Vd_D_KA` |

# Usage Notes

* **Data Integrity:** While efforts are made to ensure data accuracy, occasional discrepancies may occur due to the dynamic nature of YouTube data.  
* **Missing Values:** Some fields may contain `null` or empty values if the information was not available at the time of data collection.  
* **Updates:** These datasets may be updated periodically. Please check the modification date of the files for the latest versions.

