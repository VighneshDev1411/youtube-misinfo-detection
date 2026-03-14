"""
YouTube Data Collection Script
Collects video metadata and comments using the YouTube Data API v3.
Uses existing channel IDs from sample_data/channel_data.json.
"""

import json
import os
import time
import csv
import sys
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ── Config ───────────────────────────────────────────────────────────────────
API_KEY = "AIzaSyAt9FePZjpfUwzE0wM1bMXDFdW3LjatSLA"
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "collected_data"
DATA_DIR.mkdir(exist_ok=True)

# Output files
VIDEOS_FILE = DATA_DIR / "video_data.csv"
COMMENTS_FILE = DATA_DIR / "comments.csv"
PROGRESS_FILE = DATA_DIR / "progress.json"

# API quota: 10,000 units/day
# search.list = 100 units, videos.list = 1 unit, commentThreads.list = 1 unit
# Strategy: use channels.list + playlistItems.list (cheaper) instead of search

youtube = build("youtube", "v3", developerKey=API_KEY)

# ── Progress tracking ────────────────────────────────────────────────────────
def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"completed_channels": [], "video_count": 0, "comment_count": 0, "quota_used": 0}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


# ── Video collection ─────────────────────────────────────────────────────────
def get_upload_playlist_id(channel_id):
    """Get the uploads playlist ID for a channel (costs 1 unit)."""
    try:
        resp = youtube.channels().list(
            part="contentDetails", id=channel_id
        ).execute()
        if resp.get("items"):
            return resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    except HttpError as e:
        if e.resp.status == 403:
            print(f"  QUOTA EXCEEDED. Stopping.")
            return "QUOTA_EXCEEDED"
        print(f"  Error getting playlist for {channel_id}: {e}")
    return None


def get_playlist_videos(playlist_id, max_results=50):
    """Get video IDs from a playlist (costs 1 unit per page)."""
    video_ids = []
    next_page = None
    pages = 0
    max_pages = 10  # cap at 500 videos per channel

    while pages < max_pages:
        try:
            resp = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page,
            ).execute()
            for item in resp.get("items", []):
                video_ids.append(item["contentDetails"]["videoId"])
            next_page = resp.get("nextPageToken")
            pages += 1
            if not next_page:
                break
        except HttpError as e:
            if e.resp.status == 403:
                return video_ids, "QUOTA_EXCEEDED"
            print(f"  Error fetching playlist: {e}")
            break

    return video_ids, pages


def get_video_details(video_ids):
    """Get video metadata in batches of 50 (costs 1 unit per call)."""
    all_videos = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        try:
            resp = youtube.videos().list(
                part="snippet,statistics",
                id=",".join(batch),
            ).execute()
            for item in resp.get("items", []):
                snippet = item["snippet"]
                stats = item.get("statistics", {})
                all_videos.append({
                    "channel_id": snippet.get("channelId", ""),
                    "channel_title": snippet.get("channelTitle", ""),
                    "video_id": item["id"],
                    "category_id": snippet.get("categoryId", ""),
                    "published_at": snippet.get("publishedAt", ""),
                    "title": snippet.get("title", ""),
                    "description": snippet.get("description", "")[:500],
                    "view_count": stats.get("viewCount", ""),
                    "like_count": stats.get("likeCount", ""),
                    "comment_count": stats.get("commentCount", ""),
                    "tags": "|".join(snippet.get("tags", [])),
                })
        except HttpError as e:
            if e.resp.status == 403:
                return all_videos, "QUOTA_EXCEEDED"
            print(f"  Error fetching video details: {e}")

    return all_videos, None


# ── Comment collection ───────────────────────────────────────────────────────
def get_comments(video_id, max_comments=100):
    """Get top-level comments for a video (costs 1 unit per page)."""
    comments = []
    next_page = None
    pages = 0
    max_pages = 2  # ~40-100 comments per video

    while pages < max_pages:
        try:
            resp = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page,
                textFormat="plainText",
                order="relevance",
            ).execute()
            for item in resp.get("items", []):
                c = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "video_id": video_id,
                    "comment_id": item["id"],
                    "comment_text": c.get("textDisplay", ""),
                    "author_name": c.get("authorDisplayName", ""),
                    "author_channel_id": c.get("authorChannelId", {}).get("value", ""),
                    "published_at": c.get("publishedAt", ""),
                    "like_count": c.get("likeCount", 0),
                })
            next_page = resp.get("nextPageToken")
            pages += 1
            if not next_page:
                break
        except HttpError as e:
            if e.resp.status == 403:
                if "commentsDisabled" in str(e):
                    break
                return comments, "QUOTA_EXCEEDED"
            break  # comments disabled or other error

    return comments, None


