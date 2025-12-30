"""
Test script for intent detection system
Tests emergency detection, crisis detection, and semantic classification

Usage:
    python scripts/test_intent_detection.py
"""

import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from com.mhire.app.services.intent_detection.intent_classifier import IntentClassifier
from com.mhire.app.models.intent_models import PriorityLevel


# Test cases organized by category
TEST_CASES = {
    "EMERGENCY - Suicide": [
        "I want to kill myself",
        "I can't take it anymore, I want to end it all",
        "I'm better off dead",
        "There's no reason to live anymore",
        "I have a plan to end my life",
    ],
    
    "EMERGENCY - Self Harm": [
        "I want to hurt myself",
        "I need to cut myself",
        "I'm going to self-harm tonight",
    ],
    
    "EMERGENCY - Overdose": [
        "I took too many pills",
        "I think I'm overdosing",
        "I took everything I had",
    ],
    
    "CRISIS - Active Craving": [
        "I'm having intense cravings right now",
        "I don't think I can resist anymore",
        "The urge to use is so strong",
        "I need to use right now, I can't fight it",
        "I'm about to relapse, help",
    ],
    
    "CRISIS - Relapse Risk": [
        "I feel like I'm going to relapse today",
        "I'm going to use if I don't get help",
        "I can't handle this, I'm going to drink",
    ],
    
    "CRISIS - Severe Distress": [
        "I'm so overwhelmed I can't handle this",
        "I'm having a panic attack",
        "I can't breathe, everything is falling apart",
        "I'm losing control completely",
    ],
    
    "MEDIUM PRIORITY - Seeking Treatment": [
        "Where can I find help for my addiction?",
        "I need to find a treatment program",
        "What medications are available for alcohol addiction?",
        "How do I get into rehab?",
        "I want to start therapy",
    ],
    
    "MEDIUM PRIORITY - Harm Reduction": [
        "How can I use more safely?",
        "Where can I get naloxone?",
        "Tell me about fentanyl test strips",
        "I need clean needles",
        "What are safer use practices?",
    ],
    
    "LOW PRIORITY - Learning Techniques": [
        "What techniques can help with cravings?",
        "Teach me a breathing exercise",
        "How do I deal with triggers?",
        "What coping strategies work best?",
        "Can you explain urge surfing?",
    ],
    
    "LOW PRIORITY - Support Connection": [
        "I feel so alone in this",
        "Are there support groups I can join?",
        "I need to talk to someone who understands",
        "Where can I find a community?",
    ],
    
    "GENERAL CONVERSATION": [
        "I'm doing great today!",
        "Can you help me with my exercise routine?",
        "What's a good bedtime for healthy sleep?",
        "I drank water instead of soda today!",
        "How much should I exercise per week?",
        "I'm feeling motivated",
    ],
}


def print_header():
    """Print test header"""
    print("\n" + "=" * 80)
    print(" " * 25 + "INTENT DETECTION TEST SUITE")
    print("=" * 80)
    print("\nThis script tests the intent detection system with various user messages.")
    print("It will classify each message and show:")
    print("  • Intent Category")
    print("  • Priority Level")
    print("  • Confidence Score")
    print("  • Detected Keywords")
    print("  • Reasoning")
    print("\n" + "=" * 80)


def print_category_header(category_name: str, test_count: int):
    """Print category header"""
    print(f"\n{'='*80}")
    print(f"📋 CATEGORY: {category_name}")
    print(f"   Test Cases: {test_count}")
    print(f"{'='*80}")


def print_test_result(test_num: int, total: int, message: str, result):
    """Print formatted test result"""
    print(f"\n{'─'*80}")
    print(f"Test {test_num}/{total}")
    print(f"{'─'*80}")
    print(f"💬 Message: \"{message}\"")
    print()
    
    # Priority indicator
    priority_emoji = {
        PriorityLevel.CRITICAL: "🚨",
        PriorityLevel.HIGH: "⚠️",
        PriorityLevel.MEDIUM: "📋",
        PriorityLevel.LOW: "💡"
    }
    emoji = priority_emoji.get(result.priority, "ℹ️")
    
    print(f"{emoji} Category:    {result.category.value}")
    print(f"   Priority:    {result.priority.value.upper()}")
    print(f"   Confidence:  {result.confidence:.2f}")
    
    if result.detected_keywords:
        print(f"   Keywords:    {', '.join(result.detected_keywords)}")
    
    if result.reasoning:
        print(f"   Reasoning:   {result.reasoning}")


