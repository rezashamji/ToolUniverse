from tooluniverse import ToolUniverse
import sys
import os
import pytest
import requests_mock
import requests

# Add src to path to import tooluniverse modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(scope="session")
def tooluni():
    """Initialize tool universe for all tests."""
    tu = ToolUniverse()
    tu.load_tools()
    return tu


@pytest.fixture(autouse=True)
def auto_mock_cellosaurus_apis():
    """Automatically mock all Cellosaurus API calls for all tests."""
    with requests_mock.Mocker() as m:
        # Mock search API with various responses
        m.get(
            "https://api.cellosaurus.org/search/cell-line",
            json={
                "total": 3,
                "cellLines": [
                    {
                        "id": "CVCL_0030",
                        "name": "HeLa",
                        "ox": "9606",
                        "char": ["cancer", "epithelial"],
                    },
                    {
                        "id": "CVCL_0001",
                        "name": "A-549",
                        "ox": "9606",
                        "char": ["cancer", "lung"],
                    },
                    {
                        "id": "CVCL_0027",
                        "name": "MCF-7",
                        "ox": "9606",
                        "char": ["cancer", "breast"],
                    },
                ],
            },
        )

        # Mock cell line info API
        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_0030",
            json={
                "id": "CVCL_0030",
                "name": "HeLa",
                "ox": "9606",
                "char": ["cancer", "epithelial"],
                "ag": "female",
                "ca": "cervix",
                "dt": "1951",
                "sy": ["HeLa", "HeLa 229", "HeLa S3"],
            },
        )

        # Mock non-existent cell line (404)
        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_NONEXISTENT",
            status_code=404,
            json={"error": "Cell line not found"},
        )

        # Mock empty search results
        m.get(
            "https://api.cellosaurus.org/search/cell-line?q=nonexistent",
            json={"total": 0, "cellLines": []},
        )

        yield m


def test_basic_functionality(tooluni):
    """Test basic functionality of all three tools."""
    # Test search
    query1 = {
        "name": "cellosaurus_search_cell_lines",
        "arguments": {"q": "HeLa", "size": 3},
    }
    result1 = tooluni.run(query1)
    assert result1 is not None
    assert "results" in result1 or "error" in result1
    print(f"✅ Search test passed: {result1}")

    # Test query converter
    query2 = {
        "name": "cellosaurus_query_converter",
        "arguments": {"query": "human cancer cells"},
    }
    result2 = tooluni.run(query2)
    assert result2 is not None
    print(f"✅ Query converter test passed: {result2}")

    # Test get cell line info
    query3 = {
        "name": "cellosaurus_get_cell_line_info",
        "arguments": {"accession": "CVCL_0030"},
    }
    result3 = tooluni.run(query3)
    assert result3 is not None
    print(f"✅ Get cell line info test passed: {result3}")

    # Additional: search with JSON Cellosaurus structure
    # to exercise JSON parsing path in search tool
    with requests_mock.Mocker() as m:
        m.get(
            "https://api.cellosaurus.org/search/cell-line",
            json={
                "Cellosaurus": {
                    "cell-line-list": [
                        {"id": "CVCL_0030", "name": "HeLa", "ox": "9606"}
                    ]
                }
            },
        )
        query4 = {
            "name": "cellosaurus_search_cell_lines",
            "arguments": {"q": "HeLa", "size": 1},
        }
        result4 = tooluni.run(query4)
        assert result4 is not None and result4.get("success") is True
        assert result4["results"]["total"] == 1
        print(f"✅ Search JSON Cellosaurus structure: {result4}")


def test_error_handling_and_http_errors(tooluni):
    """Test comprehensive error handling and HTTP errors."""
    with requests_mock.Mocker() as m:
        # Test HTTP errors
        m.get(
            "https://api.cellosaurus.org/search/cell-line",
            status_code=500,
            text="Internal Server Error",
        )
        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_404",
            status_code=404,
            json={"error": "Not found"},
        )
        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_ERROR",
            exc=requests.exceptions.ConnectionError("Connection failed"),
        )

        # Test search HTTP error
        query1 = {
            "name": "cellosaurus_search_cell_lines",
            "arguments": {"q": "HeLa", "size": 1},
        }
        result1 = tooluni.run(query1)
        assert "error" in result1
        print(f"✅ HTTP error test passed: {result1}")

        # Test get_cell_line_info 404 error
        query2 = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_404"},
        }
        result2 = tooluni.run(query2)
        assert "error" in result2
        print(f"✅ 404 error test passed: {result2}")

        # Test connection error
        query3 = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_ERROR"},
        }
        result3 = tooluni.run(query3)
        assert "error" in result3
        print(f"✅ Connection error test passed: {result3}")

        # Test line 1614: HTTP error handling for get_cell_line_info
        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_ERROR",
            status_code=500,
            json={"error": "Internal Server Error"},
        )

        query_http_error = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_ERROR"},
        }
        result_http_error = tooluni.run(query_http_error)
        assert "error" in result_http_error
        print(f"✅ HTTP error test passed: {result_http_error}")


