# Copyright 2022 Google LLC
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

from typing import Union, Literal, Optional, Annotated

from pydantic import Field, BaseModel, ConfigDict

import capa.features.file
import capa.features.insn
import capa.features.common
import capa.features.basicblock


class FeatureModel(BaseModel):
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    def to_capa(self) -> capa.features.common.Feature:
        if isinstance(self, OSFeature):
            return capa.features.common.OS(self.os, description=self.description)

        elif isinstance(self, ArchFeature):
            return capa.features.common.Arch(self.arch, description=self.description)

        elif isinstance(self, FormatFeature):
            return capa.features.common.Format(self.format, description=self.description)

        elif isinstance(self, MatchFeature):
            return capa.features.common.MatchedRule(self.match, description=self.description)

        elif isinstance(
            self,
            CharacteristicFeature,
        ):
            return capa.features.common.Characteristic(self.characteristic, description=self.description)

        elif isinstance(self, ExportFeature):
            return capa.features.file.Export(self.export, description=self.description)

        elif isinstance(self, ImportFeature):
            return capa.features.file.Import(self.import_, description=self.description)

        elif isinstance(self, SectionFeature):
            return capa.features.file.Section(self.section, description=self.description)

        elif isinstance(self, FunctionNameFeature):
            return capa.features.file.FunctionName(self.function_name, description=self.description)

        elif isinstance(self, SubstringFeature):
            return capa.features.common.Substring(self.substring, description=self.description)

        elif isinstance(self, RegexFeature):
            return capa.features.common.Regex(self.regex, description=self.description)

        elif isinstance(self, StringFeature):
            return capa.features.common.String(self.string, description=self.description)

        elif isinstance(self, ClassFeature):
            return capa.features.common.Class(self.class_, description=self.description)

        elif isinstance(self, NamespaceFeature):
            return capa.features.common.Namespace(self.namespace, description=self.description)

        elif isinstance(self, BasicBlockFeature):
            return capa.features.basicblock.BasicBlock(description=self.description)

        elif isinstance(self, APIFeature):
            return capa.features.insn.API(self.api, description=self.description)

        elif isinstance(self, PropertyFeature):
            return capa.features.insn.Property(self.property, access=self.access, description=self.description)

        elif isinstance(self, NumberFeature):
            return capa.features.insn.Number(self.number, description=self.description)

        elif isinstance(self, BytesFeature):
            return capa.features.common.Bytes(bytes.fromhex(self.bytes), description=self.description)

        elif isinstance(self, OffsetFeature):
            return capa.features.insn.Offset(self.offset, description=self.description)

        elif isinstance(self, MnemonicFeature):
            return capa.features.insn.Mnemonic(self.mnemonic, description=self.description)

        elif isinstance(self, OperandNumberFeature):
            return capa.features.insn.OperandNumber(
                self.index,
                self.operand_number,
                description=self.description,
            )

        elif isinstance(self, OperandOffsetFeature):
            return capa.features.insn.OperandOffset(
                self.index,
                self.operand_offset,
                description=self.description,
            )

        else:
            raise NotImplementedError(f"Feature.to_capa({type(self)}) not implemented")


def feature_from_capa(f: capa.features.common.Feature) -> "Feature":
    if isinstance(f, capa.features.common.OS):
        assert isinstance(f.value, str)
        return OSFeature(os=f.value, description=f.description)

    elif isinstance(f, capa.features.common.Arch):
        assert isinstance(f.value, str)
        return ArchFeature(arch=f.value, description=f.description)

    elif isinstance(f, capa.features.common.Format):
        assert isinstance(f.value, str)
        return FormatFeature(format=f.value, description=f.description)

    elif isinstance(f, capa.features.common.MatchedRule):
        assert isinstance(f.value, str)
        return MatchFeature(match=f.value, description=f.description)

    elif isinstance(f, capa.features.common.Characteristic):
        assert isinstance(f.value, str)
        return CharacteristicFeature(characteristic=f.value, description=f.description)

    elif isinstance(f, capa.features.file.Export):
        assert isinstance(f.value, str)
        return ExportFeature(export=f.value, description=f.description)

    elif isinstance(f, capa.features.file.Import):
        assert isinstance(f.value, str)
        return ImportFeature(import_=f.value, description=f.description)  # type: ignore
        # Mypy is unable to recognise `import_` as an argument due to alias

    elif isinstance(f, capa.features.file.Section):
        assert isinstance(f.value, str)
        return SectionFeature(section=f.value, description=f.description)

    elif isinstance(f, capa.features.file.FunctionName):
        assert isinstance(f.value, str)
        return FunctionNameFeature(function_name=f.value, description=f.description)  # type: ignore
        # Mypy is unable to recognise `function_name` as an argument due to alias

    # must come before check for String due to inheritance
    elif isinstance(f, capa.features.common.Substring):
        assert isinstance(f.value, str)
        return SubstringFeature(substring=f.value, description=f.description)

    # must come before check for String due to inheritance
    elif isinstance(f, capa.features.common.Regex):
        assert isinstance(f.value, str)
        return RegexFeature(regex=f.value, description=f.description)

    elif isinstance(f, capa.features.common.String):
        assert isinstance(f.value, str)
        return StringFeature(string=f.value, description=f.description)

    elif isinstance(f, capa.features.common.Class):
        assert isinstance(f.value, str)
        return ClassFeature(class_=f.value, description=f.description)  # type: ignore
        # Mypy is unable to recognise `class_` as an argument due to alias

    elif isinstance(f, capa.features.common.Namespace):
        assert isinstance(f.value, str)
        return NamespaceFeature(namespace=f.value, description=f.description)

    elif isinstance(f, capa.features.basicblock.BasicBlock):
        return BasicBlockFeature(description=f.description)

    elif isinstance(f, capa.features.insn.API):
        assert isinstance(f.value, str)
        return APIFeature(api=f.value, description=f.description)

    elif isinstance(f, capa.features.insn.Property):
        assert isinstance(f.value, str)
        return PropertyFeature(property=f.value, access=f.access, description=f.description)

    elif isinstance(f, capa.features.insn.Number):
        assert isinstance(f.value, (int, float))
        return NumberFeature(number=f.value, description=f.description)

    elif isinstance(f, capa.features.common.Bytes):
        buf = f.value
        assert isinstance(buf, bytes)
        return BytesFeature(bytes=bytes.hex(buf), description=f.description)

    elif isinstance(f, capa.features.insn.Offset):
        assert isinstance(f.value, int)
        return OffsetFeature(offset=f.value, description=f.description)

    elif isinstance(f, capa.features.insn.Mnemonic):
        assert isinstance(f.value, str)
        return MnemonicFeature(mnemonic=f.value, description=f.description)

    elif isinstance(f, capa.features.insn.OperandNumber):
        assert isinstance(f.value, int)
        return OperandNumberFeature(index=f.index, operand_number=f.value, description=f.description)  # type: ignore
        # Mypy is unable to recognise `operand_number` as an argument due to alias

    elif isinstance(f, capa.features.insn.OperandOffset):
        assert isinstance(f.value, int)
        return OperandOffsetFeature(index=f.index, operand_offset=f.value, description=f.description)  # type: ignore
        # Mypy is unable to recognise `operand_offset` as an argument due to alias

    else:
        raise NotImplementedError(f"feature_from_capa({type(f)}) not implemented")


