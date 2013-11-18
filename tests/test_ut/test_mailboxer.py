import json

from ..test_utils import send_mail, TestCase

class SingleMailboxTest(TestCase):

    def setUp(self):
        super(SingleMailboxTest, self).setUp()
        self.mailbox_email = "mailbox_email@blap.com"
        self._post("/v2/mailboxes", data={"email": self.mailbox_email})

    def _get_single_page(self, url):
        returned = json.loads(self._get(url).data)
        self.assertEquals(returned["metadata"]["total_num_pages"], 1)
        self.assertEquals(returned["metadata"]["page"], 1)
        return returned["result"]

class MailboxTest(SingleMailboxTest):

    def test_get_mailboxes(self):
        [mailbox] = self._get_single_page("/v2/mailboxes")
        self.assertEquals(mailbox["email"], self.mailbox_email)

    def test_get_emails_empty(self):
        self.assertEquals([], self._get_single_page("/v2/mailboxes/{}/emails".format(self.mailbox_email)))


class EmailSendingTest(SingleMailboxTest):

    def setUp(self):
        super(EmailSendingTest, self).setUp()
        self.message = "message here"
        self.fromaddr = "someaddr@blap.com"
        send_mail(self.fromaddr, [self.mailbox_email], self.message)

    def test_send_receive_email(self):
        [email] = self._get_single_page("/v2/mailboxes/{}/emails".format(self.mailbox_email))
        self.assertEquals(email, {
            "id": 1,
            "message": self.message,
            "fromaddr": self.fromaddr,
            "sent_via_ssl": False,
        })
