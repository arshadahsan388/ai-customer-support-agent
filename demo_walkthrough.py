#!/usr/bin/env python3
"""
Demo Walkthrough Script - AI Support Agent
============================================

This script demonstrates exactly how our support agent works by processing
real tickets and showing the internal workflow step-by-step.

Story: From Raw Ticket → AI-Powered Resolution
"""

import json
import time
from typing import Dict, Any

from graph import run_support_workflow
from utils import generate_ticket_id

def print_section(title: str, content: str = "", color: str = "blue"):
    """Pretty print sections with colors."""
    colors = {
        "blue": "\033[94m",
        "green": "\033[92m", 
        "yellow": "\033[93m",
        "red": "\033[91m",
        "reset": "\033[0m"
    }
    
    print(f"\n{colors.get(color, '')}")
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print(f"{colors['reset']}")
    if content:
        print(content)

def show_state_transition(step: str, state: Dict[str, Any]):
    """Display current state during workflow."""
    print(f"\n🔄 **{step}**")
    print("-" * 40)
    
    if 'category' in state:
        print(f"📂 Category: {state['category']}")
    if 'knowledge_base_result' in state:
        kb_result = state['knowledge_base_result']
        if kb_result and kb_result != "No relevant solution found":
            print(f"📚 Found KB Solution: {kb_result[:100]}...")
        else:
            print(f"📚 KB Result: {kb_result}")
    if 'ai_response' in state:
        print(f"🤖 AI Response: {state['ai_response'][:100]}...")
    if 'review_decision' in state:
        print(f"🔍 Review: {state['review_decision']}")
    if 'retry_count' in state:
        print(f"🔄 Retry Count: {state['retry_count']}")

def demo_ticket_processing():
    """Demonstrate processing different types of support tickets."""
    
    print_section("🎬 AI SUPPORT AGENT - LIVE DEMO", color="green")
    print("Watch how our AI processes real customer support tickets...")
    time.sleep(2)
    
    # Demo tickets representing different scenarios
    demo_tickets = [
        {
            "subject": "Cannot access my account",
            "description": "I forgot my password and the reset email isn't working",
            "expected_flow": "Security → KB Match → Direct Solution"
        },
        {
            "subject": "Billing discrepancy", 
            "description": "I was charged $50 but my plan should be $30",
            "expected_flow": "Billing → No KB Match → AI Generation → Review"
        },
        {
            "subject": "App keeps crashing",
            "description": "The mobile app crashes every time I try to upload a photo",
            "expected_flow": "Technical → Partial KB → AI Enhancement → Review"
        }
    ]
    
    for i, ticket in enumerate(demo_tickets, 1):
        print_section(f"🎫 TICKET #{i}: {ticket['subject']}", color="yellow")
        print(f"📝 Description: {ticket['description']}")
        print(f"🔮 Expected Flow: {ticket['expected_flow']}")
        
        print("\n⏱️  Processing ticket through our AI pipeline...")
        time.sleep(1)
        
        # Run the actual workflow
        try:
            initial_state = {
                "ticket_id": generate_ticket_id(),
                "subject": ticket["subject"],
                "description": ticket["description"],
                "retry_count": 0
            }
            
            # Process through our workflow
            result = run_support_workflow(initial_state)
            
            # Show the journey
            print_section("📊 PROCESSING JOURNEY", color="blue")
            
            print("1️⃣ **CLASSIFICATION**")
            print(f"   ✅ Categorized as: {result.get('category', 'Unknown')}")
            
            print("\n2️⃣ **KNOWLEDGE BASE SEARCH**")
            kb_result = result.get('knowledge_base_result', 'No result')
            if kb_result and kb_result != "No relevant solution found":
                print(f"   ✅ Found relevant solution")
                print(f"   📋 Solution: {kb_result[:150]}...")
            else:
                print(f"   ❌ No direct match found - proceeding to AI generation")
            
            print("\n3️⃣ **AI RESPONSE GENERATION**")
            if result.get('ai_response'):
                print(f"   ✅ Generated personalized response")
                print(f"   🤖 Response: {result['ai_response'][:150]}...")
            else:
                print(f"   ℹ️  Used knowledge base solution directly")
            
            print("\n4️⃣ **QUALITY REVIEW**")
            review = result.get('review_decision', 'Not reviewed')
            if review:
                print(f"   📝 Review Decision: {review}")
                print(f"   🔄 Retry Count: {result.get('retry_count', 0)}")
            
            print("\n5️⃣ **FINAL RESULT**")
            final_response = result.get('final_response', result.get('ai_response', kb_result))
            if final_response:
                print(f"   ✅ **CUSTOMER RECEIVES:**")
                print(f"   💬 {final_response}")
            else:
                print(f"   ⚠️  Escalated to human agent")
                
        except Exception as e:
            print(f"   ❌ Error processing ticket: {str(e)}")
        
        print("\n" + "⏸️ " * 20)
        input("Press Enter to continue to next ticket...")

