import:py from openai { OpenAI };
import:py from dotenv { load_dotenv };
import:py import os;

load_dotenv();

walker DocGenie {
    has code_content: str;
    has api_key: str = os.getenv("OPENAI_API_KEY");
    has documentation: str = "";

    can generate_docs with entry {
        print("Generating documentation with AI...");
        self.documentation = f"Documentation for code:\n{self.code_content}";
        print(self.documentation);
    };
};
