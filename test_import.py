import sys
import os

# Emulate run_app.bat environment
src_path = os.path.join(os.getcwd(), 'src')
sys.path.insert(0, src_path)

print(f"sys.path[0]: {sys.path[0]}")

try:
    import codealign
    print(f"codealign: {codealign.__file__}")
    
    from codealign.authenticity import similarity
    print(f"similarity module: {similarity}")
    
    from codealign.authenticity.similarity import calculate_similarity
    print("Success: calculate_similarity imported.")
except Exception as e:
    print(f"Error: {e}")
except ImportError as e:
    print(f"ImportError: {e}")
