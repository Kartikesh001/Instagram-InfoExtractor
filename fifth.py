import instaloader
import pandas as pd

# Input Instagram username
username = input("Enter Instagram Username: ")
instagram = instaloader.Instaloader()

# Login for enhanced access
login = input("Do you want to log in for enhanced access? (yes/no): ").lower()
if login == "yes":
    insta_username = input("Enter your Instagram username for login: ")
    insta_password = input("Enter your Instagram password: ")
    instagram.login(insta_username, insta_password)
    print("Logged in successfully!")

# Load profile
profile = instaloader.Profile.from_username(instagram.context, username)

# Profile information
profile_data = {
    "Username": username,
    "Followers": profile.followers,
    "Following": profile.followees,
    "Total Posts": profile.mediacount,
    "Bio": profile.biography,
    "External URL": profile.external_url,
    "Full Name": profile.full_name,
    "Is Private": profile.is_private,
    "Is Verified": profile.is_verified,
    "Is Business Account": profile.is_business_account,
}

# Print profile data for verification
print("\nUser Information:")
for key, value in profile_data.items():
    print(f"{key}: {value}")

# Collect post analytics
posts_data = []
print("\nFetching Post Analytics...")

for post in profile.get_posts():
    # Add post analytics
    post_data = {
        "Post ID": post.shortcode,
        "Caption": (post.caption[:50] + "...") if post.caption else "No caption",  # Truncated caption
        "Likes": post.likes,
        "Comments": post.comments,
        "Views": post.video_view_count if post.is_video else "Not a video",
        "Post Time": post.date_utc.strftime('%Y-%m-%d %H:%M:%S'),
        "Location": post.location.name if post.location else "No location",
        "Is Video": post.is_video,
    }
    posts_data.append(post_data)

    # Limit to first 50 posts (adjustable)
    if len(posts_data) >= 50:
        break

# Save data to a CSV file
profile_df = pd.DataFrame([profile_data])
posts_df = pd.DataFrame(posts_data)

# Save as CSV
profile_df.to_csv(f"{username}_profile.csv", index=False)
posts_df.to_csv(f"{username}_posts.csv", index=False)

print("\nData saved successfully!")
print(f"Profile data saved as {username}_profile.csv")
print(f"Post analytics saved as {username}_posts.csv")
