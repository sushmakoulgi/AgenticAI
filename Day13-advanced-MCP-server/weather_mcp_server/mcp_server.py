from fastmcp import FastMCP


mcp=FastMCP("Weather Server")

@mcp.tool()
def get_weather(city:str):
    """ 
    return the weather of the given city"""
    weather_data={
        "Boston":"63F",
        "Newyork":"58F"
    }

    return weather_data.get(city,"Weather not available")

@mcp.resource(uri="weather:\\cities")
def available_cities():
    """
    provides the list of cities for which weather is available"""
    return """ available cities are Boston and Newyork"""

if __name__=="__main__":
    print("starting Weather MCP server")
    # mcp.run(
    #     transport="http",
    #     show_banner=True,
    #     host="127.0.0.1",
    #     port=8001
    # )
    mcp.run()