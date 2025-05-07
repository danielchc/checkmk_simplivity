#!/usr/bin/env python3

from cmk.server_side_calls.v1 import noop_parser, SpecialAgentConfig, SpecialAgentCommand

def _agent_arguments(params, host_config):
    args = [
        "--user", params['user'],
        "--password", params['password'].unsafe(),
        "--hostname", host_config.name,
    ]
    yield SpecialAgentCommand(command_arguments=args)
    
special_agent_hellospecial = SpecialAgentConfig(
    name="simplivity",
    parameter_parser=noop_parser,
    commands_function=_agent_arguments
)