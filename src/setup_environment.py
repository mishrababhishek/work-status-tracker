from dotenv import load_dotenv;

def setup_env():
    print(
        '''
        Setting up environment variables...
        '''
    )
    load_dotenv()