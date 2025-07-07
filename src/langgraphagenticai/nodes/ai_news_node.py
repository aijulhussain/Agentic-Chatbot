from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


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
    

    def summarize_news(self, state:dict)->dict:
        """
        Summarize the fetched news using an LLM.
        
        Args:
            State (dict): The state dictionary containing 'news_data'.
        
        Returns:
            dict: Updated state with 'summary' key containing the summarized news.
        
        """
        news_item = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are an assistant that summarizes AI news articles in markdown format. For each article:
        - Use the date in **YYYY-MM-DD** format (IST timezone)
        - Provide a concise summary in clear sentences
        - Sort the articles by date (latest first)
        - Include the source URL as a hyperlink

        Format:
        ### [YYYY-MM-DD]
        - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_item:
            
        ])
        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary']=response.content
        self.state['summary']=state['summary']
        return self.state