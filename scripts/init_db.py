import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import init_db

if __name__ == "__main__":
    init_db()
    print("Database initialized with sample data.")