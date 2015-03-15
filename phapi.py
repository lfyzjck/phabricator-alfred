#!/usr/bin/python
# encoding=utf-8
from urlparse import urlparse
from operator import itemgetter

from phabricator import Phabricator

ph = Phabricator()


class PhabricatorAPI(object):
    def __init__(self):
        self.user = self.whoami()

    @property
    def phid(self):
        return self.user['phid']

    @property
    def username(self):
        return self.user['userName']

    def whoami(self):
        return ph.user.whoami()

    def query_users(self, phids):
        return ph.user.query(phids=phids)

    def query_phid(self, user):
        return ph.user.query(usernames=[user])[0]['phid']

    def query_tasks(self):
        return ph.maniphest.query(
            ownerPHIDs=[self.phid],
            status='status-open',
            order='order-priority'
        ).response.values()

    def close_task(self, taskid, comment=u''):
        return ph.maniphest.update(
            taskid, status='status-closed', comment=comment)

    def query_diff(self):
        return ph.differential.query(
            status='status-open',
            reviewers=[self.phid],
            order='order-created'
        )


def query_usernames(api, phids):
    users = api.query_users(phids)
    return map(itemgetter('userName'), users)


def new_task(wf):
    parser = urlparse(ph.host)
    uri = "%s://%s/maniphest/task/create/" % (parser.scheme, parser.netloc)
    wf.add_item("New Phniphest Task", 
        arg=uri,
        valid=True)
    wf.send_feedback()


def query_tasks(wf):
    api = PhabricatorAPI()
    tasks = api.query_tasks()
    for task in sorted(tasks, reverse=True):
        wf.add_item(
            u"[%s] %s" % (task['objectName'], task['title']),
            arg=task['uri'],
            valid=True)

    wf.send_feedback()


def query_diffs(wf):
    api = PhabricatorAPI()
    diffs = api.query_diff()
    for d in diffs:
        p = urlparse(d['uri'])
        users = query_usernames(api, d['reviewers'])
        wf.add_item(u'[%s] %s' % (p.path.lstrip('/'), d['title']),
            '%s, reviwers: %s' % (d['statusName'], ', '.join(users)),
            arg=d['uri'],
            valid=True)

    wf.send_feedback()
