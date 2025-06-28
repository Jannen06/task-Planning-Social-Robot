import numpy as np
import random
from typing import Dict, List, Tuple, Set

'''Written using Claude'''

def generate_dishes_and_preferences(grid: np.ndarray, rooms: Dict, people_positions: List[Tuple[int, int]], 
                                  occupied_positions: Set[Tuple[int, int]]) -> Tuple[np.ndarray, Dict[int, str], List[Tuple[int, int, str]]]:
    """
    Generate vegan and non-vegetarian dishes scattered in the kitchen and assign dietary preferences to people.
    
    Args:
        grid: The house layout grid
        rooms: Dictionary containing room slice information
        people_positions: List of (row, col) positions where people are located
        occupied_positions: Set of positions that are already occupied
    
    Returns:
        Tuple containing:
        - Updated grid with dishes placed
        - Dictionary mapping person number to dietary preference
        - List of dish positions with their types [(row, col, dish_type), ...]
    """
    
    # Get kitchen area
    kitchen_slice = rooms['K']
    kitchen_rows, kitchen_cols = kitchen_slice
    
    # Number of people (dishes needed)
    num_people = len(people_positions)
    
    # Generate dietary preferences for each person
    # Ensure we have a good mix of vegan and non-vegetarian preferences
    preferences = ['vegan', 'non-vegetarian']
    person_preferences = {}
    
    # Randomly assign preferences with some balance
    for i in range(num_people):
        person_num = i + 1
        # Create a balanced distribution
        if i < num_people // 2:
            person_preferences[person_num] = random.choice(preferences)
        else:
            # Ensure we have at least some of each type
            remaining_vegan = sum(1 for p in person_preferences.values() if p == 'vegan')
            remaining_non_veg = sum(1 for p in person_preferences.values() if p == 'non-vegetarian')
            
            if remaining_vegan == 0:
                person_preferences[person_num] = 'vegan'
            elif remaining_non_veg == 0:
                person_preferences[person_num] = 'non-vegetarian'
            else:
                person_preferences[person_num] = random.choice(preferences)
    
    # Find valid positions in kitchen for dishes
    valid_kitchen_positions = []
    for row in range(kitchen_rows.start, kitchen_rows.stop):
        for col in range(kitchen_cols.start, kitchen_cols.stop):
            # Check if position is valid (not wall, door, furniture, or person)
            if ((row, col) not in occupied_positions and 
                grid[row, col] not in ['W', 'd', 'k', 'F'] and  # Not wall, door, counter, or fridge
                grid[row, col] == 'K'):  # Must be in kitchen space
                valid_kitchen_positions.append((row, col))
    
    # Check if we have enough space for all dishes
    if len(valid_kitchen_positions) < num_people:
        print(f"Warning: Only {len(valid_kitchen_positions)} valid positions found in kitchen for {num_people} dishes")
        print("Some dishes may not be placed or may overlap")
    
    # Place dishes in kitchen
    dish_positions = []
    grid_copy = grid.copy()
    
    # Shuffle positions to randomize placement
    random.shuffle(valid_kitchen_positions)
    
    # Create dishes based on preferences
    vegan_count = sum(1 for p in person_preferences.values() if p == 'vegan')
    non_veg_count = sum(1 for p in person_preferences.values() if p == 'non-vegetarian')
    
    dishes_to_place = (['V'] * vegan_count) + (['N'] * non_veg_count)
    random.shuffle(dishes_to_place)
    
    # Place dishes
    for i, dish_type in enumerate(dishes_to_place):
        if i < len(valid_kitchen_positions):
            row, col = valid_kitchen_positions[i]
            grid_copy[row, col] = dish_type
            dish_type_name = 'vegan' if dish_type == 'V' else 'non-vegetarian'
            dish_positions.append((row, col, dish_type_name))
        else:
            print(f"Could not place dish {i+1} - no more valid positions")
    
    return grid_copy, person_preferences, dish_positions

def get_person_dietary_preference(person_number: int, person_preferences: Dict[int, str]) -> str:
    """
    Get the dietary preference for a specific person.
    
    Args:
        person_number: The person's number (1-8)
        person_preferences: Dictionary mapping person numbers to preferences
    
    Returns:
        String indicating dietary preference ('vegan' or 'non-vegetarian')
    """
    return person_preferences.get(person_number, 'unknown')

def find_dishes_by_type(dish_positions: List[Tuple[int, int, str]], dish_type: str) -> List[Tuple[int, int]]:
    """
    Find all dishes of a specific type.
    
    Args:
        dish_positions: List of dish positions with types
        dish_type: Type of dish to find ('vegan' or 'non-vegetarian')
    
    Returns:
        List of (row, col) positions for dishes of the specified type
    """
    return [(row, col) for row, col, dtype in dish_positions if dtype == dish_type]

def get_dish_assignment_summary(person_preferences: Dict[int, str], dish_positions: List[Tuple[int, int, str]]) -> Dict:
    """
    Get a summary of dish assignments and preferences.
    
    Args:
        person_preferences: Dictionary mapping person numbers to preferences
        dish_positions: List of dish positions with types
    
    Returns:
        Dictionary containing summary information
    """
    vegan_people = [p for p, pref in person_preferences.items() if pref == 'vegan']
    non_veg_people = [p for p, pref in person_preferences.items() if pref == 'non-vegetarian']
    
    vegan_dishes = find_dishes_by_type(dish_positions, 'vegan')
    non_veg_dishes = find_dishes_by_type(dish_positions, 'non-vegetarian')
    
    return {
        'total_people': len(person_preferences),
        'vegan_people': vegan_people,
        'non_vegetarian_people': non_veg_people,
        'vegan_people_count': len(vegan_people),
        'non_vegetarian_people_count': len(non_veg_people),
        'vegan_dishes_positions': vegan_dishes,
        'non_vegetarian_dishes_positions': non_veg_dishes,
        'vegan_dishes_count': len(vegan_dishes),
        'non_vegetarian_dishes_count': len(non_veg_dishes)
    }

def visualize_dishes_and_preferences(grid: np.ndarray, person_preferences: Dict[int, str], 
                                   dish_positions: List[Tuple[int, int, str]], people_positions: List[Tuple[int, int]]):
    """
    Print a summary of the dish and preference assignments.
    
    Args:
        grid: Updated grid with dishes
        person_preferences: Dictionary mapping person numbers to preferences
        dish_positions: List of dish positions with types
        people_positions: List of people positions
    """
    print("\n" + "="*60)
    print("DISH GENERATION AND DIETARY PREFERENCES SUMMARY")
    print("="*60)
    
    summary = get_dish_assignment_summary(person_preferences, dish_positions)
    
    print(f"\nTotal People: {summary['total_people']}")
    print(f"Vegan People: {summary['vegan_people_count']} - {summary['vegan_people']}")
    print(f"Non-Vegetarian People: {summary['non_vegetarian_people_count']} - {summary['non_vegetarian_people']}")
    
    
    print(f"\nPerson-Preference Mapping:")
    for (person_num, preference), (row, col, dish_type) in zip(person_preferences.items(), dish_positions):
        person_pos = people_positions[person_num - 1] if person_num <= len(people_positions) else "Unknown"
        print(f"Person {person_num} at {person_pos}: dietary {preference} at ({row}, {col})")
    

