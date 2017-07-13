from __future__ import absolute_import

from rest_framework.response import Response

from sentry.api.bases import ProjectEndpoint

from sentry.models import (
    GroupHash, GroupTombstone,
)


class GroupTombstoneDetailsEndpoint(ProjectEndpoint):

    def delete(self, request, project, tombstone_id):
        """
        Remove a GroupTombstone
        ```````````````

        Undiscards a group such that new events in that group will be captured.
        This does not restore any previous data.

        :pparam string organization_slug: the slug of the organization.
        :pparam string project_slug: the slug of the project to which this tombstone belongs.
        :pparam string issue_id: the ID of the tombstone to remove.
        :auth: required
        """
        GroupHash.objects.filter(
            group_tombstone=tombstone_id,
        ).update(
            # will allow new events to be captured
            group_tombstone=None,
        )

        try:
            GroupTombstone.objects.get(id=tombstone_id).delete()
        except GroupTombstone.DoesNotExist:
            pass

        return Response(status=204)