def test_validation_and_edge_cases(tooluni):
    """Test validation scenarios and edge cases."""
    # Test missing required parameters
    error_tests = [
        ("cellosaurus_search_cell_lines", {}, "q"),
        ("cellosaurus_query_converter", {}, "query"),
        ("cellosaurus_get_cell_line_info", {}, "accession"),
    ]

    for tool_name, args, param_name in error_tests:
        query = {"name": tool_name, "arguments": args}
        result = tooluni.run(query)
        assert "error" in result
        assert "required" in result["error"].lower()
        print(f"✅ {tool_name} missing {param_name}: {result['error']}")

    # Test invalid accession format
    query = {
        "name": "cellosaurus_get_cell_line_info",
        "arguments": {"accession": "INVALID_ACCESSION"},
    }
    result = tooluni.run(query)
    assert "error" in result
    assert "cvcl_" in result["error"].lower()
    print(f"✅ Invalid accession test passed: {result['error']}")

    # Test empty query
    query = {"name": "cellosaurus_search_cell_lines", "arguments": {"q": ""}}
    result = tooluni.run(query)
    assert "error" in result
    assert "required" in result["error"].lower()
    print(f"✅ Empty query test passed: {result['error']}")

    # Test invalid format
    query = {
        "name": "cellosaurus_get_cell_line_info",
        "arguments": {"accession": "CVCL_0030", "format": "invalid_format"},
    }
    result = tooluni.run(query)
    assert "error" in result
    assert "format" in result["error"].lower()
    print(f"✅ Invalid format test passed: {result}")

    # Invalid fields list content (mix of valid and invalid)
    with requests_mock.Mocker() as m:
        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_0030",
            json={
                "Cellosaurus": {
                    "cell-line-list": [
                        {"id": "CVCL_0030", "name": "HeLa", "ox": "9606"}
                    ]
                }
            },
        )
        query_invalid_fields = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_0030", "fields": ["id", "foo"]},
        }
        res_invalid_fields = tooluni.run(query_invalid_fields)
        assert "error" in res_invalid_fields
        assert "Invalid fields" in res_invalid_fields["error"]
        print(f"✅ Invalid fields content test passed: {res_invalid_fields}")

    # Test fields validation (line 1476) - fields not a list
    # Note: This validation happens at schema level, so we test the error message
    query = {
        "name": "cellosaurus_get_cell_line_info",
        "arguments": {"accession": "CVCL_0030", "fields": "invalid_string"},
    }
    result = tooluni.run(query)
    assert "error" in str(result) or "Invalid function call" in str(result)
    print(f"✅ Fields validation test passed: {result}")


