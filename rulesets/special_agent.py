#!/usr/bin/env python3

from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic, Help, Title
from cmk.rulesets.v1.form_specs import Dictionary, DictElement, String, Password, migrate_to_password, DefaultValue
from cmk.rulesets.v1.form_specs import BooleanChoice, DefaultValue, Float, LevelDirection, SimpleLevels
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


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

def _parameter_form():
    return Dictionary(
        elements = {
            "latency_reads": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Latency Reads Threshold μs"),
                    form_spec_template = Float(),
                    level_direction = LevelDirection.UPPER,
                    prefill_fixed_levels = DefaultValue(value=(20000, 25000)),
                ),
                required = True,
            ),
            "latency_writes": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Latency Writes Threshold μs"),
                    form_spec_template = Float(),
                    level_direction = LevelDirection.UPPER,
                    prefill_fixed_levels = DefaultValue(value=(25000, 30000)),
                ),
                required = True,
            ),            
        }
    )


rule_spec_simplivity = SpecialAgent(
    topic=Topic.ENVIRONMENTAL,
    name="simplivity",
    title=Title("HPE Simplivity"),
    parameter_form=_formspec
)

rule_spec_thresholds = CheckParameters(
    name = "simplivity_thresholds",
    title = Title("HPE Simplivity Thresholds"),
    topic = Topic.GENERAL,
    parameter_form = _parameter_form,
    condition = HostCondition(),
)