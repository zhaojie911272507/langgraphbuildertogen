import ast

from langgraphgenpy.langgraph_gen.generate import generate_from_spec

SAMPLE_YAML = """\
# agent_graph.yaml
entrypoint: start
nodes:
  - name: start
  - name: process
  - name: decide
edges:
  - from: start
    to: process
  - from: process
    to: decide
  - from: decide
    condition: check_decision
    paths:
      continue: process
      end: __end__
"""
# agnet yml 验证生成的文件是否会变化
SAMPLE_YAML = """\
# agent_graph.yaml
entrypoint: start
name: CustomAgent
nodes:
  - name: model
  - name: tools
edges:
  - from: __start__
    to: model
  - from: tools
    to: model
  - from: model
    condition: route_after_model
    paths: [tools, __end__]
"""

def test_generate_from_yaml() -> None:
    """Simple end-to-end test to verify that valid python code is generated"""
    stub = generate_from_spec(
        SAMPLE_YAML, "yaml", language="python", templates=["stub"]
    )[0]
    print(stub)
    # Try to parse the ast to verify it works
    ast.parse(stub)
    
    # Try to exec the code to verify it works
    # Prepare a globals dictionary that simulates the main module environment
    globals_dict = {
        "__name__": "__main__",
        "__file__": "your_script.py",
        "__package__": None,
    }
    print(globals_dict)
    # Exec is safe in this context since all the code is fully controlled by us
    # and it appears only on the test path.
    exec(stub, globals_dict)




JSON_SPEC = """\
{
  "entrypoint": "start",
  "nodes": [
    { "name": "start" },
    { "name": "process" },
    { "name": "decide" }
  ],
  "edges": [
    { "from": "start", "to": "process" },
    { "from": "process", "to": "decide" },
    {
      "from": "decide",
      "condition": "check_decision",
      "paths": {
        "continue": "process",
        "end": "__end__"
      }
    }
  ]
}
"""


def test_generate_from_json() -> None:
    """Simple end-to-end test to verify that valid python code is generated"""
    code = generate_from_spec(JSON_SPEC, "json", language="python", templates=["stub"])[
        0
    ]
    # Try to parse the ast to verify it works
    ast.parse(code)
    # Try to exec the code to verify it works
    # Prepare a globals dictionary that simulates the main module environment
    globals_dict = {
        "__name__": "__main__",
        "__file__": "your_script.py",
        "__package__": None,
    }

    # Exec is safe in this context since all the code is fully controlled by us
    # and it appears only on the test path.
    exec(code, globals_dict)


def test_generate_from_yaml_typescript() -> None:
    """Simple end-to-end test to verify that valid python code is generated"""
    code = generate_from_spec(
        SAMPLE_YAML, "yaml", language="typescript", templates=["stub"]
    )[0]
    assert isinstance(code, str)


THREE_NODE_SEQUENCE_YAML = """\
# agent_graph.yaml
entrypoint: node1
nodes:
  - name: node1
  - name: node2
  - name: node3
edges:
  - from: node1
    to: node2
  - from: node2
    to: node3
"""


def test_stub_and_implementation() -> None:
    """Test stub and generated implementation for a simple 3 node graph."""
    stub, impl = generate_from_spec(
        THREE_NODE_SEQUENCE_YAML,
        "yaml",
        language="python",
        templates=["stub", "implementation"],
    )
    # Try to parse the ast to verify it works
    ast.parse(stub)
    ast.parse(impl)

    # Try to exec the code to verify it works
    # Prepare a globals dictionary that simulates the main module environment
    globals_dict = {
        "__name__": "__main__",
        "__file__": "your_script.py",
        "__package__": None,
    }

    # Exec is safe in this context since all the code is fully controlled by us
    # and it appears only on the test path.
    exec(stub, globals_dict)

    exec(impl, globals_dict)


NON_MACHINE_FRIENDLY_NAMES_YAML = """\
# agent_graph.yaml
entrypoint: node-1
nodes:
  - name: node-1
  - name: node-2
  - name: node-3
edges:
  - from: node-1
    to: node-2
  - from: node-2
    to: node-3
"""

NON_MACHINE_FRIENDLY_NAMES_YAML = """\
# agent_graph.yaml
name: CustomAgent
nodes:
  - name: model
  - name: tools
edges:
  - from: __start__
    to: model
  - from: tools
    to: model
  - from: model
    condition: route_after_model
    paths: [tools, __end__]
"""


def test_generation_with_human_names() -> None:
    """Test generation with non machine-friendly names."""
    stub, impl = generate_from_spec(
        NON_MACHINE_FRIENDLY_NAMES_YAML,
        "yaml",
        language="python",
        templates=["stub", "implementation"]
    )
    # Try to parse the ast to verify it works
    ast.parse(stub)
    ast.parse(impl)
    print(stub)
    print("------------------")
    print(impl)
    # Try to exec the code to verify it works
    # Prepare a globals dictionary that simulates the main module environment
    # globals_dict = {
    #     "__name__": "__main__",
    #     "__file__": "your_script.py",
    #     "__package__": None,
    # }

    # Exec is safe in this context since all the code is fully controlled by us
    # and it appears only on the test path.
    # exec(stub, globals_dict)

    # exec(impl, globals_dict)

test_generation_with_human_names()
print("success")
