from pathlib import Path
import ast


print(Path(__file__).parent)
spec = '''
name: CustomAgent
nodes:
  - name: model
  - name: tools
  - name: Node 1
edges:
  - from: Node 1
    to: __end__
  - from: tools
    to: model
  - from: __start__
    condition: conditional_edge_1
    paths: [model, Node 1]
  - from: model
    condition: route_after_model
    paths: [tools, __end__]
'''


language = ".py"
# Get the implementation relative to the output path
# stub_module = _rewrite_path_as_import(
#     output_path.relative_to(implementation.parent)
# )
    # stub_module=stub_module,

stub_module = "langgraph_gen"
from langgraphgenpy.langgraph_gen.generate import generate_from_spec
spec_as_yaml = spec
stub, impl = generate_from_spec(
    spec_as_yaml,
    "yaml",
    templates=["stub", "implementation"],
    language=language

)
print(stub)
print("----------------")
print(impl)


def test_generate_from_yaml() -> None:
    """Simple end-to-end test to verify that valid python code is generated"""
    stub = generate_from_spec(
        spec, "yaml", language="python", templates=["stub"]
    )[0]
    # Try to parse the ast to verify it works
    ast.parse(stub)


    # Try to exec the code to verify it works
    # Prepare a globals dictionary that simulates the main module environment
    globals_dict = {
        "__name__": "__main__",
        "__file__": "your_script.py",
        "__package__": None,
    }

    # Exec is safe in this context since all the code is fully controlled by us
    # and it appears only on the test path.
    # exec(stub, globals_dict)
