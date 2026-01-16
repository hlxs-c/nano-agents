import pytest
import asyncio
from pydantic import BaseModel
from nano_agents.tools.base_tool import BaseTool

class MockInput(BaseModel):
    value: str

class MockOutput(BaseModel):
    result: str

class MockTool(BaseTool[MockInput, MockOutput]):
    name = "mock_tool"
    description = "A mock tool for testing"
    args_schema = MockInput

    def _run(self, args: MockInput) -> MockOutput:
        return MockOutput(result=f"processed {args.value}")

class AsyncMockTool(BaseTool[MockInput, MockOutput]):
    name = "async_mock_tool"
    description = "An async mock tool for testing"
    args_schema = MockInput

    def _run(self, args: MockInput) -> MockOutput:
        raise NotImplementedError("Should use _arun")

    async def _arun(self, args: MockInput) -> MockOutput:
        await asyncio.sleep(0.01)
        return MockOutput(result=f"async processed {args.value}")

def test_base_tool_sync_run():
    tool = MockTool()
    result = tool.run(value="test")
    assert result.result == "processed test"

@pytest.mark.asyncio
async def test_base_tool_async_run():
    tool = AsyncMockTool()
    # verify arun works
    result = await tool.arun(value="test")
    assert result.result == "async processed test"

@pytest.mark.asyncio
async def test_base_tool_default_arun():
    # Verify that default _arun calls _run
    tool = MockTool()
    result = await tool.arun(value="test")
    assert result.result == "processed test"
