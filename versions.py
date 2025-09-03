import importlib.metadata
packages =[
    "langchain",
    "python-dotenv",
    "ipykernel",
    "langchain_groq",
    "langchain_openai",
    "langchain_google_genai",
    "langchain_community",
    "pypdf",
    "faiss-cpu",
    "pymupdf",
    "structlog",
    "pandas",
    "streamlit",
    "pytest",
    "langchain-core",
    "docx2txt"
]
for pkg in packages:
    try:
        version = importlib.metadata.version(pkg)
        print(f"{pkg}=={version}")
    except importlib.metadata.PackageNotFoundError:
        print(f"{pkg} (not installed)")