# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2014 Mirantis, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from manila import exception
from manila import test
from manila import utils


class FakeNotifier(object):
    """Acts like the manila.openstack.common.notifier.api module."""
    ERROR = 88

    def __init__(self):
        self.provided_publisher = None
        self.provided_event = None
        self.provided_priority = None
        self.provided_payload = None

    def notify(self, context, publisher, event, priority, payload):
        self.provided_publisher = publisher
        self.provided_event = event
        self.provided_priority = priority
        self.provided_payload = payload


class ManilaExceptionTestCase(test.TestCase):
    def test_default_error_msg(self):
        class FakeManilaException(exception.ManilaException):
            message = "default message"

        exc = FakeManilaException()
        self.assertEqual(unicode(exc), 'default message')

    def test_error_msg(self):
        self.assertEqual(unicode(exception.ManilaException('test')),
                          'test')

    def test_default_error_msg_with_kwargs(self):
        class FakeManilaException(exception.ManilaException):
            message = "default message: %(code)s"

        exc = FakeManilaException(code=500)
        self.assertEqual(unicode(exc), 'default message: 500')

    def test_error_msg_exception_with_kwargs(self):
        # NOTE(dprince): disable format errors for this test
        self.flags(fatal_exception_format_errors=False)

        class FakeManilaException(exception.ManilaException):
            message = "default message: %(mispelled_code)s"

        exc = FakeManilaException(code=500)
        self.assertEqual(unicode(exc), 'default message: %(mispelled_code)s')

    def test_default_error_code(self):
        class FakeManilaException(exception.ManilaException):
            code = 404

        exc = FakeManilaException()
        self.assertEqual(exc.kwargs['code'], 404)

    def test_error_code_from_kwarg(self):
        class FakeManilaException(exception.ManilaException):
            code = 500

        exc = FakeManilaException(code=404)
        self.assertEqual(exc.kwargs['code'], 404)


class ManilaExceptionResponseCode400(test.TestCase):

    def test_invalid(self):
        # Verify response code for exception.Invalid
        e = exception.Invalid()
        self.assertEqual(e.code, 400)

    def test_invalid_input(self):
        # Verify response code for exception.InvalidInput
        reason = "fake_reason"
        e = exception.InvalidInput(reason=reason)
        self.assertEqual(e.code, 400)
        self.assertIn(reason, e.msg)

    def test_invalid_request(self):
        # Verify response code for exception.InvalidRequest
        e = exception.InvalidRequest()
        self.assertEqual(e.code, 400)

    def test_invalid_results(self):
        # Verify response code for exception.InvalidResults
        e = exception.InvalidResults()
        self.assertEqual(e.code, 400)

    def test_invalid_uuid(self):
        # Verify response code for exception.InvalidUUID
        uuid = "fake_uuid"
        e = exception.InvalidUUID(uuid=uuid)
        self.assertEqual(e.code, 400)
        self.assertIn(uuid, e.msg)

    def test_invalid_content_type(self):
        # Verify response code for exception.InvalidContentType
        content_type = "fake_content_type"
        e = exception.InvalidContentType(content_type=content_type)
        self.assertEqual(e.code, 400)
        self.assertIn(content_type, e.msg)

    def test_invalid_parameter_value(self):
        # Verify response code for exception.InvalidParameterValue
        err = "fake_err"
        e = exception.InvalidParameterValue(err=err)
        self.assertEqual(e.code, 400)
        self.assertIn(err, e.msg)

    def test_invalid_reservation_expiration(self):
        # Verify response code for exception.InvalidReservationExpiration
        expire = "fake_expire"
        e = exception.InvalidReservationExpiration(expire=expire)
        self.assertEqual(e.code, 400)
        self.assertIn(expire, e.msg)

    def test_invalid_quota_value(self):
        # Verify response code for exception.InvalidQuotaValue
        e = exception.InvalidQuotaValue()
        self.assertEqual(e.code, 400)

    def test_invalid_share(self):
        # Verify response code for exception.InvalidShare
        reason = "fake_reason"
        e = exception.InvalidShare(reason=reason)
        self.assertEqual(e.code, 400)
        self.assertIn(reason, e.msg)

    def test_invalid_share_access(self):
        # Verify response code for exception.InvalidShareAccess
        reason = "fake_reason"
        e = exception.InvalidShareAccess(reason=reason)
        self.assertEqual(e.code, 400)
        self.assertIn(reason, e.msg)

    def test_invalid_share_snapshot(self):
        # Verify response code for exception.InvalidShareSnapshot
        reason = "fake_reason"
        e = exception.InvalidShareSnapshot(reason=reason)
        self.assertEqual(e.code, 400)
        self.assertIn(reason, e.msg)

    def test_invalid_share_metadata(self):
        # Verify response code for exception.InvalidShareMetadata
        e = exception.InvalidShareMetadata()
        self.assertEqual(e.code, 400)

    def test_invalid_share_metadata_size(self):
        # Verify response code for exception.InvalidShareMetadataSize
        e = exception.InvalidShareMetadataSize()
        self.assertEqual(e.code, 400)

    def test_invalid_volume(self):
        # Verify response code for exception.InvalidVolume
        e = exception.InvalidVolume()
        self.assertEqual(e.code, 400)

    def test_invalid_volume_type(self):
        # Verify response code for exception.InvalidVolumeType
        reason = "fake_reason"
        e = exception.InvalidVolumeType(reason=reason)
        self.assertEqual(e.code, 400)
        self.assertIn(reason, e.msg)


