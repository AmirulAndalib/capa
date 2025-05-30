# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Union, Optional, Annotated, TypeAlias

from pydantic import Field, BaseModel, ConfigDict
from pydantic.functional_validators import BeforeValidator


def validate_hex_int(value):
    if isinstance(value, str):
        return int(value, 16) if value.startswith("0x") else int(value, 10)
    else:
        return value


def validate_hex_bytes(value):
    return bytes.fromhex(value) if isinstance(value, str) else value


HexInt = Annotated[int, BeforeValidator(validate_hex_int)]
HexBytes = Annotated[bytes, BeforeValidator(validate_hex_bytes)]


# a model that *cannot* have extra fields
# if they do, pydantic raises an exception.
# use this for models we rely upon and cannot change.
#
# for things that may be extended and we don't care,
# use FlexibleModel.
class ExactModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


# a model that can have extra fields that we ignore.
# use this if we don't want to raise an exception for extra
# data fields that we didn't expect.
class FlexibleModel(BaseModel):
    pass


# use this type to indicate that we won't model this data.
# because it's not relevant to our use in capa.
#
# while its nice to have full coverage of the data shape,
# it can easily change and break our parsing.
# so we really only want to describe what we'll use.
Skip: TypeAlias = Optional[Any]


# mark fields that we haven't seen yet and need to model.
# pydantic should raise an error when encountering data
# in a field with this type.
# then we can update the model with the discovered shape.
TODO: TypeAlias = None
ListTODO: TypeAlias = list[None]
DictTODO: TypeAlias = ExactModel

Emptydict: TypeAlias = BaseModel
EmptyList: TypeAlias = list[Any]


class Info(FlexibleModel):
    version: str


class ImportedSymbol(FlexibleModel):
    address: HexInt
    name: Optional[str] = None


class ImportedDll(FlexibleModel):
    dll: str
    imports: list[ImportedSymbol]


"""
class DirectoryEntry(FlexibleModel):
    name: str
    virtual_address: HexInt
    size: HexInt
"""


class Section(FlexibleModel):
    name: str
    # raw_address: HexInt
    virtual_address: HexInt
    # virtual_size: HexInt
    # size_of_data: HexInt
    # characteristics: str
    # characteristics_raw: HexInt
    # entropy: float


"""
class Resource(FlexibleModel):
    name: str
    language: Optional[str] = None
    sublanguage: str
    filetype: Optional[str]
    offset: HexInt
    size: HexInt
    entropy: float


class DigitalSigner(FlexibleModel):
    md5_fingerprint: str
    not_after: str
    not_before: str
    serial_number: str
    sha1_fingerprint: str
    sha256_fingerprint: str

    issuer_commonName: Optional[str] = None
    issuer_countryName: Optional[str] = None
    issuer_localityName: Optional[str] = None
    issuer_organizationName: Optional[str] = None
    issuer_stateOrProvinceName: Optional[str] = None

    subject_commonName: Optional[str] = None
    subject_countryName: Optional[str] = None
    subject_localityName: Optional[str] = None
    subject_organizationName: Optional[str] = None
    subject_stateOrProvinceName: Optional[str] = None

    extensions_authorityInfoAccess_caIssuers: Optional[str] = None
    extensions_authorityKeyIdentifier: Optional[str] = None
    extensions_cRLDistributionPoints_0: Optional[str] = None
    extensions_certificatePolicies_0: Optional[str] = None
    extensions_subjectAltName_0: Optional[str] = None
    extensions_subjectKeyIdentifier: Optional[str] = None


class AuxSigner(FlexibleModel):
    name: str
    issued_to: str = Field(alias="Issued to")
    issued_by: str = Field(alias="Issued by")
    expires: str = Field(alias="Expires")
    sha1_hash: str = Field(alias="SHA1 hash")


class Signer(FlexibleModel):
    aux_sha1: Optional[str] = None
    aux_timestamp: Optional[str] = None
    aux_valid: Optional[bool] = None
    aux_error: Optional[bool] = None
    aux_error_desc: Optional[str] = None
    aux_signers: Optional[list[AuxSigner]] = None


class Overlay(FlexibleModel):
    offset: HexInt
    size: HexInt


class KV(FlexibleModel):
    name: str
    value: str
"""


