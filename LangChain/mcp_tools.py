from langchain_mcp_adapters.client import MultiServerMCPClient

# client=MultiServerMCPClient(
#     {
#         "time_server":{
#             "transport":"http",
#             "url":"https://dlptest.com/api/mcp/"
#             # "args":
#             #         {
#             #            "github.com/weather-mcp/weather-mcp"
#             #         }        
#     }
#     }
# )

client=MultiServerMCPClient(
    {
        "time_server":{
            "transport":"stdio",
            "command":"python",
            "args":[
                "mcp_server.py"
            ]
        }
    }
)