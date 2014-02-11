#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2013 The dfVFS Project Authors.
# Please see the AUTHORS file for details on individual authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A resolver for Windows paths to file system specific formats."""

import re

from dfvfs.lib import definitions
from dfvfs.lib import errors
from dfvfs.path import factory as path_spec_factory


class WindowsPathResolver(object):
  """Resolver object for Windows paths."""

  # Type indicators that do not have a parent.
  _PARENTLESS_TYPE_INDICATORS = frozenset([
      definitions.TYPE_INDICATOR_FAKE,
      definitions.TYPE_INDICATOR_OS])

  _PATH_SEPARATOR = u'\\'
  _PATH_EXPANSION_VARIABLE = re.compile('^[%][^%]+[%]$')

  def __init__(self, file_system, mount_point, drive_letter=u'C'):
    """Initializes the Windows path helper.

       The mount point indicates a path specification where the Windows
       file system is mounted. This can either be a path specification
       into a storage media image or a directory accessible by the operating
       system.

    Args:
      file_system: the file system object.
      mount_point: the mount point path specification (instance of
                   path.PathSpec). The default is None.
      drive_letter: optional string that contains the drive letter used by
                    the file system. The default is C.

    Raises:
      PathSpecError: if the mount point path specification is incorrect.
      ValueError: when file system or mount point is not set.
    """
    if not file_system or not mount_point:
      raise ValueError(u'Missing file system or mount point value.')

    if mount_point.type_indicator in self._PARENTLESS_TYPE_INDICATORS:
      if not hasattr(mount_point, 'location'):
        raise errors.PathSpecError(
            u'Mount point path specification missing location.')

    self._drive_letter = drive_letter
    self._environment_variables = {}
    self._file_system = file_system
    self._mount_point = mount_point

  # Windows paths:
  # Device path:                    \\.\PhysicalDrive0
  # Volume device path:             \\.\C:
  # Volume file system path:        \\.\C:\
  # Extended-length path:           \\?\C:\directory\file.txt
  # Extended-length UNC path:       \\?\UNC\server\share\directory\file.txt
  # Local 'absolute' path:          \directory\file.txt
  #                                 \directory\\file.txt
  # Local 'relative' path:          ..\directory\file.txt
  # Local 'relative' path:          .\directory\file.txt
  # Volume 'absolute' path:         C:\directory\file.txt
  # Volume 'relative' path:         C:directory\file.txt
  # UNC path:                       \\server\share\directory\file.txt
  # Path with environment variable: %SystemRoot%\file.txt
  #
  # Note Windows also allows paths like:
  # C:\..\directory\file.txt

  def _PathStripPrefix(self, path):
    """Strips the prefix from a path.

    Args:
      path: the Windows path to strip the prefix from.

    Returns:
      The path without the prefix or None if the path is not supported.
    """
    if path.startswith(u'\\\\.\\') or path.startswith(u'\\\\?\\'):
      if len(path) < 7 or path[5] != u':' or path[6] != self._PATH_SEPARATOR:
        # Cannot handle a non-volume path.
        return
      path = path[7:]

    elif path.startswith(u'\\\\'):
      # Cannot handle an UNC path.
      return

    elif len(path) >= 3 and path[1] == u':':
      # Check if the path is a Volume 'absolute' path.
      if path[2] != self._PATH_SEPARATOR:
        # Cannot handle a Volume 'relative' path.
        return
      path = path[3:]

    elif path.startswith(u'\\'):
      path = path[1:]

    else:
      # Cannot handle a relative path.
      return

    return path

  def _ResolvePath(self, path, expand_variables=True):
    """Resolves a Windows path in file system specific format.

       This function will check if the individual path segments exists within
       the file system. For this it will prefer the first case sensitive match
       above a case insensitive match. If no match was found None is returned.

    Args:
      path: the Windows path to resolve.
      expand_variables: optional value to indicate path variables should be
                        expanded or not. The default is to expand (True).

    Returns:
      A tuple of the path in file system specific format and the matching path
      specification.
    """
    # Allow for paths that start with an environment variable e.g.
    # %SystemRoot%\file.txt
    if path.startswith(u'%'):
      path_segment, _, _ = path.partition(self._PATH_SEPARATOR)
      if not self._PATH_EXPANSION_VARIABLE.match(path_segment):
        path = None
    else:
      path = self._PathStripPrefix(path)

    if path is None:
      return None, None

    if self._mount_point.type_indicator in self._PARENTLESS_TYPE_INDICATORS:
      file_entry = self._file_system.GetFileEntryByPathSpec(self._mount_point)
      expanded_path_segments = self._file_system.SplitPath(
          self._mount_point.location)
    else:
      file_entry = self._file_system.GetRootFileEntry()
      expanded_path_segments = []

    number_of_expanded_path_segments = 0

    for path_segment in path.split(self._PATH_SEPARATOR):
      if file_entry is None:
        return None, None

      # Ignore empty path segments or path segments containing a single dot.
      if not path_segment or path_segment == '.':
        continue

      if path_segment == '..':
        # Only allow to traverse back up to the mount point.
        if number_of_expanded_path_segments > 0:
          _ = expanded_path_segments.pop()
          number_of_expanded_path_segments -= 1
          file_entry = file_entry.GetParentFileEntry()
        continue

      if (expand_variables and
          self._PATH_EXPANSION_VARIABLE.match(path_segment)):
        path_segment = self._environment_variables.get(
            path_segment[1:-1].upper(), path_segment)

      sub_file_entry = file_entry.GetSubFileEntryByName(
          path_segment, case_sensitive=False)
      if sub_file_entry is None:
        return None, None

      expanded_path_segments.append(sub_file_entry.name)
      number_of_expanded_path_segments += 1
      file_entry = sub_file_entry

    location = self._file_system.JoinPath(expanded_path_segments)
    return location, file_entry.path_spec

  def GetWindowsPath(self, path_spec):
    """Returns the Windows path based on a resolved path specification.

    Args:
      path_spec: the path specification (instance of path.PathSpec).

    Returns:
      The corresponding Windows path or None if the Windows path could not
      be determined.

    Raises:
      PathSpecError: if the path specification is incorrect.
    """
    location = getattr(path_spec, 'location', None)
    if location is None:
      raise errors.PathSpecError(u'Path specification missing location.')

    if self._mount_point.type_indicator in self._PARENTLESS_TYPE_INDICATORS:
      if not location.startswith(self._mount_point.location):
        raise errors.PathSpecError(
            u'Path specification does not contain mount point.')
    else:
      if not hasattr(path_spec, 'parent'):
        raise errors.PathSpecError(u'Path specification missing parent.')

      if path_spec.parent != self._mount_point:
        raise errors.PathSpecError(
            u'Path specification does not contain mount point.')

    path_segments = self._file_system.SplitPath(location)

    if self._mount_point.type_indicator in self._PARENTLESS_TYPE_INDICATORS:
      mount_point_path_segments = self._file_system.SplitPath(
          self._mount_point.location)
      path_segments = path_segments[len(mount_point_path_segments):]

    return u'{0:s}:\\{1:s}'.format(
        self._drive_letter, self._PATH_SEPARATOR.join(path_segments))

  def ResolvePath(self, path, expand_variables=True):
    """Resolves a Windows path in file system specific format.

    Args:
      path: the Windows path to resolve.
      expand_variables: optional value to indicate path variables should be
                        expanded or not. The default is to expand (True).

    Returns:
      The path specification (instance of path.PathSpec) in file system
      specific format.
    """
    location, path_spec = self._ResolvePath(
        path, expand_variables=expand_variables)

    if not location or not path_spec:
      return

    # Note that we don't want to set the keyword arguments when not used because
    # the path specification base class will check for unused keyword arguments
    # and raise.
    kwargs = path_spec_factory.Factory.GetProperties(path_spec)

    kwargs['location'] = location
    if self._mount_point.type_indicator not in self._PARENTLESS_TYPE_INDICATORS:
      kwargs['parent'] = self._mount_point

    return path_spec_factory.Factory.NewPathSpec(
        self._file_system.type_indicator, **kwargs)

  def SetEnvironmentVariable(self, name, value):
    """Sets an environment variable in the Windows path helper.

    Args:
      name: the name of the environment variable without enclosing
            %-characters, e.g. SystemRoot as in %SystemRoot%.
      value: the value of the environment variable.
    """
    value = self._PathStripPrefix(value)
    if value is not None:
      self._environment_variables[name.upper()] = value