class ExportedSymbol(FlexibleModel):
    address: HexInt
    name: str
    # ordinal: int


class PE(FlexibleModel):
    # peid_signatures: TODO
    imagebase: HexInt
    # entrypoint: HexInt
    # reported_checksum: HexInt
    # actual_checksum: HexInt
    # osversion: str
    # pdbpath: Optional[str] = None
    # timestamp: str

    # list[ImportedDll], or dict[basename(dll), ImportedDll]
    imports: list[ImportedDll] | dict[str, ImportedDll] = Field(default_factory=list)  # type: ignore
    # imported_dll_count: Optional[int] = None
    # imphash: str

    # exported_dll_name: Optional[str] = None
    exports: list[ExportedSymbol] = Field(default_factory=list)

    # dirents: list[DirectoryEntry]
    sections: list[Section] = Field(default_factory=list)

    # ep_bytes: Optional[HexBytes] = None

    # overlay: Optional[Overlay] = None
    # resources: list[Resource]
    # versioninfo: list[KV]

    # base64 encoded data
    # icon: Optional[str] = None
    # MD5-like hash
    # icon_hash: Optional[str] = None
    # MD5-like hash
    # icon_fuzzy: Optional[str] = None
    # short hex string
    # icon_dhash: Optional[str] = None

    # digital_signers: list[DigitalSigner]
    # guest_signers: Signer


# TODO(mr-tz): target.file.dotnet, target.file.extracted_files, target.file.extracted_files_tool,
#  target.file.extracted_files_time
# https://github.com/mandiant/capa/issues/1814
class File(FlexibleModel):
    type: str
    # cape_type_code: Optional[int] = None
    # cape_type: Optional[str] = None

    # pid: Optional[Union[int, Literal[""]]] = None
    # name: Union[list[str], str]
    # path: str
    # guest_paths: Union[list[str], str, None]
    # timestamp: Optional[str] = None

    #
    # hashes
    #
    # crc32: str
    md5: str
    sha1: str
    sha256: str
    # sha512: str
    # sha3_384: Optional[str] = None
    # ssdeep: str
    # unsure why this would ever be "False"
    # tlsh: Optional[Union[str, bool]] = None
    # rh_hash: Optional[str] = None

    #
    # other metadata, static analysis
    #
    # size: int
    pe: Optional[PE] = None
    # ep_bytes: Optional[HexBytes] = None
    # entrypoint: Optional[int] = None
    # data: Optional[str] = None
    # strings: Optional[list[str]] = None

    #
    # detections (skip)
    #
    # yara: Skip = None
    # cape_yara: Skip = None
    # clamav: Skip = None
    # virustotal: Skip = None


"""
class ProcessFile(File):
    #
    # like a File, but also has dynamic analysis results
    #
    pid: Optional[int] = None
    process_path: Optional[str] = None
    process_name: Optional[str] = None
    module_path: Optional[str] = None
    virtual_address: Optional[HexInt] = None
    target_pid: Optional[Union[int, str]] = None
    target_path: Optional[str] = None
    target_process: Optional[str] = None
"""


class Argument(FlexibleModel):
    name: str
    # unsure why empty list is provided here
    value: Union[HexInt, int, str, EmptyList]
    pretty_value: Optional[str] = None


class Call(FlexibleModel):
    # timestamp: str
    thread_id: int
    # category: str

    api: str

    arguments: list[Argument]
    # status: bool
    return_: HexInt = Field(alias="return")
    pretty_return: Optional[str] = None

    # repeated: int

    # virtual addresses
    # caller: HexInt
    # parentcaller: HexInt

    # index into calls array
    # id: int


