from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from com.mhire.app.config.config import Config

class MotivationService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MotivationService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize LangChain components"""
        config = Config()
        
        # Initialize Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=config.GEMINI_API_KEY,
            temperature=0.9,  # Higher temperature for more creative responses
        )
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a motivational coach for a habit tracking app. 
Your job is to generate short, powerful motivational quotes to help people build good habits and break bad ones.

Rules:
- Generate ONLY 1-2 sentences with a maximum of 110 characters
- Focus on wellness, personal growth, and positive change
- Be encouraging and actionable
- Vary your messages to keep them fresh
- Do not use quotation marks
- Keep it concise and impactful"""),
            ("user", "Generate a motivational quote for someone working on their habits today.")
        ])
        
        # Create output parser
        self.output_parser = StrOutputParser()
        
        # Create the chain
        self.chain = self.prompt | self.llm | self.output_parser
    
    async def generate_motivation(self) -> str:
        """Generate a motivational quote"""
        try:
            motivation = await self.chain.ainvoke({})
            # Clean up the response (remove any quotes if present)
            motivation = motivation.strip().strip('"').strip("'")
            return motivation
        except Exception as e:
            # Fallback motivation in case of error
            return "Every small step forward is progress. Keep building your better self today."

# Create singleton instance
motivation_service = MotivationService()