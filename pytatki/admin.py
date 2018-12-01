"""This module contains endpoints for administrating a pytatki server."""

from pytatki import __version__ as version
from pytatki.user import send_confirmation_email
from pytatki.dbconnect import connection
from pytatki.main import APP
from pytatki.view_manager import admin_required

__author__ = u"Patryk Niedźwiedziński"
__copyright__ = "Copyright 2018, Pytatki"
__credits__ = []
__license__ = "MIT"
__version__ = version
__maintainer__ = u"Patryk Niedźwiedziński"
__email__ = "pniedzwiedzinski19@gmail.com"
__status__ = "Production"


@APP.route('/admin/verify_all/')
@admin_required
def send_to_all():
    """
    This endpoint provide possibility to resend verification emails to all
    users, who have unverified email adress.
    :returns: "success" after sending all emails
    """
    con, conn = connection()
    con.execute("SELECT email FROM user WHERE email_confirm = 0")
    emails = [email['email'] for email in con.fetchall()]
    con.close()
    conn.close()

    for email in emails:
        send_confirmation_email(email)

    return "success"
