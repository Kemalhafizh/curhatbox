import os
import django
import random
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'curhatbox.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import Message

def main():
    try:
        user = User.objects.get(username='qctester123')
    except User.DoesNotExist:
        print("User qctester123 not found.")
        return

    # Delete old messages to start fresh
    Message.objects.filter(recipient=user).delete()
    print("Cleared old messages.")

    browser_choices = ['Chrome', 'Safari', 'Firefox', 'Edge', 'Opera']
    device_choices = ['Windows', 'Mac OS X', 'Android', 'iOS', 'Linux']
    reaction_choices = ["🔥", "❤️", "💀", "🤡", "😄", "😂", "😭", "🥺", "😡", "🤯", "👍", "✨"]
    
    now = timezone.now()

    messages_data = []
    
    print("Generating 50 dummy messages...")
    for i in range(50):
        # Randomize creation time mostly within the last 7 days
        days_ago = random.randint(0, 7)
        hour_sent = random.choices(
            range(24),
            weights=[1, 1, 1, 0, 0, 0, 1, 3, 5, 8, 10, 8, 5, 4, 3, 4, 6, 9, 12, 11, 8, 5, 3, 2], # Peak hours around 10am and 6-7pm
            k=1
        )[0]
        minute_sent = random.randint(0, 59)
        
        created_time = now - timedelta(days=days_ago)
        created_time = created_time.replace(hour=hour_sent, minute=minute_sent)
        
        is_read = random.choice([True, True, True, False]) # Mostly read
        
        msg = Message(
            recipient=user,
            content=f"Dummy message #{i+1} for analytics testing.",
            sender_ip=f"192.168.1.{random.randint(1, 255)}",
            sender_device=random.choices(device_choices, weights=[40, 20, 30, 8, 2], k=1)[0],
            sender_browser=random.choices(browser_choices, weights=[50, 20, 15, 10, 5], k=1)[0],
            is_public=random.choice([True, False]),
            is_read=is_read,
            is_favorite=random.choice([True, False, False, False]),
            is_disposable=False
        )
        
        # Add reaction to some read messages
        if is_read and random.random() > 0.4:
            msg.reaction = random.choice(reaction_choices)
            
        # Add reply to some read messages
        if is_read and random.random() > 0.5:
            msg.reply_content = f"Reply to message #{i+1}"
            msg.replied_at = created_time + timedelta(hours=random.randint(1, 5))
            
        # Manually set the created_at later since auto_now_add overrides it during save
        msg.save()
        msg.created_at = created_time
        msg.save(update_fields=['created_at'])

    print(f"Successfully created 50 messages for {user.username}.")

if __name__ == '__main__':
    main()
