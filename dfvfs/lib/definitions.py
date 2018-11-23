# -*- coding: utf-8 -*-
"""The Virtual File System (VFS) definitions."""

from __future__ import unicode_literals


# The compression method definitions.
COMPRESSION_METHOD_BZIP2 = 'bzip2'
COMPRESSION_METHOD_DEFLATE = 'deflate'
COMPRESSION_METHOD_LZMA = 'lzma'
COMPRESSION_METHOD_XZ = 'xz'
COMPRESSION_METHOD_ZLIB = 'zlib'

# The encoding method definitions.
ENCODING_METHOD_BASE16 = 'base16'
ENCODING_METHOD_BASE32 = 'base32'
ENCODING_METHOD_BASE64 = 'base64'

# The encryption method definitions.
ENCRYPTION_METHOD_AES = 'aes'
ENCRYPTION_METHOD_BLOWFISH = 'blowfish'
ENCRYPTION_METHOD_DES3 = 'des3'
ENCRYPTION_METHOD_RC4 = 'rc4'

# The encryption mode of operations.
ENCRYPTION_MODE_CBC = 'cbc'
ENCRYPTION_MODE_CFB = 'cfb'
ENCRYPTION_MODE_ECB = 'ecb'
ENCRYPTION_MODE_OFB = 'ofb'

# The type indicator definitions.
TYPE_INDICATOR_APFS = 'APFS'
TYPE_INDICATOR_APFS_CONTAINER = 'APFS_CONTAINER'
TYPE_INDICATOR_BDE = 'BDE'
TYPE_INDICATOR_BZIP2 = 'BZIP2'
TYPE_INDICATOR_COMPRESSED_STREAM = 'COMPRESSED_STREAM'
TYPE_INDICATOR_CPIO = 'CPIO'
TYPE_INDICATOR_DATA_RANGE = 'DATA_RANGE'
TYPE_INDICATOR_ENCODED_STREAM = 'ENCODED_STREAM'
TYPE_INDICATOR_ENCRYPTED_STREAM = 'ENCRYPTED_STREAM'
TYPE_INDICATOR_EWF = 'EWF'
TYPE_INDICATOR_FAKE = 'FAKE'
TYPE_INDICATOR_FVDE = 'FVDE'
TYPE_INDICATOR_GZIP = 'GZIP'
TYPE_INDICATOR_LVM = 'LVM'
TYPE_INDICATOR_MOUNT = 'MOUNT'
TYPE_INDICATOR_NTFS = 'NTFS'
TYPE_INDICATOR_OS = 'OS'
TYPE_INDICATOR_QCOW = 'QCOW'
TYPE_INDICATOR_RAW = 'RAW'
TYPE_INDICATOR_SQLITE_BLOB = 'SQLITE_BLOB'
TYPE_INDICATOR_TAR = 'TAR'
TYPE_INDICATOR_TSK = 'TSK'
TYPE_INDICATOR_TSK_PARTITION = 'TSK_PARTITION'
TYPE_INDICATOR_VHDI = 'VHDI'
TYPE_INDICATOR_VMDK = 'VMDK'
TYPE_INDICATOR_VSHADOW = 'VSHADOW'
TYPE_INDICATOR_ZIP = 'ZIP'

ENCRYPTED_VOLUME_TYPE_INDICATORS = frozenset([
    TYPE_INDICATOR_BDE,
    TYPE_INDICATOR_FVDE])

FILE_SYSTEM_TYPE_INDICATORS = frozenset([
    TYPE_INDICATOR_APFS,
    TYPE_INDICATOR_NTFS,
    TYPE_INDICATOR_TSK])

STORAGE_MEDIA_IMAGE_TYPE_INDICATORS = frozenset([
    TYPE_INDICATOR_EWF,
    TYPE_INDICATOR_QCOW,
    TYPE_INDICATOR_RAW,
    TYPE_INDICATOR_VHDI,
    TYPE_INDICATOR_VMDK])

VOLUME_SYSTEM_TYPE_INDICATORS = frozenset([
    TYPE_INDICATOR_APFS_CONTAINER,
    TYPE_INDICATOR_LVM,
    TYPE_INDICATOR_TSK_PARTITION,
    TYPE_INDICATOR_VSHADOW])

# The preferred back-ends.
PREFERRED_NTFS_BACK_END = TYPE_INDICATOR_TSK

# The NTFS attribute types.
ATTRIBUTE_TYPE_NTFS_FILE_NAME = 'NTFS:$FILE_NAME'
ATTRIBUTE_TYPE_NTFS_OBJECT_ID = 'NTFS:$OBJECT_ID'
ATTRIBUTE_TYPE_NTFS_SECURITY_DESCRIPTOR = 'NTFS:$SECURITY_DESCRIPTOR'
ATTRIBUTE_TYPE_NTFS_STANDARD_INFORMATION = 'NTFS:$STANDARD_INFORMATION'

# The file entry types.
FILE_ENTRY_TYPE_DEVICE = 'device'
FILE_ENTRY_TYPE_DIRECTORY = 'directory'
FILE_ENTRY_TYPE_FILE = 'file'
FILE_ENTRY_TYPE_LINK = 'link'
FILE_ENTRY_TYPE_SOCKET = 'socket'
FILE_ENTRY_TYPE_PIPE = 'pipe'
FILE_ENTRY_TYPE_WHITEOUT = 'whiteout'

# The format category definitions.
FORMAT_CATEGORY_UNDEFINED = 0
FORMAT_CATEGORY_ARCHIVE = 1
FORMAT_CATEGORY_COMPRESSED_STREAM = 2
FORMAT_CATEGORY_ENCODED_STREAM = 3
FORMAT_CATEGORY_FILE_SYSTEM = 4
FORMAT_CATEGORY_STORAGE_MEDIA_IMAGE = 5
FORMAT_CATEGORY_VOLUME_SYSTEM = 6

FORMAT_CATEGORIES = frozenset([
    FORMAT_CATEGORY_UNDEFINED,
    FORMAT_CATEGORY_ARCHIVE,
    FORMAT_CATEGORY_COMPRESSED_STREAM,
    FORMAT_CATEGORY_ENCODED_STREAM,
    FORMAT_CATEGORY_FILE_SYSTEM,
    FORMAT_CATEGORY_STORAGE_MEDIA_IMAGE,
    FORMAT_CATEGORY_VOLUME_SYSTEM])

# The source type definitions.
SOURCE_TYPE_DIRECTORY = 'directory'
SOURCE_TYPE_FILE = 'file'
SOURCE_TYPE_STORAGE_MEDIA_DEVICE = 'storage media device'
SOURCE_TYPE_STORAGE_MEDIA_IMAGE = 'storage media image'