# FlexibleModel to account for extended fields
# refs: https://github.com/mandiant/capa/issues/2466
# https://github.com/kevoreilly/CAPEv2/pull/2199
class Process(FlexibleModel):
    process_id: int
    process_name: str
    parent_id: int
    # module_path: str
    # first_seen: str
    calls: list[Call]
    threads: list[int]
    environ: dict[str, str]


"""
class ProcessTree(FlexibleModel):
    name: str
    pid: int
    parent_id: int
    module_path: str
    threads: list[int]
    environ: dict[str, str]
    children: list["ProcessTree"]
"""


class Summary(FlexibleModel):
    files: list[str]
    # read_files: list[str]
    # write_files: list[str]
    # delete_files: list[str]
    keys: list[str]
    # read_keys: list[str]
    # write_keys: list[str]
    # delete_keys: list[str]
    executed_commands: list[str]
    resolved_apis: list[str]
    mutexes: list[str]
    created_services: list[str]
    started_services: list[str]


"""
class EncryptedBuffer(FlexibleModel):
    process_name: str
    pid: int

    api_call: str
    buffer: str
    buffer_size: Optional[int] = None
    crypt_key: Optional[Union[HexInt, str]] = None
"""


class Behavior(FlexibleModel):
    summary: Summary | None = None

    # list of processes, of threads, of calls
    processes: list[Process]
    # tree of processes
    # processtree: list[ProcessTree]

    # anomaly: list[str]
    # encryptedbuffers: list[EncryptedBuffer]
    # these are small objects that describe atomic events,
    # like file move, registry access.
    # we'll detect the same with our API call analysis.
    # enhanced: Skip = None


class Target(FlexibleModel):
    # category: str
    file: File
    # pe: Optional[PE] = None


class Static(FlexibleModel):
    pe: Optional[PE] = None
    # flare_capa: Skip = None


"""
class Cape(FlexibleModel):
    payloads: list[ProcessFile]
    configs: Skip = None
"""


# flexible because there may be more sorts of analysis
# but we only care about the ones described here.
class CapeReport(FlexibleModel):
    # the input file, I think
    target: Target
    # info about the processing job, like machine and distributed metadata.
    info: Info

    #
    # static analysis results
    #
    static: Optional[Static] = None
    strings: Optional[list[str]] = None

    #
    # dynamic analysis results
    #
    # post-processed results: process tree, anomalies, etc
    behavior: Behavior

    # =========================================================================
    # information we won't use in capa
    #
    # post-processed results: payloads and extracted configs
    # CAPE: Optional[Union[Cape, list]] = None
    # dropped: Optional[list[File]] = None
    # procdump: Optional[list[ProcessFile]] = None
    # procmemory: Optional[ListTODO] = None

    #
    # NBIs and HBIs
    # these are super interesting, but they don't enable use to detect behaviors.
    # they take a lot of code to model and details to maintain.
    #
    # if we come up with a future use for this, go ahead and re-enable!
    #
    # network: Skip = None
    # suricata: Skip = None
    # curtain: Skip = None
    # sysmon: Skip = None
    # url_analysis: Skip = None

    # screenshot hash values
    # deduplicated_shots: Skip = None
    # k-v pairs describing the time it took to run each stage.
    # statistics: Skip = None
    # k-v pairs of ATT&CK ID to signature name or similar.
    # ttps: Skip = None
    # debug log messages
    # debug: Skip = None

    # various signature matches
    # we could potentially extend capa to use this info one day,
    # though it would be quite sandbox-specific,
    # and more detection-oriented than capability detection.
    # signatures: Skip = None
    # malfamily_tag: Optional[str] = None
    # malscore: float
    # detections: Skip = None
    # detections2pid: Optional[dict[int, list[str]]] = None
    # AV detections for the sample.
    # virustotal: Skip = None

    @classmethod
    def from_buf(cls, buf: bytes) -> "CapeReport":
        return cls.model_validate_json(buf)
