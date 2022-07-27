#!/usr/bin/env python3
import zope.interface

from colrev_core.process import PreparationEndpoint
from colrev_core.built_in.prescreen import ScopePrescreenEndpoint 
from colrev_core.process import DefaultSettings
from dacite import from_dict


@zope.interface.implementer(PreparationEndpoint)
class CustomPrepare:

    source_correction_hint = "check with the developer"
    always_apply_changes = True

    additional_title_complementary_materials_keywords = ['acknowledgment of reviewers', 'acknowledgment to reviewers']

    def __init__(self, *, SETTINGS):
        self.SETTINGS = from_dict(data_class=DefaultSettings, data=SETTINGS)

    def prepare(self, PREPARATION, RECORD):

        if "title" in RECORD.data:
            if any(x == RECORD.data['title'].lower() for x in ScopePrescreenEndpoint.title_complementary_materials_keywords) :
                RECORD.prescreen_exclude(
                    reason="complementary material"
                )
            for k in self.additional_title_complementary_materials_keywords:
                if k in RECORD.data["title"].lower():
                    RECORD.prescreen_exclude(
                        reason="complementary material"
                    )

        return RECORD


if __name__ == "__main__":
    pass