def show_architecture_overview():
    """Show how the system is architecturally designed."""
    
    print_section("🏗️ SYSTEM ARCHITECTURE - How We Built It", color="blue")
    
    architecture_story = """
📦 **MODULAR DESIGN**
├── main.py          → Entry point & CLI interface
├── graph.py         → LangGraph workflow orchestration  
├── state.py         → Type-safe state management
├── config.py        → Centralized configuration
├── utils.py         → Helper functions
└── nodes/           → Individual processing steps
    ├── classify.py      → AI-powered categorization
    ├── retrieve.py      → Knowledge base search
    ├── auto_agent.py    → AI response generation  
    ├── review.py        → Quality assurance
    └── should_continue.py → Flow control decisions

🔄 **WORKFLOW PIPELINE**
Raw Ticket → Classify → Search KB → Generate AI Response → Review → Decision → Final Response

🧠 **KEY IMPLEMENTATIONS**
✅ LangGraph for workflow orchestration
✅ Google Gemini for AI processing
✅ TypedDict for type-safe state
✅ Retry logic with quality gates
✅ Comprehensive logging & error handling
✅ Modular node architecture for easy testing
"""
    print(architecture_story)

def show_technical_stack():
    """Show the technical implementation details."""
    
    print_section("⚙️ TECHNICAL STACK - What We Actually Used", color="green")
    
    tech_details = """
🔧 **CORE TECHNOLOGIES**
• Python 3.8+ (Type hints, modern syntax)
• LangGraph (Workflow orchestration)
• LangChain (AI model integration) 
• Google Gemini AI (Language model)
• CSV logging (Simple data persistence)

📂 **STATE MANAGEMENT**
• TypedDict for type safety
• Immutable state transitions
• Validation at each step
• Complete audit trail

🔍 **KNOWLEDGE BASE**
• Static keyword matching
• Similarity scoring algorithm  
• Predefined solution templates
• No external database (limitation)

🤖 **AI INTEGRATION**
• Google Gemini 1.5 Flash model
• Temperature 0.3 for consistency
• Prompt engineering for accuracy
• Context-aware response generation

🛡️ **QUALITY CONTROLS**
• Input sanitization
• Response validation
• Retry mechanism (max 2 attempts)
• Automatic escalation fallback
"""
    print(tech_details)

def main():
    """Main demo function."""
    print_section("🚀 AI SUPPORT AGENT DEMONSTRATION", 
                 "Ready to see our AI in action?", color="green")
    
    menu = """
What would you like to see?

1️⃣  Live Ticket Processing Demo
2️⃣  System Architecture Overview  
3️⃣  Technical Stack Details
4️⃣  Exit Demo

Choose (1-4): """
    
    while True:
        choice = input(menu)
        
        if choice == "1":
            demo_ticket_processing()
        elif choice == "2":
            show_architecture_overview()
        elif choice == "3":
            show_technical_stack()
        elif choice == "4":
            print_section("👋 Demo Complete!", 
                         "Thanks for exploring our AI Support Agent!", color="green")
            break
        else:
            print("Please choose 1, 2, 3, or 4")

if __name__ == "__main__":
    main()
