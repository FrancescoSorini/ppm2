import re
from users.models import CustomUser
from notifications.models import Notification

def notify_mentions(content, sender, post_id=None, context='context'):
    """
    Cerca @menzioni nel contenuto e crea notifiche per ogni utente menzionato.
    """
    mentioned_usernames = set(re.findall(r'@(\w+)', content))
    users = CustomUser.objects.filter(username__in=mentioned_usernames).exclude(id=sender.id)

    for user in users:
        Notification.objects.create(
            sender=sender,
            recipient=user,
            notification_type=context,  # puoi usare un tipo separato se vuoi
            post_id=post_id,
            message=f"@{sender.username} ti ha menzionato in un {context}."
        )
