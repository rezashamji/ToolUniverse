Tutorial Navigation
===================

Learn how to extend ToolUniverse with your own custom tools. This section provides comprehensive guides for creating, registering, and contributing tools to the ToolUniverse ecosystem.

Overview
--------

ToolUniverse is designed to be extensible, allowing you to add custom tools for your specific research needs. Whether you want to integrate with external APIs, create specialized analysis tools, or contribute to the community, this section has you covered.

**What You'll Learn:**

- 🏠 **Local Tool Development**: Create tools that run within ToolUniverse
- 🔗 **Remote Tool Integration**: Connect with external services and APIs
- 📤 **Community Contributions**: Submit your tools to the ToolUniverse repository
- 🔧 **Advanced Patterns**: Best practices and advanced development techniques

Quick Start
-----------

Choose your path based on your needs:

**I want to create a tool for my own use:**
→ Start with :doc:`local_tool_registration` for simple, fast tools

**I want to integrate with external services:**
→ Start with :doc:`remote_tool_registration` for API integrations

**I want to learn advanced tool features:**
→ Start with :doc:`advanced_tool_development` for BaseTool capabilities and advanced patterns

**I want to contribute to the community:**
→ Start with :doc:`comprehensive_tool_guide` for the complete step-by-step contribution process

Guides
------

Local Tool Registration and Usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`local_tool_registration`

Learn how to create, register, and use custom tools locally within ToolUniverse. This Tutorial covers everything from basic tool creation to advanced patterns and best practices.

**Key Topics:**
- Quick start with decorator registration
- Step-by-step tool creation
- Common tool patterns (API wrappers, file processors, database tools)
- Advanced features (caching, rate limiting, error handling)
- Testing and troubleshooting

Remote Tool Registration and Usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`remote_tool_registration`

Learn how to integrate external services, APIs, and tools running on different servers with ToolUniverse. This Tutorial covers MCP integration, REST API wrappers, and advanced remote tool patterns.

**Key Topics:**
- MCP (Model Context Protocol) integration
- REST API wrapper creation
- Specialized API wrappers (OpenAI, Weather, Database)
- Microservice integration patterns
- Authentication and security
- Performance optimization

Advanced Tool Development
~~~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`advanced_tool_development`

Learn how to leverage the full power of BaseTool capabilities for advanced tool development. This guide covers custom validation, error handling, caching, and other advanced features.

**Key Topics:**
- Enhanced BaseTool capabilities
- Custom parameter validation
- Advanced error handling patterns
- Custom caching strategies
- Capability declaration
- Migration from basic tools
- Best practices and testing

Contributing Tools to ToolUniverse - Complete Tutorial
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:doc:`comprehensive_tool_guide`

A comprehensive, step-by-step Tutorial that combines tool reference documentation with detailed contribution instructions. This Tutorial covers everything from understanding existing tools to creating, testing, and submitting your own tools with detailed code examples and best practices.

**Key Topics:**
- Understanding ToolUniverse tool structure and categories
- Complete development environment setup
- Step-by-step tool implementation with templates
- Comprehensive testing strategies and examples
- Code quality standards and documentation requirements
- Pull request submission and review process
- Advanced topics including performance optimization and security

:doc:`contributing_tools`

Quick reference for submitting tools to the ToolUniverse repository (legacy Tutorial - use comprehensive_tool_guide for detailed instructions).

**Key Topics:**
- Basic contribution process
- Testing and documentation requirements
- Pull request submission overview

Tool Types
----------

Local Tools
~~~~~~~~~~~

Local tools are Python classes that run within the same process as ToolUniverse. They provide:

- **High Performance**: No network overhead
- **Easy Development**: Simple Python classes
- **Automatic Discovery**: Tools auto-register with decorators
- **Full Integration**: Access to all ToolUniverse features

**Best for:**
- Data processing and analysis
- File manipulation utilities
- Simple API wrappers
- Computational tools

Remote Tools
~~~~~~~~~~~~

Remote tools allow you to integrate external services, APIs, or tools running on different servers. They provide:

- **Scalability**: Offload heavy computation to dedicated servers
- **Integration**: Connect with existing systems and services
- **Flexibility**: Use tools in different programming languages
- **Isolation**: Keep sensitive operations separate

**Best for:**
- External API integrations
- Microservice connections
- Cloud-based AI services
- Proprietary system connections