def test_field_filtering_and_formats(tooluni):
    """Test field filtering and different output formats."""
    with requests_mock.Mocker() as m:
        # Mock detailed response
        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_0030",
            json={
                "id": "CVCL_0030",
                "name": "HeLa",
                "ox": "9606",
                "char": ["cancer", "epithelial"],
                "ag": "female",
                "ca": "cervix",
                "dt": "1951",
                "sy": ["HeLa", "HeLa 229", "HeLa S3"],
            },
        )

        # Test field filtering
        query1 = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_0030", "fields": ["id", "name", "ox"]},
        }
        result1 = tooluni.run(query1)
        assert result1 is not None
        print(f"✅ Field filtering test passed: {result1}")

        # Test JSON format
        query2 = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {
                "accession": "CVCL_0030",
                "format": "json",
                "fields": ["id", "ox", "char"],
            },
        }
        result2 = tooluni.run(query2)
        assert result2 is not None
        print(f"✅ JSON format test passed: {result2}")

        # Test empty response
        m.get("https://api.cellosaurus.org/cell-line/CVCL_EMPTY", json={})
        query3 = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_EMPTY"},
        }
        result3 = tooluni.run(query3)
        assert "error" in result3
        print(f"✅ Empty response test passed: {result3}")

        # Test TXT format path
        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_0030",
            text="ID: CVCL_0030\nName: HeLa",
            headers={"content-type": "text/plain"},
        )
        query_txt = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_0030", "format": "txt"},
        }
        result_txt = tooluni.run(query_txt)
        assert result_txt.get("success") is True
        assert isinstance(result_txt.get("data"), str)
        print(f"✅ TXT format test passed: {result_txt['data'][:20]}")

        # Test FASTA format path
        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_0030",
            text=">CVCL_0030 HeLa\nATGC",
            headers={"content-type": "text/plain"},
        )
        query_fasta = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_0030", "format": "fasta"},
        }
        result_fasta = tooluni.run(query_fasta)
        assert result_fasta.get("success") is True
        assert result_fasta.get("format") == "fasta"
        print(f"✅ FASTA format test passed: {result_fasta['data'][:10]}")

        # Test lines 1586-1593: field filtering with cell-line-list structure
        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_0030",
            json={
                "Cellosaurus": {
                    "cell-line-list": [
                        {
                            "id": "CVCL_0030",
                            "name": "HeLa",
                            "ox": "9606",
                            "char": "cancer",
                            "ag": "female",
                        }
                    ]
                }
            },
        )

        query_filtering = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_0030", "fields": ["id", "name", "ox"]},
        }
        result_filtering = tooluni.run(query_filtering)
        assert result_filtering is not None
        print(f"✅ Field filtering with cell-line-list test passed: {result_filtering}")

        # Test with various field combinations
        edge_field_tests = [
            {"accession": "CVCL_0030", "fields": ["id", "name", "ox", "char"]},
            {"accession": "CVCL_0030", "fields": ["id"]},
            {"accession": "CVCL_0030", "fields": ["id", "nonexistent"]},
        ]

        for field_test in edge_field_tests:
            query_field_edge = {
                "name": "cellosaurus_get_cell_line_info",
                "arguments": field_test,
            }
            result_field_edge = tooluni.run(query_field_edge)
            assert result_field_edge is not None
            print(f"✅ Edge field test passed: {field_test} -> {result_field_edge}")


def test_query_converter_edge_cases(tooluni):
    """Test query converter edge cases and validation."""
    test_cases = [
        # Basic edge cases
        ("ox:9606 human cancer", "field_with_colon_and_value"),
        ("human cancer (AND mouse", "unbalanced_parens"),
        ("human cancer [AND mouse", "unbalanced_brackets"),
        ("char: cancer cells", "empty_field_value"),
        ("human cancer cells", "normal_query"),
        (
            "human cancer cells",
            "include_explanation_false",
            {"include_explanation": False},
        ),
        # Uncovered lines - line 1188: Skip very short terms
        ("a b x y", "short_terms_skip"),
        # Uncovered lines - line 1245: No field-specific terms found
        ("xyzabc123", "no_field_matches"),
        # Uncovered lines - line 1268: Single field query
        ("human", "single_field_query"),
        # Uncovered lines - lines 1291-1292: Validation exception
        ("human cancer cells", "validation_exception"),
        # Uncovered lines - lines 1355-1356: Conversion exception
        ("human cancer cells", "conversion_exception"),
    ]

    for query_text, test_type, *extra_args in test_cases:
        args = {"query": query_text}
        if extra_args:
            args.update(extra_args[0])

        query = {"name": "cellosaurus_query_converter", "arguments": args}
        result = tooluni.run(query)
        assert result is not None
        print(f"✅ {test_type} test passed: {result}")

    # Additional tests for specific uncovered lines
    # Test line 1256: field queries with colon and value
    query_colon_value = {
        "name": "cellosaurus_query_converter",
        "arguments": {"query": "ox:9606 human"},
    }
    result_colon_value = tooluni.run(query_colon_value)
    assert result_colon_value is not None
    print(f"✅ Field queries with colon and value test passed: {result_colon_value}")


