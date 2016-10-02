# -*- coding: utf-8 -*-
"""
Unit tests for the da.check.bulk_data module.

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2016 High Integrity Artificial Intelligence Systems"

license:
    "Licensed under the Apache License, Version 2.0 (the License);
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."
...
"""


import textwrap

import pytest


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def dirpath_lwc_root():
    """
    Return the directory path to the root of the local working copy.

    """
    import da.lwc.discover
    return da.lwc.discover.path('root')


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def mock_bulk_data_factory(tmpdir_factory):
    """
    Fixture returning a factory function used to create mock bulk data stores.

    """
    def _factory(                                       # pylint: disable=R0913
            counterparty     = 'c000_orion',
            project_year     = '2015',
            project          = 'p0000_da',
            timebox          = '1505A',
            date             = '0504',
            plat_cfg         = 'm00_000',
            rec_serial       = 'g000_1245',
            stream_id        = 'n00_front',
            stream_path      = 'n00_front.asf',
            stream_utc_start = '124500',
            stream_utc_end   = '124500',
            stream_bytes     = '4',
            stream_sha256    = '78d3622739dd9561c366cc0bd6189d7032de3e2a98484bc1bd5eedb9d4ece51d'):  # pylint: disable=C0301
        """
        Factory function used to create mock bulk data stores.

        """
        catalog = textwrap.dedent("""
        title:
          "Mock data catalog."

        identification:
          counterparty:     "{counterparty}"
          project_year:     "{project_year}"
          project:          "{project}"
          timebox:          "{timebox}"

        catalog:
          - date:           "{date}"
            plat_cfg:       "{plat_cfg}"
            rec_serial:     "{rec_serial}"
            streams:
              {stream_id}:
                path:       "{stream_path}"
                utc_start:  "{stream_utc_start}"
                utc_end:    "{stream_utc_end}"
                bytes:      "{stream_bytes}"
                sha256:     "{stream_sha256}"
            notes:
              "This empty clip is used as a unit test mock."
            tags:
              - unit_test
        """.format(counterparty     = counterparty,
                   project_year     = project_year,
                   project          = project,
                   timebox          = timebox,
                   date             = date,
                   plat_cfg         = plat_cfg,
                   rec_serial       = rec_serial,
                   stream_id        = stream_id,
                   stream_path      = stream_path,
                   stream_utc_start = stream_utc_start,
                   stream_utc_end   = stream_utc_end,
                   stream_bytes     = stream_bytes,
                   stream_sha256    = stream_sha256))

        filename_asf     = '{stream_id}.asf'.format(
                                                stream_id = stream_id)

        filename_label   = '{stream_id}.label.jseq'.format(
                                                stream_id = stream_id)

        filename_catalog = '{timebox}.data_catalog.yaml'.format(
                                                timebox = timebox)

        path = tmpdir_factory.mktemp('mock_bulk_data')

        path.ensure(counterparty,
                    project_year,
                    project,
                    timebox,
                    date,
                    plat_cfg,
                    rec_serial,
                    filename_asf).write(b'\x30\x26\xB2\x75', mode = 'wb')

        path.ensure(counterparty,
                    project_year,
                    project,
                    timebox,
                    date,
                    plat_cfg,
                    rec_serial,
                    filename_label)

        path.ensure(counterparty,
                    project_year,
                    project,
                    timebox,
                    filename_catalog).write(catalog)
        return str(path)

    return _factory

# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def valid_mass_data(mock_bulk_data_factory):
    """
    Test fixture directory structure with valid file and directory names.

    """
    return mock_bulk_data_factory()


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def invalid_counterparty(mock_bulk_data_factory):
    """
    Test fixture directory structure with an invalid counterparty dirname.

    """
    return mock_bulk_data_factory(counterparty = "INVALID_COUNTERPARTY")


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def invalid_year(mock_bulk_data_factory):
    """
    Test fixture directory structure with an invalid year dirname.

    """
    return mock_bulk_data_factory(project_year = "INVALID_YEAR")


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def invalid_project(mock_bulk_data_factory):
    """
    Test fixture directory structure with an invalid project dirname.

    """
    return mock_bulk_data_factory(project = "INVALID_PROJECT")


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def invalid_timebox(mock_bulk_data_factory):
    """
    Test fixture directory structure with an invalid timebox dirname.

    """
    return mock_bulk_data_factory(timebox = "INVALID_TIMEBOX")


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def invalid_date(mock_bulk_data_factory):
    """
    Test fixture directory structure with an invalid date dirname.

    """
    return mock_bulk_data_factory(date = "INVALID_DATE")


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def invalid_platform(mock_bulk_data_factory):
    """
    Test fixture directory structure with an invalid platform dirname.

    """
    return mock_bulk_data_factory(plat_cfg = "INVALID_PLATFORM")


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def invalid_recording(mock_bulk_data_factory):
    """
    Test fixture directory structure with an invalid recording dirname.

    """
    return mock_bulk_data_factory(rec_serial = "INVALID_RECORDING")


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def invalid_stream(mock_bulk_data_factory):
    """
    Test fixture directory structure with an invalid stream filename.

    """
    return mock_bulk_data_factory(stream_id = "INVALID_STREAM")


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'session')
def idclass_regex_tab(dirpath_lwc_root):
    """
    Return a idclass_regex_tab.

    """
    import da.lwc.discover
    idclass_regex_tab = da.idclass.regex_table(dirpath_lwc_root)
    return idclass_regex_tab