# ── CSV writers ──────────────────────────────────────────────────────────────
def init_csv(filepath, fieldnames):
    if not filepath.exists():
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

def append_csv(filepath, rows, fieldnames):
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(rows)


# ── Main collection loop ────────────────────────────────────────────────────
def main():
    # Load channel IDs
    with open(PROJECT_ROOT / "sample_data" / "channel_data.json") as f:
        channels = json.load(f)
    channel_ids = [c["channel_id"] for c in channels]
    print(f"Total channels: {len(channel_ids)}")

    # Load progress
    progress = load_progress()
    completed = set(progress["completed_channels"])
    remaining = [c for c in channel_ids if c not in completed]
    print(f"Already completed: {len(completed)}")
    print(f"Remaining: {len(remaining)}")
    print(f"Videos so far: {progress['video_count']}")
    print(f"Comments so far: {progress['comment_count']}")

    # Init CSVs
    video_fields = ["channel_id", "channel_title", "video_id", "category_id",
                    "published_at", "title", "description", "view_count",
                    "like_count", "comment_count", "tags"]
    comment_fields = ["video_id", "comment_id", "comment_text", "author_name",
                     "author_channel_id", "published_at", "like_count"]
    init_csv(VIDEOS_FILE, video_fields)
    init_csv(COMMENTS_FILE, comment_fields)

    quota_used = progress["quota_used"]
    QUOTA_LIMIT = 9500  # leave buffer

    for i, channel_id in enumerate(remaining):
        if quota_used >= QUOTA_LIMIT:
            print(f"\n--- Approaching daily quota limit ({quota_used} units used). Stopping. ---")
            print("Run the script again tomorrow to continue.")
            break

        print(f"\n[{i+1}/{len(remaining)}] Channel: {channel_id}")

        # Get uploads playlist
        playlist_id = get_upload_playlist_id(channel_id)
        quota_used += 1
        if playlist_id == "QUOTA_EXCEEDED":
            break
        if not playlist_id:
            progress["completed_channels"].append(channel_id)
            save_progress(progress)
            continue

        # Get video IDs from playlist
        video_ids, pages_or_error = get_playlist_videos(playlist_id)
        if pages_or_error == "QUOTA_EXCEEDED":
            break
        quota_used += pages_or_error if isinstance(pages_or_error, int) else 1
        print(f"  Found {len(video_ids)} videos")

        if not video_ids:
            progress["completed_channels"].append(channel_id)
            save_progress(progress)
            continue

        # Get video details
        videos, error = get_video_details(video_ids)
        quota_used += (len(video_ids) + 49) // 50
        if error == "QUOTA_EXCEEDED":
            break
        if videos:
            append_csv(VIDEOS_FILE, videos, video_fields)
            progress["video_count"] += len(videos)
            print(f"  Saved {len(videos)} video details")

        # Get comments for each video (sample up to 20 videos per channel)
        comment_videos = video_ids[:20]
        total_comments = 0
        for vid in comment_videos:
            comments, error = get_comments(vid)
            quota_used += 1
            if error == "QUOTA_EXCEEDED":
                break
            if comments:
                append_csv(COMMENTS_FILE, comments, comment_fields)
                total_comments += len(comments)

            if quota_used >= QUOTA_LIMIT:
                break

        progress["comment_count"] += total_comments
        progress["quota_used"] = quota_used
        progress["completed_channels"].append(channel_id)
        save_progress(progress)
        print(f"  Saved {total_comments} comments | Quota used: ~{quota_used}")

        # Small delay to be nice to the API
        time.sleep(0.1)

    # Final summary
    print(f"\n{'='*50}")
    print(f"Collection complete for this run!")
    print(f"Videos collected: {progress['video_count']}")
    print(f"Comments collected: {progress['comment_count']}")
    print(f"Channels completed: {len(progress['completed_channels'])}/{len(channel_ids)}")
    print(f"Estimated quota used: ~{quota_used}")
    if quota_used >= QUOTA_LIMIT:
        print(f"\nQuota limit reached. Run again tomorrow to continue.")
    save_progress(progress)


if __name__ == "__main__":
    main()