class ManilaExceptionResponseCode403(test.TestCase):

    def test_not_authorized(self):
        # Verify response code for exception.NotAuthorized
        e = exception.NotAuthorized()
        self.assertEqual(e.code, 403)

    def test_admin_required(self):
        # Verify response code for exception.AdminRequired
        e = exception.AdminRequired()
        self.assertEqual(e.code, 403)

    def test_policy_not_authorized(self):
        # Verify response code for exception.PolicyNotAuthorized
        action = "fake_action"
        e = exception.PolicyNotAuthorized(action=action)
        self.assertEqual(e.code, 403)
        self.assertIn(action, e.msg)


class ManilaExceptionResponseCode404(test.TestCase):

    def test_not_found(self):
        # Verify response code for exception.NotFound
        e = exception.NotFound()
        self.assertEqual(e.code, 404)

    def test_share_network_not_found(self):
        # Verify response code for exception.ShareNetworkNotFound
        share_network_id = "fake_share_network_id"
        e = exception.ShareNetworkNotFound(share_network_id=share_network_id)
        self.assertEqual(e.code, 404)
        self.assertIn(share_network_id, e.msg)

    def test_share_server_not_found(self):
        # Verify response code for exception.ShareServerNotFound
        share_server_id = "fake_share_server_id"
        e = exception.ShareServerNotFound(share_server_id=share_server_id)
        self.assertEqual(e.code, 404)
        self.assertIn(share_server_id, e.msg)

    def test_service_not_found(self):
        # Verify response code for exception.ServiceNotFound
        service_id = "fake_service_id"
        e = exception.ServiceNotFound(service_id=service_id)
        self.assertEqual(e.code, 404)
        self.assertIn(service_id, e.msg)

    def test_host_not_found(self):
        # Verify response code for exception.HostNotFound
        host = "fake_host"
        e = exception.HostNotFound(host=host)
        self.assertEqual(e.code, 404)
        self.assertIn(host, e.msg)

    def test_scheduler_host_filter_not_found(self):
        # Verify response code for exception.SchedulerHostFilterNotFound
        filter_name = "fake_filter_name"
        e = exception.SchedulerHostFilterNotFound(filter_name=filter_name)
        self.assertEqual(e.code, 404)
        self.assertIn(filter_name, e.msg)

    def test_scheduler_host_weigher_not_found(self):
        # Verify response code for exception.SchedulerHostWeigherNotFound
        weigher_name = "fake_weigher_name"
        e = exception.SchedulerHostWeigherNotFound(weigher_name=weigher_name)
        self.assertEqual(e.code, 404)
        self.assertIn(weigher_name, e.msg)

    def test_host_binary_not_found(self):
        # Verify response code for exception.HostBinaryNotFound
        host = "fake_host"
        binary = "fake_binary"
        e = exception.HostBinaryNotFound(binary=binary, host=host)
        self.assertEqual(e.code, 404)
        self.assertIn(binary, e.msg)
        self.assertIn(host, e.msg)

    def test_quota_not_found(self):
        # Verify response code for exception.QuotaNotFound
        e = exception.QuotaNotFound()
        self.assertEqual(e.code, 404)

    def test_quota_resource_unknown(self):
        # Verify response code for exception.QuotaResourceUnknown
        e = exception.QuotaResourceUnknown()
        self.assertEqual(e.code, 404)

    def test_project_quota_not_found(self):
        # Verify response code for exception.ProjectQuotaNotFound
        e = exception.ProjectQuotaNotFound()
        self.assertEqual(e.code, 404)

    def test_quota_class_not_found(self):
        # Verify response code for exception.QuotaClassNotFound
        e = exception.QuotaClassNotFound()
        self.assertEqual(e.code, 404)

    def test_quota_usage_not_found(self):
        # Verify response code for exception.QuotaUsageNotFound
        e = exception.QuotaUsageNotFound()
        self.assertEqual(e.code, 404)

    def test_reservation_not_found(self):
        # Verify response code for exception.ReservationNotFound
        e = exception.ReservationNotFound()
        self.assertEqual(e.code, 404)

    def test_migration_not_found(self):
        # Verify response code for exception.MigrationNotFound
        migration_id = "fake_migration_id"
        e = exception.MigrationNotFound(migration_id=migration_id)
        self.assertEqual(e.code, 404)
        self.assertIn(migration_id, e.msg)

    def test_migration_not_found_by_status(self):
        # Verify response code for exception.MigrationNotFoundByStatus
        status = "fake_status"
        instance_id = "fake_instance_id"
        e = exception.MigrationNotFoundByStatus(status=status,
                                                instance_id=instance_id)
        self.assertEqual(e.code, 404)
        self.assertIn(status, e.msg)
        self.assertIn(instance_id, e.msg)

    def test_file_not_found(self):
        # Verify response code for exception.FileNotFound
        file_path = "fake_file_path"
        e = exception.FileNotFound(file_path=file_path)
        self.assertEqual(e.code, 404)
        self.assertIn(file_path, e.msg)

    def test_config_not_found(self):
        # Verify response code for exception.ConfigNotFound
        path = "fake_path"
        e = exception.ConfigNotFound(path=path)
        self.assertEqual(e.code, 404)
        self.assertIn(path, e.msg)

    def test_paste_app_not_found(self):
        # Verify response code for exception.PasteAppNotFound
        name = "fake_name"
        path = "fake_path"
        e = exception.PasteAppNotFound(name=name, path=path)
        self.assertEqual(e.code, 404)
        self.assertIn(name, e.msg)
        self.assertIn(path, e.msg)

    def test_share_snapshot_not_found(self):
        # Verify response code for exception.ShareSnapshotNotFound
        snapshot_id = "fake_snapshot_id"
        e = exception.ShareSnapshotNotFound(snapshot_id=snapshot_id)
        self.assertEqual(e.code, 404)
        self.assertIn(snapshot_id, e.msg)

    def test_share_metadata_not_found(self):
        # verify response code for exception.ShareMetadataNotFound
        e = exception.ShareMetadataNotFound()
        self.assertEqual(e.code, 404)

    def test_security_service_not_found(self):
        # verify response code for exception.SecurityServiceNotFound
        security_service_id = "fake_security_service_id"
        e = exception.SecurityServiceNotFound(
            security_service_id=security_service_id)
        self.assertEqual(e.code, 404)
        self.assertIn(security_service_id, e.msg)

    def test_volume_not_found(self):
        # verify response code for exception.VolumeNotFound
        volume_id = "fake_volume_id"
        e = exception.VolumeNotFound(volume_id=volume_id)
        self.assertEqual(e.code, 404)
        self.assertIn(volume_id, e.msg)

    def test_volume_snapshot_not_found(self):
        # verify response code for exception.VolumeSnapshotNotFound
        snapshot_id = "fake_snapshot_id"
        e = exception.VolumeSnapshotNotFound(snapshot_id=snapshot_id)
        self.assertEqual(e.code, 404)
        self.assertIn(snapshot_id, e.msg)

    def test_volume_type_not_found(self):
        # verify response code for exception.VolumeTypeNotFound
        volume_type_id = "fake_volume_type_id"
        e = exception.VolumeTypeNotFound(volume_type_id=volume_type_id)
        self.assertEqual(e.code, 404)
        self.assertIn(volume_type_id, e.msg)

    def test_volume_type_not_found_by_name(self):
        # verify response code for exception.VolumeTypeNotFoundByName
        volume_type_name = "fake_volume_type_name"
        e = exception.VolumeTypeNotFoundByName(
            volume_type_name=volume_type_name)
        self.assertEqual(e.code, 404)
        self.assertIn(volume_type_name, e.msg)

    def test_volume_type_extra_specs_not_found(self):
        # verify response code for exception.VolumeTypeExtraSpecsNotFound
        volume_type_id = "fake_volume_type_id"
        extra_specs_key = "fake_extra_specs_key"
        e = exception.VolumeTypeExtraSpecsNotFound(
            volume_type_id=volume_type_id, extra_specs_key=extra_specs_key)
        self.assertEqual(e.code, 404)
        self.assertIn(volume_type_id, e.msg)
        self.assertIn(extra_specs_key, e.msg)

    def test_instance_not_found(self):
        # verify response code for exception.InstanceNotFound
        instance_id = "fake_instance_id"
        e = exception.InstanceNotFound(instance_id=instance_id)
        self.assertEqual(e.code, 404)
        self.assertIn(instance_id, e.msg)