# -----------------------------------------------------------------------------
@pytest.fixture
def mock_build_monitor():
    """
    Return a mock da.monitor.BuildMonitor class.

    """

    # =========================================================================
    class Mock:
        """
        Mock da.monitor.BuildMonitor class

        """

        # ---------------------------------------------------------------------
        def __init__(self):
            """
            Constructor for mock build monitor.

            """
            self.nonconformity_reported = False
            self.nonconformities        = []

        # ---------------------------------------------------------------------
        def report_nonconformity(                       # pylint: disable=R0913
                self, tool, msg_id, msg, path,          # pylint: disable=W0613
                line = 1, col = 0):                     # pylint: disable=W0613
            """
            Mock report_nonconformity method.

            """
            self.nonconformity_reported = True
            self.nonconformities.append({
                'tool':     tool,
                'msg_id':   msg_id,
                'msg':      msg,
                'path':     path,
                'line':     line,
                'col':      col})

    return Mock()


# =============================================================================
class SpecifyCheckAll:
    """
    Specify the da.check.bulk_data.check_all() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        Thecheck_all() function is callable.

        """
        import da.check.bulk_data
        assert callable(da.check.bulk_data.check_all)


# =============================================================================
class Specify_CheckAllImpl:
    """
    Specify the da.check.bulk_data._check_all_impl() function.

    """

    # -------------------------------------------------------------------------
    def it_validates_valid_directory_structures(self,
                                                valid_mass_data,
                                                dirpath_lwc_root,
                                                idclass_regex_tab,
                                                mock_build_monitor):
        """
        The _check_all_impl() function validates valid directory structures.

        """
        import da.check.bulk_data
        da.check.bulk_data._check_all_impl(
                                    dirpath           = valid_mass_data,
                                    entry_level       = 'data_root',
                                    dirpath_lwc_root  = dirpath_lwc_root,
                                    idclass_regex_tab = idclass_regex_tab,
                                    build_monitor     = mock_build_monitor)
        assert len(mock_build_monitor.nonconformities) == 0
        assert mock_build_monitor.nonconformity_reported == False

    # -------------------------------------------------------------------------
    def it_reports_when_counterparty_invalid(self,
                                             invalid_counterparty,
                                             dirpath_lwc_root,
                                             idclass_regex_tab,
                                             mock_build_monitor):
        """
        _check_all_impl() reports a nonconformity for invalid_counterparty.

        """
        import da.check.bulk_data
        da.check.bulk_data._check_all_impl(
                                    dirpath           = invalid_counterparty,
                                    entry_level       = 'data_root',
                                    dirpath_lwc_root  = dirpath_lwc_root,
                                    idclass_regex_tab = idclass_regex_tab,
                                    build_monitor     = mock_build_monitor)
        mon = mock_build_monitor
        assert mon.nonconformity_reported == True

        assert all(
            nc['tool'] == 'da.check.bulk_data' for nc in mon.nonconformities)

        assert any(
            nc['msg_id'] == da.check.constants.DATA_NAME_ERR_IN_DATA_ROOT
                for nc in mon.nonconformities)

    # -------------------------------------------------------------------------
    def it_reports_when_year_invalid(self,
                                     invalid_year,
                                     dirpath_lwc_root,
                                     idclass_regex_tab,
                                     mock_build_monitor):
        """
        _check_all_impl() reports a nonconformity when invalid_year given.

        """
        import da.check.bulk_data
        da.check.bulk_data._check_all_impl(
                                    dirpath           = invalid_year,
                                    entry_level       = 'data_root',
                                    dirpath_lwc_root  = dirpath_lwc_root,
                                    idclass_regex_tab = idclass_regex_tab,
                                    build_monitor     = mock_build_monitor)
        mon = mock_build_monitor
        assert mon.nonconformity_reported == True

        assert all(
            nc['tool'] == 'da.check.bulk_data' for nc in mon.nonconformities)

        assert any(
            nc['msg_id'] == da.check.constants.DATA_NAME_ERR_IN_COUNTERPARTY
                for nc in mon.nonconformities)

    # -------------------------------------------------------------------------
    def it_reports_when_project_invalid(self,
                                        invalid_project,
                                        dirpath_lwc_root,
                                        idclass_regex_tab,
                                        mock_build_monitor):
        """
        _check_all_impl() reports a nonconformity when invalid_project given.

        """
        import da.check.bulk_data
        da.check.bulk_data._check_all_impl(
                                    dirpath           = invalid_project,
                                    entry_level       = 'data_root',
                                    dirpath_lwc_root  = dirpath_lwc_root,
                                    idclass_regex_tab = idclass_regex_tab,
                                    build_monitor     = mock_build_monitor)
        mon = mock_build_monitor
        assert mon.nonconformity_reported == True

        assert all(
            nc['tool'] == 'da.check.bulk_data' for nc in mon.nonconformities)

        assert any(
            nc['msg_id'] == da.check.constants.DATA_NAME_ERR_IN_YEAR
                for nc in mon.nonconformities)

    # -------------------------------------------------------------------------
    def it_reports_when_timebox_invalid(self,
                                        invalid_timebox,
                                        dirpath_lwc_root,
                                        idclass_regex_tab,
                                        mock_build_monitor):
        """
        _check_all_impl() reports a nonconformity when invalid_timebox given.

        """
        import da.check.bulk_data
        da.check.bulk_data._check_all_impl(
                                    dirpath           = invalid_timebox,
                                    entry_level       = 'data_root',
                                    dirpath_lwc_root  = dirpath_lwc_root,
                                    idclass_regex_tab = idclass_regex_tab,
                                    build_monitor     = mock_build_monitor)
        mon = mock_build_monitor
        assert mon.nonconformity_reported == True

        assert all(
            nc['tool'] == 'da.check.bulk_data' for nc in mon.nonconformities)

        assert any(
            nc['msg_id'] == da.check.constants.DATA_NAME_ERR_IN_PROJECT
                for nc in mon.nonconformities)

    # -------------------------------------------------------------------------
    def it_reports_when_date_invalid(self,
                                     invalid_date,
                                     dirpath_lwc_root,
                                     idclass_regex_tab,
                                     mock_build_monitor):
        """
        _check_all_impl() reports a nonconformity when invalid_date given.

        """
        import da.check.bulk_data
        da.check.bulk_data._check_all_impl(
                                    dirpath           = invalid_date,
                                    entry_level       = 'data_root',
                                    dirpath_lwc_root  = dirpath_lwc_root,
                                    idclass_regex_tab = idclass_regex_tab,
                                    build_monitor     = mock_build_monitor)
        mon = mock_build_monitor
        assert mon.nonconformity_reported == True

        assert all(
            nc['tool'] == 'da.check.bulk_data' for nc in mon.nonconformities)

        assert any(
            nc['msg_id'] == da.check.constants.DATA_NAME_ERR_IN_TIMEBOX
                for nc in mon.nonconformities)

    # -------------------------------------------------------------------------
    def it_reports_when_platform_invalid(self,
                                         invalid_platform,
                                         dirpath_lwc_root,
                                         idclass_regex_tab,
                                         mock_build_monitor):
        """
        _check_all_impl() reports a nonconformity when invalid_platform given.

        """
        import da.check.bulk_data
        da.check.bulk_data._check_all_impl(
                                    dirpath           = invalid_platform,
                                    entry_level       = 'data_root',
                                    dirpath_lwc_root  = dirpath_lwc_root,
                                    idclass_regex_tab = idclass_regex_tab,
                                    build_monitor     = mock_build_monitor)
        mon = mock_build_monitor
        assert mon.nonconformity_reported == True

        assert all(
            nc['tool'] == 'da.check.bulk_data' for nc in mon.nonconformities)

        assert any(
            nc['msg_id'] == da.check.constants.DATA_NAME_ERR_IN_MMDD_DATE
                for nc in mon.nonconformities)

    # -------------------------------------------------------------------------
    def it_reports_when_recording_invalid(self,
                                          invalid_recording,
                                          dirpath_lwc_root,
                                          idclass_regex_tab,
                                          mock_build_monitor):
        """
        _check_all_impl() reports a nonconformity when invalid_recording given.

        """
        import da.check.bulk_data
        da.check.bulk_data._check_all_impl(
                                    dirpath           = invalid_recording,
                                    entry_level       = 'data_root',
                                    dirpath_lwc_root  = dirpath_lwc_root,
                                    idclass_regex_tab = idclass_regex_tab,
                                    build_monitor     = mock_build_monitor)
        mon = mock_build_monitor
        assert mon.nonconformity_reported == True

        assert all(
            nc['tool'] == 'da.check.bulk_data' for nc in mon.nonconformities)

        assert any(
            nc['msg_id'] == da.check.constants.DATA_NAME_ERR_IN_PLATFORM
                for nc in mon.nonconformities)

    # -------------------------------------------------------------------------
    def it_reports_when_stream_invalid(self,
                                       invalid_stream,
                                       dirpath_lwc_root,
                                       idclass_regex_tab,
                                       mock_build_monitor):
        """
        _check_all_impl() reports a nonconformity when invalid_stream given.

        """
        import da.check.bulk_data
        da.check.bulk_data._check_all_impl(
                                    dirpath           = invalid_stream,
                                    entry_level       = 'data_root',
                                    dirpath_lwc_root  = dirpath_lwc_root,
                                    idclass_regex_tab = idclass_regex_tab,
                                    build_monitor     = mock_build_monitor)
        mon = mock_build_monitor
        assert mon.nonconformity_reported == True

        assert all(
            nc['tool'] == 'da.check.bulk_data' for nc in mon.nonconformities)

        assert any(
            nc['msg_id'] == da.check.constants.DATA_NAME_ERR_IN_RECORDING
                for nc in mon.nonconformities)
