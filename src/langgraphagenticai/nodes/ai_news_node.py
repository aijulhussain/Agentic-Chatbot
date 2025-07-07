from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplat


class AINewsNode:
    def __init__(self, llm):
        """
        Initialize the AINewsNode with API keys for Tavily and Groq.
        """
        self.tavily=TavilyClient()
        self.llm = llm
        self.state={}
    

    
    def fetch_news(self, state:dict)->dict:
        """
        Fetch AI news based on the specified frequency.
        Args:
            State (dict): The state dictionay containing 'frequency'.
            
        Returns:
            dict: Updated state with 'news_data' key containing fetched news.
        
        """
        frequency = state['message'][0].content.lower()
        self.state['frequency']=frequency
        time_range_map={'daily':'d', 'weekly':'w', 'monthly':'m', 'year':'y'}
        days_map={'daily':1, 'weekly':7, 'monthly':30, 'year':365} 

        response = self.tavily.search(
            qurey = "Top Artificial Intelligence (AI) technology news India and Globally",
            topic = "news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency]
        )


        state['news_data']=response.get('results', [])
        self.state['news_data']=state['news_data']
        return state