class ManilaExceptionResponseCode413(test.TestCase):

    def test_quota_error(self):
        # verify response code for exception.QuotaError
        e = exception.QuotaError()
        self.assertEqual(e.code, 413)

    def test_share_size_exceeds_available_quota(self):
        # verify response code for exception.ShareSizeExceedsAvailableQuota
        e = exception.ShareSizeExceedsAvailableQuota()
        self.assertEqual(e.code, 413)

    def test_share_limit_exceeded(self):
        # verify response code for exception.ShareLimitExceeded
        allowed = 776  # amount of allowed shares
        e = exception.ShareLimitExceeded(allowed=allowed)
        self.assertEqual(e.code, 413)
        self.assertIn(str(allowed), e.msg)

    def test_snapshot_limit_exceeded(self):
        # verify response code for exception.SnapshotLimitExceeded
        allowed = 777  # amount of allowed snapshots
        e = exception.SnapshotLimitExceeded(allowed=allowed)
        self.assertEqual(e.code, 413)
        self.assertIn(str(allowed), e.msg)

    def test_share_networks_limit_exceeded(self):
        # verify response code for exception.ShareNetworksLimitExceeded
        allowed = 778  # amount of allowed share networks
        e = exception.ShareNetworksLimitExceeded(allowed=allowed)
        self.assertEqual(e.code, 413)
        self.assertIn(str(allowed), e.msg)

    def test_port_limit_exceeded(self):
        # verify response code for exception.PortLimitExceeded
        e = exception.PortLimitExceeded()
        self.assertEqual(e.code, 413)