class OSFeature(FeatureModel):
    type: Literal["os"] = "os"
    os: str
    description: Optional[str] = None


class ArchFeature(FeatureModel):
    type: Literal["arch"] = "arch"
    arch: str
    description: Optional[str] = None


class FormatFeature(FeatureModel):
    type: Literal["format"] = "format"
    format: str
    description: Optional[str] = None


class MatchFeature(FeatureModel):
    type: Literal["match"] = "match"
    match: str
    description: Optional[str] = None


class CharacteristicFeature(FeatureModel):
    type: Literal["characteristic"] = "characteristic"
    characteristic: str
    description: Optional[str] = None


class ExportFeature(FeatureModel):
    type: Literal["export"] = "export"
    export: str
    description: Optional[str] = None


class ImportFeature(FeatureModel):
    type: Literal["import"] = "import"
    import_: str = Field(alias="import")
    description: Optional[str] = None


class SectionFeature(FeatureModel):
    type: Literal["section"] = "section"
    section: str
    description: Optional[str] = None


class FunctionNameFeature(FeatureModel):
    type: Literal["function name"] = "function name"
    function_name: str = Field(alias="function name")
    description: Optional[str] = None


class SubstringFeature(FeatureModel):
    type: Literal["substring"] = "substring"
    substring: str
    description: Optional[str] = None


class RegexFeature(FeatureModel):
    type: Literal["regex"] = "regex"
    regex: str
    description: Optional[str] = None


class StringFeature(FeatureModel):
    type: Literal["string"] = "string"
    string: str
    description: Optional[str] = None


class ClassFeature(FeatureModel):
    type: Literal["class"] = "class"
    class_: str = Field(alias="class")
    description: Optional[str] = None


class NamespaceFeature(FeatureModel):
    type: Literal["namespace"] = "namespace"
    namespace: str
    description: Optional[str] = None


class BasicBlockFeature(FeatureModel):
    type: Literal["basic block"] = "basic block"
    description: Optional[str] = None


class APIFeature(FeatureModel):
    type: Literal["api"] = "api"
    api: str
    description: Optional[str] = None


class PropertyFeature(FeatureModel):
    type: Literal["property"] = "property"
    access: Optional[str] = None
    property: str
    description: Optional[str] = None


class NumberFeature(FeatureModel):
    type: Literal["number"] = "number"
    number: Union[int, float]
    description: Optional[str] = None


class BytesFeature(FeatureModel):
    type: Literal["bytes"] = "bytes"
    bytes: str
    description: Optional[str] = None


class OffsetFeature(FeatureModel):
    type: Literal["offset"] = "offset"
    offset: int
    description: Optional[str] = None


class MnemonicFeature(FeatureModel):
    type: Literal["mnemonic"] = "mnemonic"
    mnemonic: str
    description: Optional[str] = None


class OperandNumberFeature(FeatureModel):
    type: Literal["operand number"] = "operand number"
    index: int
    operand_number: int = Field(alias="operand number")
    description: Optional[str] = None


class OperandOffsetFeature(FeatureModel):
    type: Literal["operand offset"] = "operand offset"
    index: int
    operand_offset: int = Field(alias="operand offset")
    description: Optional[str] = None


Feature = Annotated[
    Union[
        OSFeature,
        ArchFeature,
        FormatFeature,
        MatchFeature,
        CharacteristicFeature,
        ExportFeature,
        ImportFeature,
        SectionFeature,
        FunctionNameFeature,
        SubstringFeature,
        RegexFeature,
        StringFeature,
        ClassFeature,
        NamespaceFeature,
        APIFeature,
        PropertyFeature,
        NumberFeature,
        BytesFeature,
        OffsetFeature,
        MnemonicFeature,
        OperandNumberFeature,
        OperandOffsetFeature,
        # Note! this must be last, see #1161
        BasicBlockFeature,
    ],
    Field(discriminator="type"),
]
