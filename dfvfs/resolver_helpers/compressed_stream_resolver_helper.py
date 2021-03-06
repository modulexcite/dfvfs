# -*- coding: utf-8 -*-
"""The compressed stream path specification resolver helper implementation."""

from __future__ import unicode_literals

from dfvfs.file_io import compressed_stream_io
from dfvfs.lib import definitions
from dfvfs.resolver_helpers import manager
from dfvfs.resolver_helpers import resolver_helper
from dfvfs.vfs import compressed_stream_file_system


class CompressedStreamResolverHelper(resolver_helper.ResolverHelper):
  """Compressed stream resolver helper."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_COMPRESSED_STREAM

  def NewFileObject(self, resolver_context):
    """Creates a new file-like object.

    Args:
      resolver_context (Context): resolver context.

    Returns:
      FileIO: file-like object.
    """
    return compressed_stream_io.CompressedStream(resolver_context)

  def NewFileSystem(self, resolver_context):
    """Creates a new file system object.

    Args:
      resolver_context (Context): resolver context.

    Returns:
      FileSystem: file system.
    """
    return compressed_stream_file_system.CompressedStreamFileSystem(
        resolver_context)


manager.ResolverHelperManager.RegisterHelper(CompressedStreamResolverHelper())
