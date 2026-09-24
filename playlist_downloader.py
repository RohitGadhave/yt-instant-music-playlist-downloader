import yt_dlp
import os
import re

def download_playlist_as_mp3(playlist_url):
    print("Fetching playlist information... Please wait.")
    
    # 1. Fetch flat playlist info to get all items without downloading yet
    ydl_opts_flat = {
        'extract_flat': 'in_playlist',
        'quiet': True,
        'ignoreerrors': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts_flat) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        
    if not info or 'entries' not in info:
        print("❌ Could not retrieve playlist info. Make sure the playlist is public.")
        return

    playlist_title = info.get('title', 'Unknown_Playlist')
    entries = list(info['entries'])
    total_items = len(entries)
    
    # Create a safe folder name from the playlist title
    safe_folder_name = re.sub(r'[\\/*?:"<>|]', "", playlist_title).strip()
    os.makedirs(safe_folder_name, exist_ok=True)
    
    log_filename = os.path.join(safe_folder_name, "download_summary.log")
    
    print(f"\n📂 Playlist: {playlist_title}")
    print(f"📊 Total videos found: {total_items}\n")
    
    success_count = 0
    failed_items = []
    
    # 2. Iterate and download each item individually to catch specific errors
    for index, entry in enumerate(entries, 1):
        if entry is None:
            failed_items.append({
                "index": index,
                "title": "Unknown/Deleted Video",
                "reason": "Video is private, deleted, or geoblocked."
            })
            continue
            
        vid_title = entry.get('title', f'Unknown Title {index}')
        vid_url = entry.get('url')
        
        if not vid_url:
            failed_items.append({
                "index": index,
                "title": vid_title,
                "reason": "No valid URL found in playlist metadata."
            })
            continue
            
        # yt-dlp sometimes extracts just the ID in flat mode
        if not vid_url.startswith('http'):
            vid_url = f"https://www.youtube.com/watch?v={vid_url}"
            
        print(f"[{index}/{total_items}] Fetching: {vid_title}")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            # Manually inject the index for correct track ordering
            'outtmpl': f"{safe_folder_name}/{index:02d} - %(title)s.%(ext)s",
            'ignoreerrors': False, # Force exceptions so we can catch and log them
            'quiet': True,         # Suppress yt-dlp console spam to keep our UI clean
            'no_warnings': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([vid_url])
            success_count += 1
            print("✅ Success.\n")
        except Exception as e:
            # Grab the main error text without the huge python traceback stack
            error_msg = str(e).replace('\n', ' | ') 
            print("❌ Failed.\n")
            failed_items.append({
                "index": index,
                "title": vid_title,
                "reason": error_msg
            })

    # 3. Generate the Log File inside the playlist folder
    with open(log_filename, 'w', encoding='utf-8') as log_file:
        log_file.write(f"Playlist Name: {playlist_title}\n")
        log_file.write(f"Total Videos: {total_items}\n")
        log_file.write(f"Successfully Downloaded: {success_count}\n")
        log_file.write(f"Failed Downloads: {len(failed_items)}\n")
        log_file.write("="*50 + "\n\n")
        
        if failed_items:
            log_file.write("⚠️ FAILED ITEMS REPORT:\n")
            log_file.write("-" * 50 + "\n")
            for fail in failed_items:
                log_file.write(f"Track #{fail['index']}: {fail['title']}\n")
                log_file.write(f"Reason: {fail['reason']}\n")
                log_file.write("-" * 50 + "\n")
        else:
            log_file.write("🎉 All items downloaded successfully! No failures.\n")

    # 4. Final Console Output Summary
    print("===========================================")
    print("🎉 DOWNLOAD PROCESS COMPLETE!")
    print(f"✅ Succeeded: {success_count} / {total_items}")
    print(f"❌ Failed: {len(failed_items)}")
    print(f"📄 Detailed log saved at: {log_filename}")
    print("===========================================")

if __name__ == "__main__":
    url = input("\nEnter the YouTube playlist URL: ").strip()
    if url:
        download_playlist_as_mp3(url)
    else:
        print("No URL provided. Exiting.")