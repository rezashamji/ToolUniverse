#!/usr/bin/env python3
"""
Test cases for all literature search tools.
"""

import pytest
from unittest.mock import patch, Mock
from tooluniverse import ToolUniverse


class TestLiteratureTools:
    """Test cases for all literature search tools."""

    @pytest.fixture
    def tu(self):
        """Initialize ToolUniverse for testing."""
        tu = ToolUniverse()
        tu.load_tools()
        return tu

    def test_arxiv_tool(self, tu):
        """Test ArXiv tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <entry>
                <title>Test Paper Title</title>
                <summary>Test abstract content</summary>
                <author><name>Test Author</name></author>
                <published>2023-01-01T00:00:00Z</published>
                <updated>2023-01-01T00:00:00Z</updated>
                <link type="text/html"
                      href="https://arxiv.org/abs/2301.00001"/>
                <arxiv:primary_category
                    xmlns:arxiv="http://arxiv.org/schemas/atom"
                    term="cs.AI"/>
            </entry>
        </feed>'''

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": "machine learning", "limit": 1}
            })

            assert isinstance(result, list)
            if result:
                paper = result[0]
                assert "title" in paper
                assert "abstract" in paper
                assert "authors" in paper
                assert "published" in paper
                assert "url" in paper

    def test_crossref_tool(self, tu):
        """Test Crossref tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {
                "items": [{
                    "title": ["Test Article Title"],
                    "abstract": "Test abstract",
                    "container-title": ["Test Journal"],
                    "issued": {"date-parts": [[2023]]},
                    "DOI": "10.1000/test.doi",
                    "URL": "https://example.com/article"
                }]
            }
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "Crossref_search_works",
                "arguments": {"query": "test query", "limit": 1}
            })

            assert isinstance(result, list)
            if result:
                article = result[0]
                assert "title" in article
                assert "journal" in article
                assert "year" in article
                assert "doi" in article
                assert "url" in article

    def test_dblp_tool(self, tu):
        """Test DBLP tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "hits": {
                    "hit": [{
                        "info": {
                            "title": "Test Publication",
                            "authors": {"author": ["Test Author"]},
                            "year": "2023",
                            "venue": "Test Conference",
                            "url": "https://dblp.org/test",
                            "ee": "https://example.com/paper"
                        }
                    }]
                }
            }
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "DBLP_search_publications",
                "arguments": {"query": "test query", "limit": 1}
            })

            assert isinstance(result, list)
            if result:
                pub = result[0]
                assert "title" in pub
                assert "authors" in pub
                assert "year" in pub
                assert "venue" in pub
                assert "url" in pub

    def test_pubmed_tool(self, tu):
        """Test PubMed tool functionality."""
        esearch_response = Mock()
        esearch_response.status_code = 200
        esearch_response.json.return_value = {
            "esearchresult": {"idlist": ["12345678"]}
        }

        esummary_response = Mock()
        esummary_response.status_code = 200
        esummary_response.json.return_value = {
            "result": {
                "uids": ["12345678"],
                "12345678": {
                    "title": "Test Article Title",
                    "fulljournalname": "Test Journal",
                    "pubdate": "2023",
                    "articleids": [
                        {"idtype": "doi", "value": "10.1000/test.doi"}
                    ]
                }
            }
        }

        with patch('requests.get', side_effect=[
            esearch_response, esummary_response
        ]):
            result = tu.run({
                "name": "PubMed_search_articles",
                "arguments": {"query": "test query", "limit": 1}
            })

            assert isinstance(result, list)
            if result:
                article = result[0]
                assert "title" in article
                assert "journal" in article
                assert "year" in article
                assert "doi" in article
                assert "url" in article

    def test_doaj_tool(self, tu):
        """Test DOAJ tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "bibjson": {
                    "title": "Test Article",
                    "author": [{"name": "Test Author"}],
                    "year": "2023",
                    "identifier": [{"type": "doi", "id": "10.1000/test.doi"}],
                    "link": [
                        {
                            "type": "fulltext",
                            "url": "https://example.com/article"
                        }
                    ],
                    "journal": {"title": "Test Journal"}
                }
            }]
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "DOAJ_search_articles",
                "arguments": {
                    "query": "test query",
                    "max_results": 1,
                    "type": "articles"
                }
            })

            assert isinstance(result, list)
            if result:
                article = result[0]
                assert "title" in article
                assert "authors" in article
                assert "year" in article
                assert "doi" in article
                assert "venue" in article
                assert "url" in article
                assert "source" in article

    def test_unpaywall_tool(self, tu):
        """Test Unpaywall tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "is_oa": True,
            "oa_status": "gold",
            "best_oa_location": {"url": "https://example.com/oa"},
            "doi": "10.1000/test.doi",
            "title": "Test Article",
            "year": 2023,
            "publisher": "Test Publisher"
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "Unpaywall_check_oa_status",
                "arguments": {
                    "doi": "10.1000/test.doi",
                    "email": "test@example.com"
                }
            })

            assert isinstance(result, dict)
            assert "is_oa" in result
            assert "oa_status" in result
            assert "doi" in result
            assert "title" in result
            assert "year" in result

    def test_biorxiv_tool(self, tu):
        """Test BioRxiv tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "collection": [{
                "title": "Test Preprint",
                "authors": "Author One; Author Two",
                "date": "2023-01-01",
                "doi": "10.1101/2023.01.01.000001",
                "abstract": "Test abstract"
            }]
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "BioRxiv_search_preprints",
                "arguments": {"query": "test query", "max_results": 1}
            })

            assert isinstance(result, list)
            if result:
                preprint = result[0]
                assert "title" in preprint
                assert "authors" in preprint
                assert "year" in preprint
                assert "doi" in preprint
                assert "url" in preprint
                assert "source" in preprint

    def test_medrxiv_tool(self, tu):
        """Test MedRxiv tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "collection": [{
                "title": "Test Medical Preprint",
                "authors": "Medical Author One; Medical Author Two",
                "date": "2023-01-01",
                "doi": "10.1101/2023.01.01.000002",
                "abstract": "Test medical abstract"
            }]
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "MedRxiv_search_preprints",
                "arguments": {"query": "test query", "max_results": 1}
            })

            assert isinstance(result, list)
            if result:
                preprint = result[0]
                assert "title" in preprint
                assert "authors" in preprint
                assert "year" in preprint
                assert "doi" in preprint
                assert "url" in preprint
                assert "source" in preprint

    def test_hal_tool(self, tu):
        """Test HAL tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": {
                "docs": [{
                    "title_s": ["Test HAL Document"],
                    "authFullName_s": ["HAL Author"],
                    "producedDateY_i": 2023,
                    "uri_s": "https://hal.archives-ouvertes.fr/test",
                    "doiId_s": "10.1000/test.hal",
                    "abstract_s": ["Test abstract"],
                    "source_s": "Test Source"
                }]
            }
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "HAL_search_archive",
                "arguments": {"query": "test query", "max_results": 1}
            })

            assert isinstance(result, list)
            if result:
                doc = result[0]
                assert "title" in doc
                assert "authors" in doc
                assert "year" in doc
                assert "url" in doc
                assert "abstract" in doc
                assert "source" in doc

    def test_semantic_scholar_tool(self, tu):
        """Test Semantic Scholar tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{
                "title": "Test Semantic Scholar Paper",
                "abstract": "Test abstract",
                "year": 2023,
                "venue": "Test Conference",
                "url": "https://example.com/paper",
                "authors": [{"name": "Test Author"}]
            }]
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "SemanticScholar_search_papers",
                "arguments": {"query": "test query", "limit": 1}
            })

            assert isinstance(result, list)
            if result:
                paper = result[0]
                assert "title" in paper
                assert "abstract" in paper
                assert "year" in paper
                # Note: venue might be returned as 'journal' in some cases
                assert "venue" in paper or "journal" in paper
                assert "url" in paper

    def test_openalex_tool(self, tu):
        """Test OpenAlex tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "title": "Test OpenAlex Paper",
                "abstract": "Test abstract",
                "publication_year": 2023,
                "primary_location": {
                    "source": {"display_name": "Test Journal"}
                },
                "doi": "10.1000/test.doi",
                "authorships": [{"author": {"display_name": "Test Author"}}]
            }]
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "openalex_literature_search",
                "arguments": {
                    "search_keywords": "test query",
                    "max_results": 1
                }
            })

            assert isinstance(result, list)
            if result:
                paper = result[0]
                assert "title" in paper
                assert "abstract" in paper
                assert "year" in paper
                assert "venue" in paper
                assert "doi" in paper

    def test_europe_pmc_tool(self, tu):
        """Test Europe PMC tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "resultList": {
                "result": [{
                    "id": "PMC12345678",
                    "title": "Test Europe PMC Article",
                    "abstractText": "Test abstract",
                    "pubYear": "2023",
                    "journalTitle": "Test Journal",
                    "pmid": "12345678",
                    "doi": "10.1000/test.doi"
                }]
            }
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "EuropePMC_search_articles",
                "arguments": {"query": "test query", "limit": 1}
            })

            assert isinstance(result, list)
            if result:
                article = result[0]
                assert "title" in article
                assert "abstract" in article
                assert "year" in article
                assert "journal" in article
                assert "url" in article

    def test_error_handling(self, tu):
        """Test error handling in literature tools."""
        with patch('requests.get', side_effect=Exception("Network error")):
            result = tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": "", "limit": 1}
            })

            assert isinstance(result, dict)
            assert "error" in result

    def test_core_tool(self, tu):
        """Test CORE tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Test Paper Title",
                    "abstract": "Test abstract content",
                    "authors": [{"name": "Test Author"}],
                    "publishedDate": "2023-01-01T00:00:00Z",
                    "doi": "10.1000/test",
                    "downloadUrl": "https://core.ac.uk/download/test.pdf",
                    "publisher": "Test Publisher",
                    "language": {"code": "en"},
                    "citationCount": 5,
                    "downloadCount": 100
                }
            ]
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "CORE_search_papers",
                "arguments": {"query": "machine learning", "limit": 1}
            })

            assert isinstance(result, list)
            if result:
                paper = result[0]
                assert "title" in paper
                assert "abstract" in paper
                assert "authors" in paper
                assert "year" in paper
                assert "doi" in paper
                assert "url" in paper
                assert "venue" in paper
                assert "open_access" in paper
                assert "source" in paper
                assert paper["source"] == "CORE"

    def test_pmc_tool(self, tu):
        """Test PMC tool functionality."""
        # Mock search response
        search_response = Mock()
        search_response.status_code = 200
        search_response.json.return_value = {
            "esearchresult": {
                "idlist": ["PMC123456"]
            }
        }

        # Mock summary response
        summary_response = Mock()
        summary_response.status_code = 200
        summary_response.json.return_value = {
            "result": {
                "PMC123456": {
                    "title": "Test Paper Title",
                    "abstract": "Test abstract content",
                    "authors": [{"name": "Test Author"}],
                    "pubdate": "2023-01-01",
                    "pmid": "12345678",
                    "elocationid": "10.1000/test",
                    "source": "Test Journal",
                    "pubtype": ["research-article"],
                    "pmcrefcount": 10
                }
            }
        }

        with patch('requests.get', side_effect=[
            search_response, summary_response
        ]):
            result = tu.run({
                "name": "PMC_search_papers",
                "arguments": {"query": "cancer research", "limit": 1}
            })

            assert isinstance(result, list)
            if result:
                paper = result[0]
                assert "title" in paper
                assert "abstract" in paper
                assert "authors" in paper
                assert "year" in paper
                assert "pmc_id" in paper
                assert "pmid" in paper
                assert "doi" in paper
                assert "url" in paper
                assert "venue" in paper
                assert "open_access" in paper
                assert "source" in paper
                assert paper["source"] == "PMC"

    def test_zenodo_tool(self, tu):
        """Test Zenodo tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "hits": {
                "hits": [
                    {
                        "metadata": {
                            "title": "Test Dataset",
                            "creators": [{"name": "Test Author"}],
                            "publication_date": "2023-01-01",
                            "doi": "10.5281/zenodo.123456"
                        },
                        "links": {
                            "html": "https://zenodo.org/record/123456"
                        },
                        "files": []
                    }
                ]
            }
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "Zenodo_search_records",
                "arguments": {"query": "machine learning", "max_results": 1}
            })

            assert isinstance(result, list)
            if result:
                record = result[0]
                assert "title" in record
                assert "authors" in record
                assert "date" in record
                assert "doi" in record
                assert "url" in record
                assert "source" in record
                assert record["source"] == "Zenodo"

    def test_openaire_tool(self, tu):
        """Test OpenAIRE tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": {
                "results": {
                    "result": [
                        {
                            "metadata": {
                                "oaf:result": {
                                    "title": {
                                        "$": "Test OpenAIRE Publication"
                                    },
                                    "creator": [{"$": "Test Author"}],
                                    "dateofacceptance": {"year": "2023"},
                                    "pid": [
                                        {
                                            "@classid": "doi",
                                            "$": "10.1000/test.doi"
                                        }
                                    ],
                                    "bestaccessright": {
                                        "$": "https://example.com/oa"
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "OpenAIRE_search_publications",
                "arguments": {
                    "query": "test query",
                    "max_results": 1,
                    "type": "publications"
                }
            })

            assert isinstance(result, list)
            if result:
                pub = result[0]
                assert "title" in pub
                assert "authors" in pub
                assert "year" in pub
                assert "doi" in pub
                assert "url" in pub
                assert "type" in pub
                assert "source" in pub
                assert pub["source"] == "OpenAIRE"

    def test_osf_preprints_tool(self, tu):
        """Test OSF Preprints tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{
                "attributes": {
                    "title": "Test OSF Preprint",
                    "date_published": "2023-01-01",
                    "is_published": True,
                    "doi": "10.31219/osf.io/test"
                },
                "links": {
                    "html": "https://osf.io/test"
                }
            }]
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "OSF_search_preprints",
                "arguments": {"query": "test query", "max_results": 1}
            })

            assert isinstance(result, list)
            if result:
                preprint = result[0]
                assert "title" in preprint
                assert "date_published" in preprint
                assert "published" in preprint
                assert "doi" in preprint
                assert "url" in preprint
                assert "source" in preprint
                assert preprint["source"] == "OSF Preprints"

    def test_fatcat_tool(self, tu):
        """Test Fatcat tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "hits": {
                "hits": [{
                    "_source": {
                        "title": "Test Fatcat Paper",
                        "release_year": 2023,
                        "doi": "10.1000/test.doi",
                        "contrib_names": ["Test Author"],
                        "wikidata_qid": "Q123456"
                    }
                }]
            }
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "Fatcat_search_scholar",
                "arguments": {"query": "test query", "max_results": 1}
            })

            assert isinstance(result, list)
            if result:
                paper = result[0]
                assert "title" in paper
                assert "authors" in paper
                assert "year" in paper
                assert "doi" in paper
                assert "url" in paper
                assert "source" in paper
                assert paper["source"] == "Fatcat/IA Scholar"

    def test_wikidata_sparql_tool(self, tu):
        """Test Wikidata SPARQL tool functionality."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": {
                "bindings": [
                    {
                        "item": {
                            "value": "http://www.wikidata.org/entity/Q11424"
                        },
                        "itemLabel": {"value": "Test Item"}
                    }
                ]
            }
        }

        with patch('requests.get', return_value=mock_response):
            result = tu.run({
                "name": "Wikidata_SPARQL_query",
                "arguments": {
                    "sparql": (
                        "SELECT ?item ?itemLabel WHERE { "
                        "?item wdt:P31 wd:Q11424 . "
                        "?item rdfs:label ?itemLabel . "
                        "FILTER(LANG(?itemLabel) = 'en') } LIMIT 1"
                    )
                }
            })

            assert isinstance(result, list)
            if result:
                binding = result[0]
                assert "item" in binding
                assert "itemLabel" in binding

    def test_parameter_validation(self, tu):
        """Test parameter validation for literature tools."""
        # Test missing required parameters
        result = tu.run({"name": "ArXiv_search_papers", "arguments": {}})
        assert isinstance(result, dict)
        assert "error" in result

        # Test missing email for Unpaywall
        result = tu.run({
            "name": "Unpaywall_check_oa_status",
            "arguments": {"doi": "10.1000/test.doi"}
        })
        assert isinstance(result, dict)
        assert "error" in result

        # Test missing sparql for Wikidata
        result = tu.run({
            "name": "Wikidata_SPARQL_query",
            "arguments": {}
        })
        assert isinstance(result, dict)
        assert "error" in result


if __name__ == "__main__":
    pytest.main([__file__])
