#!/usr/bin/env python3

from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic, Help, Title
from cmk.rulesets.v1.form_specs import Dictionary, DictElement, String, Password, migrate_to_password, DefaultValue

def _formspec():
    return Dictionary(
        title=Title("HPE Simplivity"),
        help_text=Help("This rule is used to showcase a special agent with configuration."),
        elements={
             "user": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("User for login"),
                    prefill=DefaultValue("monitoring"),
                ),
            ),
            "password": DictElement(
                required=True,
                parameter_form=Password(
                    title=Title("Password for this user"),
                    migrate=migrate_to_password,
                ),
            ),
        }
    )

rule_spec_ometemp = SpecialAgent(
    topic=Topic.ENVIRONMENTAL,
    name="simplivity",
    title=Title("HPE Simplivity"),
    parameter_form=_formspec
)