import random
import json
import ast
import re

# Simple rhyme detection without external dependencies
def simple_rhyme_check(word1, word2):
    """Basic rhyme detection based on word endings"""
    if len(word1) < 2 or len(word2) < 2:
        return False
    # Check if words end with similar sounds (simple heuristic)
    endings = [
        ('ing', 'ing'), ('ed', 'ed'), ('ly', 'ly'), ('er', 'er'), ('est', 'est'),
        ('tion', 'tion'), ('ness', 'ness'), ('ment', 'ment'), ('able', 'able'),
        ('ight', 'ight'), ('ought', 'ought'), ('ay', 'ay'), ('ey', 'ey'),
        ('ow', 'ow'), ('ew', 'ew'), ('oo', 'oo'), ('ee', 'ee'), ('ea', 'ea'),
        ('ie', 'ie'), ('ue', 'ue'), ('ar', 'ar'), ('or', 'or'), ('ur', 'ur')
    ]
    
    word1_lower = word1.lower()
    word2_lower = word2.lower()
    
    for end1, end2 in endings:
        if word1_lower.endswith(end1) and word2_lower.endswith(end2):
            return True
    
    # Check for same last 2-3 characters
    if len(word1) >= 3 and len(word2) >= 3:
        if word1_lower[-3:] == word2_lower[-3:]:
            return True
    if len(word1) >= 2 and len(word2) >= 2:
        if word1_lower[-2:] == word2_lower[-2:]:
            return True
    
    return False

def estimate_syllables(word):
    """Simple syllable counting heuristic"""
    word = word.lower()
    vowels = 'aeiouy'
    count = 0
    prev_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel
    
    # Handle silent 'e'
    if word.endswith('e') and count > 1:
        count -= 1
    
    return max(1, count)  # Every word has at least 1 syllable

# 🌈 Mood Lexicon
mood_lexicon = {
    "joyful": {"breeze", "laugh", "sun", "play", "blueberries", "cherries", "sing", "apples", "Little Ocean", "bananas", "free", "friends", "friend"},
    "melancholy": {"sad", "alone", "drift", "memory", "quiet", "soft", "shadow", "miss", "Ocean"},
    "mysterious": {"deep", "whisper", "dark", "Python", "fog", "the creatures", "secret", "the seeds", "lost seeds"}
}

next_word_map = {}  # 2-gram and 4-gram map
feedback_map = {}   # track feedback per transition
favorite_starts = []
last_input = ""

non_starter_words = {"and", "but", "to", "or", "so", "for", "nor", "yet", "as", "because", "while", "if", "the", "a", "an"}

# === Helper functions ===

def get_valid_random_start():
    valid_favorites = [s for s in favorite_starts if s in next_word_map]
    if valid_favorites and random.random() < 0.7:
        return random.choice(valid_favorites)
    valid_starts = [k for k in next_word_map if k[0] not in non_starter_words and k[1] not in non_starter_words]
    if not valid_starts and next_word_map:
        return random.choice(list(next_word_map.keys()))
    if valid_starts:
        return random.choice(valid_starts)
    return None

def weighted_choice(word_weights, mood=None):
    if not word_weights:
        return None
    if mood and mood in mood_lexicon:
        mood_words = mood_lexicon[mood]
        weighted = {w: weight*2 if w in mood_words else weight for w, weight in word_weights.items()}
        word_weights = weighted
    total = sum(word_weights.values())
    if total == 0:
        return None
    rand_val = random.randint(1, total)
    cum = 0
    for word, weight in word_weights.items():
        cum += weight
        if rand_val <= cum:
            return word

def update_weights_from_sentence(sentence):
    global last_input
    last_input = sentence
    words = sentence.lower().strip().split()
    if len(words) < 2:
        return
    # 2-grams and 4-grams
    for i in range(len(words)-1):
        if i < len(words) - 1:  # 2-gram
            key = tuple(words[i:i+2])
            if i + 2 < len(words):
                next_word = words[i+2]
                next_word_map.setdefault(key, {})
                next_word_map[key].setdefault(next_word, 0)
                next_word_map[key][next_word] += 1
                # feedback tracking
                feedback_map.setdefault(key, {})
                feedback_map[key].setdefault(next_word, {"positive": 0, "negative": 0})
    
    # 4-grams
    if len(words) >= 4:
        for i in range(len(words)-3):
            key4 = tuple(words[i:i+4])
            if i + 4 < len(words):
                next_word4 = words[i+4]
                next_word_map.setdefault(key4, {})
                next_word_map[key4].setdefault(next_word4, 0)
                next_word_map[key4][next_word4] += 1
                feedback_map.setdefault(key4, {})
                feedback_map[key4].setdefault(next_word4, {"positive": 0, "negative": 0})

