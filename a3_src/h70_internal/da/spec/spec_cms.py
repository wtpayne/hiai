# -*- coding: utf-8 -*-
"""
Unit tests for the da.cms module.

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


# =============================================================================
class SpecifyRegister:
    """
    Specify the da.cms.register() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The register() function is callable.

        """
        import da.cms
        assert callable(da.cms.register)


# =============================================================================
class Specify_GenAllPreviousBuilds:
    """
    Specify the da.cms._gen_all_previous_builds() function.

    """

    # -------------------------------------------------------------------------
    def it_generates_all_previous_builds(self, tmpdir):
        """
        It generates all previous builds.

        """
        import da.cms
        assert True
        dir_cms  = tmpdir.ensure('cms',            dir = True)
        dir_tbox = dir_cms.ensure('2015', '1608B', dir = True)
        dir_tbox.ensure('aa', 'cc', '1608B.20.2249.aa.cc.abc01234', dir = True)
        dir_tbox.ensure('aa', 'dd', '1608B.20.2249.aa.dd.abc01234', dir = True)
        dir_tbox.ensure('bb', 'cc', '1608B.20.2249.bb.cc.abc01234', dir = True)
        dir_tbox.ensure('bb', 'dd', '1608B.20.2249.bb.dd.abc01234', dir = True)
        dirpath_cms = str(dir_cms)

        out = sorted(list(da.cms._gen_all_previous_builds(dirpath_cms)))

        assert out[0].endswith(
                        '/cms/2015/1608B/aa/cc/1608B.20.2249.aa.cc.abc01234')

        assert out[1].endswith(
                        '/cms/2015/1608B/aa/dd/1608B.20.2249.aa.dd.abc01234')

        assert out[2].endswith(
                        '/cms/2015/1608B/bb/cc/1608B.20.2249.bb.cc.abc01234')

        assert out[3].endswith(
                        '/cms/2015/1608B/bb/dd/1608B.20.2249.bb.dd.abc01234')


# =============================================================================
class Specify_GenCmsPathYear:
    """
    Specify the da.cms._gen_cms_path_year() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _gen_cms_path_year() function is callable.

        """
        import da.cms
        assert callable(da.cms._gen_cms_path_year)


# =============================================================================
class Specify_GenCmsPathTimebox:
    """
    Specify the da.cms._gen_cms_path_timebox() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _gen_cms_path_timebox() function is callable.

        """
        import da.cms
        assert callable(da.cms._gen_cms_path_timebox)


# =============================================================================
class Specify_GenCmsPathBldcfg:
    """
    Specify the da.cms._gen_cms_path_bldcfg() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _gen_cms_path_bldcfg() function is callable.

        """
        import da.cms
        assert callable(da.cms._gen_cms_path_bldcfg)


# =============================================================================
class Specify_GenCmsPathBranch:
    """
    Specify the da.cms._gen_cms_path_branch() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _gen_cms_path_branch() function is callable.

        """
        import da.cms
        assert callable(da.cms._gen_cms_path_branch)


# =============================================================================
class Specify_GenCmsPathBuild:
    """
    Specify the da.cms._gen_cms_path_build() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _gen_cms_path_build() function is callable.

        """
        import da.cms
        assert callable(da.cms._gen_cms_path_build)