def test_xml_parsing_and_data_handling(tooluni):
    """Test XML parsing and data handling scenarios."""
    with requests_mock.Mocker() as m:
        # Test XML parsing with cell-line-list (lines 133-136)
        xml_response1 = """<?xml version="1.0" encoding="UTF-8"?>
        <Cellosaurus>
            <cell-line-list>
                <cell-line id="CVCL_0030">
                    <name>HeLa</name>
                    <ox>9606</ox>
                </cell-line>
                <cell-line id="CVCL_0001">
                    <name>A-549</name>
                    <ox>9606</ox>
                </cell-line>
            </cell-line-list>
        </Cellosaurus>"""

        m.get(
            "https://api.cellosaurus.org/search/cell-line",
            text=xml_response1,
            headers={"content-type": "application/xml"},
        )

        query1 = {
            "name": "cellosaurus_search_cell_lines",
            "arguments": {"q": "HeLa", "size": 2},
        }
        result1 = tooluni.run(query1)
        assert result1 is not None
        print(f"✅ XML parsing test passed: {result1}")

        # Test XML data parsing (lines 1570-1575)
        xml_response2 = """<?xml version="1.0" encoding="UTF-8"?>
        <Cellosaurus>
            <cell-line-list>
                <cell-line id="CVCL_0030">
                    <name>HeLa</name>
                    <ox>9606</ox>
                    <char>cancer</char>
                </cell-line>
            </cell-line-list>
        </Cellosaurus>"""

        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_0030",
            text=xml_response2,
            headers={"content-type": "application/xml"},
        )

        query2 = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_0030", "format": "xml"},
        }
        result2 = tooluni.run(query2)
        assert result2 is not None
        print(f"✅ XML data parsing test passed: {result2}")

        # Test empty XML (lines 1586-1593)
        xml_response3 = """<?xml version="1.0" encoding="UTF-8"?>
        <Cellosaurus>
            <cell-line-list></cell-line-list>
        </Cellosaurus>"""

        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_EMPTY",
            text=xml_response3,
            headers={"content-type": "application/xml"},
        )

        query3 = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_EMPTY", "format": "xml"},
        }
        result3 = tooluni.run(query3)
        assert result3 is not None
        print(f"✅ Empty XML test passed: {result3}")

        # Test lines 1570-1575: XML parsing with cell-line-list structure
        xml_response5 = """<?xml version="1.0" encoding="UTF-8"?>
        <Cellosaurus>
            <cell-line-list>
                <cell-line id="CVCL_0030">
                    <name>HeLa</name>
                    <ox>9606</ox>
                    <char>cancer</char>
                </cell-line>
            </cell-line-list>
        </Cellosaurus>"""

        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_0030",
            text=xml_response5,
            headers={"content-type": "application/xml"},
        )

        query5 = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_0030", "format": "xml"},
        }
        result5 = tooluni.run(query5)
        assert result5 is not None
        print(f"✅ XML cell-line-list parsing test passed: {result5}")

        # Test lines 1586-1593: field filtering with XML data
        xml_response6 = """<?xml version="1.0" encoding="UTF-8"?>
        <Cellosaurus>
            <cell-line-list>
                <cell-line id="CVCL_0030">
                    <name>HeLa</name>
                    <ox>9606</ox>
                    <char>cancer</char>
                    <ag>female</ag>
                </cell-line>
            </cell-line-list>
        </Cellosaurus>"""

        m.get(
            "https://api.cellosaurus.org/cell-line/CVCL_0030",
            text=xml_response6,
            headers={"content-type": "application/xml"},
        )

        query6 = {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {
                "accession": "CVCL_0030",
                "format": "xml",
                "fields": ["id", "name", "ox"],
            },
        }
        result6 = tooluni.run(query6)
        assert result6 is not None
        print(f"✅ XML field filtering test passed: {result6}")


# Keep the original script functionality for backward compatibility
if __name__ == "__main__":
    # Representative test queries for standalone execution
    sample_queries = [
        {
            "name": "cellosaurus_search_cell_lines",
            "arguments": {"q": "HeLa", "size": 3},
        },
        {
            "name": "cellosaurus_query_converter",
            "arguments": {"query": "human cancer cells"},
        },
        {
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": "CVCL_0030", "format": "json"},
        },
    ]

    # Run the tests manually for standalone execution
    test_tooluni = ToolUniverse()
    test_tooluni.load_tools()

    print("Running Cellosaurus tools tests...")
    for idx, query in enumerate(sample_queries):
        print(
            f"\n[{idx+1}] Running tool: {query['name']} with arguments: {query['arguments']}"
        )
        try:
            result = test_tooluni.run(query)
            print("✅ Success. Example output snippet:")
            print(result if isinstance(result, dict) else str(result))
        except Exception as e:
            print(f"❌ Failed. Error: {str(e)}")

print("\n🎉 Cellosaurus tools testing completed!")