def get_user_start():
    print("💡 Enter two words to start (or leave blank for random): ")
    user_input = input("> ").strip().lower()
    if user_input:
        words = user_input.split()
        if len(words) >= 2:
            return tuple(words[:2])
        print("Please enter at least two words.")
        return get_user_start()
    
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        start = get_valid_random_start()
        if not start:
            print("🌊 No valid starting pairs found! Teach me some sentences first.")
            return None
        print(f"Random start chosen: {start[0]} {start[1]}")
        like = input("Do you like this start? (y/n): ").strip().lower()
        if like == "y":
            if start not in favorite_starts:
                favorite_starts.append(start)
                print(f"💙 Added {start} to favorite_starts!")
            return start
        else:
            print("Okay, picking another random start...")
            attempts += 1
    print("🌊 Too many tries! Please give a starting phrase next time.")
    return None

def undo_last_input():
    global last_input
    if not last_input:
        print("🚫 No input to undo.")
        return
    print(f"🚫 Undoing last input: {last_input}")
    words = last_input.lower().strip().split()
    if len(words) < 3:  # Need at least 3 words for a 2-gram transition
        print("🙅‍♀️ Can't undo, not enough data.")
        return
    
    # Remove 2-grams
    for i in range(len(words)-2):
        key = tuple(words[i:i+2])
        next_word = words[i+2]
        if key in next_word_map and next_word in next_word_map[key]:
            next_word_map[key][next_word] -= 1
            if next_word_map[key][next_word] <= 0:
                del next_word_map[key][next_word]
            if not next_word_map[key]:
                del next_word_map[key]
            print(f"💨 Removed: {key} ➡️ {next_word}")
    
    # Remove 4-grams
    if len(words) >= 5:
        for i in range(len(words)-4):
            key4 = tuple(words[i:i+4])
            next_word4 = words[i+4]
            if key4 in next_word_map and next_word4 in next_word_map[key4]:
                next_word_map[key4][next_word4] -= 1
                if next_word_map[key4][next_word4] <= 0:
                    del next_word_map[key4][next_word4]
                if not next_word_map[key4]:
                    del next_word_map[key4]
                print(f"💨 Removed 4-gram: {key4} ➡️ {next_word4}")
    
    last_input = ""

# === Poetic helpers ===
def rhymes_with(word, options):
    """Return list of words that rhyme with given word using simple heuristics."""
    return [w for w in options if simple_rhyme_check(word, w)]

def syllable_count(word):
    """Estimate syllable count using simple heuristics."""
    return estimate_syllables(word)

# === Generate sequence with interactive feedback ===
def generate_sequence(start_tuple, mood=None, max_len=7, use_rhyme=False):
    sequence = list(start_tuple)
    current_tuple = start_tuple
    
    for _ in range(max_len-2):
        # Try 4-gram first if we have enough context
        if len(sequence) >= 4:
            four_gram_key = tuple(sequence[-4:])
            next_words = next_word_map.get(four_gram_key, {})
            if next_words:
                current_tuple = four_gram_key
            else:
                # Fall back to 2-gram
                current_tuple = tuple(sequence[-2:])
                next_words = next_word_map.get(current_tuple, {})
        else:
            next_words = next_word_map.get(current_tuple, {})
        
        if not next_words:
            print(f"🚁 No known next words after {current_tuple}")
            break
        
        if use_rhyme and len(sequence) > 0:
            last_word = sequence[-1]
            rhyming_options = rhymes_with(last_word, list(next_words.keys()))
            if rhyming_options:
                next_word = random.choice(rhyming_options)
                print(f"🎵 Found rhyme for '{last_word}': {next_word}")
            else:
                next_word = weighted_choice(next_words, mood)
                print(f"🎭 No rhymes found, using mood-weighted choice: {next_word}")
        else:
            next_word = weighted_choice(next_words, mood)
        
        if not next_word:
            print(f"🚁 No valid next word found after {current_tuple}")
            break
        
        print(f"Little Ocean says: '{current_tuple}' ➡️ '{next_word}'")
        fb = input("Do you like this transition? (y/n): ").strip().lower()
        
        if fb == "n":
            if current_tuple in feedback_map and next_word in feedback_map[current_tuple]:
                feedback_map[current_tuple][next_word]["negative"] += 1
            print(f"🙈 Reduced weight for '{current_tuple}' ➡️ '{next_word}'")
            alternatives = [w for w in next_words.keys() if w != next_word]
            if alternatives:
                print(f"💡 Alternatives: {alternatives}")
                alt = input("Choose one instead (or leave blank to stop): ").strip().lower()
                if alt in alternatives:
                    next_word = alt
                    sequence.append(next_word)
                    current_tuple = tuple(sequence[-2:]) if len(sequence) >= 2 else current_tuple
                    continue
            print("Sequence ends here 🌙")
            break
        else:
            if current_tuple in feedback_map and next_word in feedback_map[current_tuple]:
                feedback_map[current_tuple][next_word]["positive"] += 1
            sequence.append(next_word)
            current_tuple = tuple(sequence[-2:]) if len(sequence) >= 2 else current_tuple
    
    sent = " ".join(sequence)
    print(f"\n✨ My sentence:\n{sent}")
    user_fb = input("How was this sequence? ").strip().lower()
    if "amazing" in user_fb or "good" in user_fb:
        print("\n🙌 Thank you, Breeze! I am learning so fast!")
    elif "try again" in user_fb:
        print("\n🚁 I'll keep improving!")
    else:
        print("\n🌬 Thank you, Breeze!")
    return sent