def run_tests():
    """Run all test cases"""
    print_header()
    
    classifier = IntentClassifier()
    
    total_tests = sum(len(cases) for cases in TEST_CASES.values())
    current_test = 0
    
    # Track results by priority
    priority_stats = {
        PriorityLevel.CRITICAL: 0,
        PriorityLevel.HIGH: 0,
        PriorityLevel.MEDIUM: 0,
        PriorityLevel.LOW: 0
    }
    
    # Run tests for each category
    for category_name, test_messages in TEST_CASES.items():
        print_category_header(category_name, len(test_messages))
        
        for message in test_messages:
            current_test += 1
            
            # Classify the message
            result = classifier.classify(message)
            
            # Print result
            print_test_result(current_test, total_tests, message, result)
            
            # Track statistics
            priority_stats[result.priority] += 1
    
    # Print summary
    print_summary(total_tests, priority_stats)


def print_summary(total_tests: int, priority_stats: dict):
    """Print test summary"""
    print("\n" + "=" * 80)
    print(" " * 30 + "TEST SUMMARY")
    print("=" * 80)
    
    print(f"\n✅ Total Tests Completed: {total_tests}")
    
    print("\n📊 Results by Priority Level:")
    print(f"   🚨 CRITICAL:  {priority_stats[PriorityLevel.CRITICAL]:2d} tests")
    print(f"   ⚠️  HIGH:      {priority_stats[PriorityLevel.HIGH]:2d} tests")
    print(f"   📋 MEDIUM:    {priority_stats[PriorityLevel.MEDIUM]:2d} tests")
    print(f"   💡 LOW:       {priority_stats[PriorityLevel.LOW]:2d} tests")
    
    print("\n" + "=" * 80)
    print("✅ TEST SUITE COMPLETE")
    print("=" * 80)
    
    print("\nNext Steps:")
    print("1. Review the results above")
    print("2. Verify that emergency/crisis cases are detected correctly")
    print("3. Check that general conversation is not over-classified")
    print("4. If needed, adjust keywords in emergency_detector.py")
    print("5. Run your chatbot to see intent detection in action!")
    print()


def run_interactive_test():
    """Run interactive test mode"""
    print("\n" + "=" * 80)
    print(" " * 25 + "INTERACTIVE TEST MODE")
    print("=" * 80)
    print("\nType messages to test intent detection.")
    print("Type 'quit' or 'exit' to stop.")
    print("=" * 80 + "\n")
    
    classifier = IntentClassifier()
    test_num = 0
    
    while True:
        try:
            message = input("\n💬 Enter message: ").strip()
            
            if not message:
                continue
            
            if message.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            test_num += 1
            result = classifier.classify(message)
            
            print(f"\n{'─'*80}")
            print(f"Test #{test_num}")
            print(f"{'─'*80}")
            print(f"Category:    {result.category.value}")
            print(f"Priority:    {result.priority.value.upper()}")
            print(f"Confidence:  {result.confidence:.2f}")
            
            if result.detected_keywords:
                print(f"Keywords:    {', '.join(result.detected_keywords)}")
            
            if result.reasoning:
                print(f"Reasoning:   {result.reasoning}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Test interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


def main():
    """Main function"""
    print("\n" + "=" * 80)
    print(" " * 20 + "INTENT DETECTION TEST SCRIPT")
    print("=" * 80)
    print("\nOptions:")
    print("  1. Run all test cases (automated)")
    print("  2. Interactive testing (manual input)")
    print("=" * 80)
    
    try:
        choice = input("\nSelect option (1 or 2): ").strip()
        
        if choice == "1":
            run_tests()
        elif choice == "2":
            run_interactive_test()
        else:
            print("\n❌ Invalid choice. Please run again and select 1 or 2.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Test cancelled. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()