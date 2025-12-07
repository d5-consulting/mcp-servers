import tempfile
from pathlib import Path

import pytest
from fastmcp import Client

from xlsx.tools import mcp


@pytest.mark.asyncio
async def test_create_excel():
    async with Client(mcp) as client:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = str(Path(tmpdir) / "test.xlsx")
            data = "Name,Value\\nItem1,100\\nItem2,200"

            res = await client.call_tool("create_excel", {"file_path": file_path, "data": data, "sheet_name": "Data"})
            assert "Created" in res.content[0].text
            assert Path(file_path).exists()


@pytest.mark.asyncio
async def test_read_excel():
    async with Client(mcp) as client:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = str(Path(tmpdir) / "test.xlsx")
            data = "Name,Value\\nItem1,100\\nItem2,200"

            await client.call_tool("create_excel", {"file_path": file_path, "data": data})
            res = await client.call_tool("read_excel", {"file_path": file_path})
            assert "Name" in res.content[0].text
            assert "Item1" in res.content[0].text


@pytest.mark.asyncio
async def test_get_sheet_names():
    async with Client(mcp) as client:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = str(Path(tmpdir) / "test.xlsx")
            data = "Name,Value\\nItem1,100"

            await client.call_tool("create_excel", {"file_path": file_path, "data": data, "sheet_name": "TestSheet"})
            res = await client.call_tool("get_sheet_names", {"file_path": file_path})
            assert "TestSheet" in res.content[0].text


@pytest.mark.asyncio
async def test_write_cell():
    async with Client(mcp) as client:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = str(Path(tmpdir) / "test.xlsx")
            data = "Name,Value\\nItem1,100"

            await client.call_tool("create_excel", {"file_path": file_path, "data": data, "sheet_name": "Sheet1"})
            res = await client.call_tool(
                "write_cell", {"file_path": file_path, "sheet_name": "Sheet1", "cell": "C1", "value": "=A1+B1"}
            )
            assert "Wrote" in res.content[0].text


@pytest.mark.asyncio
async def test_add_sheet():
    async with Client(mcp) as client:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = str(Path(tmpdir) / "test.xlsx")
            data = "Name,Value\\nItem1,100"

            await client.call_tool("create_excel", {"file_path": file_path, "data": data})
            res = await client.call_tool("add_sheet", {"file_path": file_path, "sheet_name": "NewSheet"})
            assert "Added" in res.content[0].text


@pytest.mark.asyncio
async def test_convert_to_csv():
    async with Client(mcp) as client:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = str(Path(tmpdir) / "test.xlsx")
            csv_path = str(Path(tmpdir) / "test.csv")
            data = "Name,Value\\nItem1,100"

            await client.call_tool("create_excel", {"file_path": file_path, "data": data})
            res = await client.call_tool("convert_to_csv", {"file_path": file_path, "output_file": csv_path})
            assert "Converted" in res.content[0].text
            assert Path(csv_path).exists()