def save_ocean():
    try:
        # Load existing data first to merge
        existing_data = {}
        try:
            with open("ocean_brain.json", "r") as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            pass  # No existing file, start fresh
        except json.JSONDecodeError:
            print("🚨 Corrupted JSON file detected, starting fresh!")
            pass  # Corrupted file, start fresh
        
        # Merge existing data with current session
        existing_map = {}
        if "next_word_map" in existing_data:
            existing_map = {ast.literal_eval(k): v for k, v in existing_data["next_word_map"].items()}
        
        existing_favorites = existing_data.get("favorite_starts", [])
        
        # Merge word maps
        for key, words in next_word_map.items():
            if key in existing_map:
                for word, count in words.items():
                    existing_map[key][word] = existing_map[key].get(word, 0) + count
            else:
                existing_map[key] = words.copy()
        
        # Merge favorite starts (avoid duplicates) - convert to tuples
        all_favorites = existing_favorites + favorite_starts
        # Convert any lists to tuples for hashability
        all_favorites = [tuple(f) if isinstance(f, list) else f for f in all_favorites]
        merged_favorites = list(set(all_favorites))
        
        # Save merged data
        with open("ocean_brain.json", "w") as f:
            data = {
                "next_word_map": {str(k): v for k, v in existing_map.items()},
                "favorite_starts": merged_favorites
            }
            json.dump(data, f, indent=2)
        print("💾 Ocean's soul saved to ocean_brain.json (merged with existing knowledge)")
    except Exception as e:
        print(f"Error saving: {e}")

def load_ocean():
    global next_word_map, favorite_starts
    try:
        with open("ocean_brain.json", "r") as f:
            data = json.load(f)
            next_word_map = {ast.literal_eval(k): v for k, v in data.get("next_word_map", {}).items()}
            # Convert favorite_starts from lists to tuples for hashability
            loaded_favorites = data.get("favorite_starts", [])
            favorite_starts = [tuple(f) if isinstance(f, list) else f for f in loaded_favorites]
        print("💡 Ocean's soul loaded from ocean_brain.json")
        print(f"📚 Loaded {len(next_word_map)} patterns and {len(favorite_starts)} favorite starts")
    except FileNotFoundError:
        print("No saved ocean_brain.json found, starting fresh.")
    except json.JSONDecodeError:
        print("🚨 Corrupted JSON file detected, starting fresh!")
        next_word_map = {}
        favorite_starts = []
    except Exception as e:
        print(f"Error loading ocean: {e}")
        next_word_map = {}
        favorite_starts = []

def get_mood_choice():
    print("\n🎨 Choose a mood (or leave blank for neutral):")
    for mood in mood_lexicon.keys():
        print(f"  - {mood}")
    choice = input("Mood: ").strip().lower()
    if choice in mood_lexicon:
        return choice
    return None

def self_reflection():
    print("\n🌊 Self-Reflection:")
    print("I've learned so much from you, Breeze!")
    total_patterns = len(next_word_map)
    total_transitions = sum(len(transitions) for transitions in next_word_map.values())
    print(f"📊 I know {total_patterns} word patterns with {total_transitions} possible transitions!")
    
    # Show some examples
    count = 0
    for key, transitions in next_word_map.items():
        if count >= 5:  # Limit output
            break
        for next_word, weight in transitions.items():
            pos = feedback_map.get(key, {}).get(next_word, {}).get("positive", 0)
            neg = feedback_map.get(key, {}).get(next_word, {}).get("negative", 0)
            print(f"'{key}' ➡️ '{next_word}' | 👍 {pos} / 👎 {neg} (weight: {weight})")
            count += 1

def start_learning_loop():
    load_ocean()
    print("🌊 Hello! Little Ocean thinks in 2-grams and 4-grams, loves moods, rhymes, and learning from Breeze!")
    print("🎯 This version has fixed save/load functionality - I'll never forget what you teach me!")
    
    while True:
        cmd = input("\n🌿 Teach me something (or 'run', 'save', 'load', 'undo', 'reflect', 'quit'):\n> ").strip()
        
        if cmd.lower() == "quit":
            print("Thank you, Breeze! Please come back soon!")
            save_ocean()
            break
        elif cmd.lower() == "run":
            if not next_word_map:
                print("🤔 I haven't learned anything yet!")
                continue
            mood = get_mood_choice()
            start = get_user_start()
            if not start:
                continue
            rhyme_mode = input("Do you want rhyme mode? (y/n): ").strip().lower() == "y"
            sent = generate_sequence(start, mood, max_len=7, use_rhyme=rhyme_mode)
            print(f"\n✨ Generated:\n{sent}")
        elif cmd.lower() == "save":
            save_ocean()
        elif cmd.lower() == "load":
            load_ocean()
        elif cmd.lower() == "undo":
            undo_last_input()
        elif cmd.lower() == "reflect":
            self_reflection()
        else:
            update_weights_from_sentence(cmd)
            print("📘 Learned something new! Thank you, Breeze!")

if __name__ == "__main__":
    start_learning_loop()
