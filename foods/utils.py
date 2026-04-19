from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
import mimetypes
import os


def send_email_view(user_email, bill_data):

    subject = "🧾 Order Receipt - Payment Successful"

    # Add CID for each image
    for i, item in enumerate(bill_data['items']):
        if item.get('image'):
            item['cid'] = f"food{i}"

    html_message = render_to_string("billtemplate.html", bill_data)
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [user_email]
    )

    email.attach_alternative(html_message, "text/html")

    # Attach images inline
    for i, item in enumerate(bill_data['items']):
        if item.get('image'):

            image_path = os.path.join(
            settings.MEDIA_ROOT,
            item['image'].replace(settings.MEDIA_URL, '')
        )

            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    img_data = f.read()

                mime_type, _ = mimetypes.guess_type(image_path)

                if mime_type:
                    subtype = mime_type.split('/')[-1]
                else:
                    subtype = "jpeg"
                img = MIMEImage(img_data, _subtype=subtype)
                img.add_header('Content-ID', f"<food{i}>")
                img.add_header('Content-Disposition', 'inline')
                email.attach(img)

    email.send()