Development Workflow
--------------------

1. **Plan Your Tool**
   - Define functionality and requirements
   - Choose between local or remote implementation
   - Design API and parameter structure

2. **Develop Your Tool**
   - Implement core functionality
   - Add proper error handling
   - Write comprehensive tests

3. **Document Your Tool**
   - Create clear documentation
   - Provide usage examples
   - Document all parameters and outputs

4. **Test Thoroughly**
   - Unit tests for all functionality
   - Integration tests with ToolUniverse
   - Test edge cases and error conditions

5. **Submit for Review**
   - Follow contribution guidelines
   - Create pull request
   - Address review feedback

Best Practices
--------------

Code Quality
~~~~~~~~~~~~

- Follow PEP 8 style guidelines
- Use type hints for better code clarity
- Write comprehensive docstrings
- Implement proper error handling
- Use meaningful variable names

Testing
~~~~~~~

- Write unit tests for all functionality
- Test edge cases and error conditions
- Include integration tests
- Maintain high test coverage
- Test with real-world data

Documentation
~~~~~~~~~~~~~

- Write clear, comprehensive documentation
- Include usage examples
- Document all parameters and return values
- Provide troubleshooting guides
- Keep documentation up-to-date

Security
~~~~~~~~

- Validate all inputs thoroughly
- Use secure coding practices
- Handle sensitive data appropriately
- Implement proper authentication for remote tools
- Follow security best practices

Examples
--------

Simple Local Tool
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from tooluniverse.tool_registry import register_tool

   @register_tool('SimpleCalculator', config={
       "name": "simple_calculator",
       "type": "SimpleCalculator",
       "description": "Basic mathematical calculations",
       "parameter": {
           "type": "object",
           "properties": {
               "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
               "a": {"type": "number"},
               "b": {"type": "number"}
           },
           "required": ["operation", "a", "b"]
       }
   })
   class SimpleCalculator:
       def run(self, arguments):
           operation = arguments["operation"]
           a = arguments["a"]
           b = arguments["b"]

           if operation == "add":
               result = a + b
           elif operation == "subtract":
               result = a - b
           elif operation == "multiply":
               result = a * b
           elif operation == "divide":
               if b == 0:
                   return {"error": "Division by zero", "success": False}
               result = a / b

           return {"result": result, "success": True}

API Integration Tool
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   @register_tool('APITool', config={
       "name": "api_wrapper",
       "type": "APITool",
       "description": "Wrapper for external API calls",
       "parameter": {
           "type": "object",
           "properties": {
               "url": {"type": "string", "description": "API endpoint URL"},
               "method": {"type": "string", "enum": ["GET", "POST"], "default": "GET"},
               "data": {"type": "object", "description": "Request data"}
           },
           "required": ["url"]
       }
   })
   class APITool:
       def run(self, arguments):
           try:
               import requests

               url = arguments["url"]
               method = arguments.get("method", "GET")
               data = arguments.get("data", {})

               if method == "GET":
                   response = requests.get(url)
               else:
                   response = requests.post(url, json=data)

               response.raise_for_status()
               return {"data": response.json(), "success": True}

           except Exception as e:
               return {"error": str(e), "success": False}

Getting Help
------------

If you need help with tool development:

- **Documentation**: Check the specific guides for detailed information
- **Examples**: Look at existing tools in the codebase
- **Community**: Ask questions in GitHub discussions
- **Issues**: Report bugs or request features

Resources
---------

- **ToolUniverse Repository**: https://github.com/original/ToolUniverse
- **Issue Tracker**: https://github.com/original/ToolUniverse/issues
- **Discussions**: https://github.com/original/ToolUniverse/discussions
- **Documentation**: https://tooluniverse.readthedocs.io

Next Steps
----------

Ready to start? Choose your path:

* 🏠 **Local Tools**: :doc:`local_tool_registration` - Start with local tool development
* 🔗 **Remote Tools**: :doc:`remote_tool_registration` - Learn about remote integrations
* 🔧 **Advanced Features**: :doc:`advanced_tool_development` - Learn BaseTool capabilities and advanced patterns
* 📤 **Contributing**: :doc:`comprehensive_tool_guide` - Complete step-by-step Tutorial for contributing tools to the community

.. tip::
   **Getting Started**: We recommend starting with a simple local tool to understand the process, then moving to more complex integrations. The community is here to help you succeed!
