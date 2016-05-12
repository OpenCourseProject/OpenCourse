from django.core.management.base import BaseCommand, CommandError
from opencourse.models import UpdateLog
from django.utils import timezone
import subprocess, signal
import os
import kronos
from django.conf import settings
from datetime import datetime

MAX_TIME = 60 * 20 # 20 Minutes

@kronos.register(settings.COURSE_UPDATE_WATCHER_INTERVAL)
class Command(BaseCommand):
    help = 'Terminates and logs errors on scrapes that have timed out'

    def kill(self):
        p = subprocess.Popen(['ps', 'a'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if 'graph-courses' in line or 'firefox' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)
                self.stdout.write('Killed pid {}'.format(pid))

    def handle(self, *args, **options):
        updates = UpdateLog.objects.filter(status=UpdateLog.IN_PROGRESS)
        if len(updates) > 0:
            for update in updates:
                diff = timezone.now() - update.time_created
                if diff.seconds >= MAX_TIME:
                    status = UpdateLog.FAILED
                    update.status = status
                    update.time_completed = timezone.now()
                    update.save()

                    minutes, seconds = divmod(diff.seconds, 60)
                    update.log('Update timeout detected. Process terminated after {}m, {}s (status = {})'.format(minutes, seconds, status))
                    self.kill()
                    self.stdout.write('Failed update {}'.format(update))
