# data.py
import json
from pathlib import Path
from typing import Optional, List, Dict

def load_real_shot_data() -> Optional[Dict]:
    """Load real shot data from HoopIQ system"""
    filepath = Path('/tmp/hoopiq_shot_data.json')
    
    if not filepath.exists():
        print("⚠️ HoopIQ data not found. Is the detection system running?")
        return None
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading HoopIQ data: {e}")
        return None

def get_shot_results() -> List[Dict]:
    """Get shot results in Streamlit format"""
    data = load_real_shot_data()
    
    if not data or 'shots' not in data:
        # Return placeholder data if no real data available
        return get_placeholder_data()
    
    # Convert HoopIQ format to Streamlit format
    results = []
    for shot in data['shots']:
        results.append({
            'Shot': shot['shot_id'],
            'Backboard': shot.get('backboard', True),
            'Rim': shot.get('rim', True),
            'Net': shot.get('net', True),
            'Game Make': shot.get('make', True),
            'trajectory_x': shot['trajectory']['x'],
            'trajectory_y': shot['trajectory']['y'],
            'trajectory_z': shot['trajectory']['z'],
        })
    
    return results

def get_placeholder_data():
    """Placeholder data when real system is not running"""
    # Your existing placeholder data
    pass
