
"""
Main entry point for the Support Agent system.

This module provides the command-line interface for running the support
agent workflow and testing different scenarios.
"""

import argparse
import json
import logging
from typing import Dict, Any

from graph import create_graph, run_support_workflow, validate_workflow_health
from config import SYSTEM_CONFIG
from utils import generate_ticket_id

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main execution function with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description="AI-Powered Customer Support Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --subject "Billing issue" --description "I was charged twice"
  python main.py --test
  python main.py --health-check
  python main.py --interactive
        """
    )
    
    parser.add_argument(
        "--subject", 
        type=str, 
        help="Subject line of the support ticket"
    )
    parser.add_argument(
        "--description", 
        type=str, 
        help="Detailed description of the issue"
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug output with full state information"
    )
    parser.add_argument(
        "--test", 
        action="store_true", 
        help="Run predefined test scenarios"
    )
    parser.add_argument(
        "--health-check", 
        action="store_true", 
        help="Run system health checks"
    )
    parser.add_argument(
        "--interactive", 
        action="store_true", 
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()
    
    try:
        if args.health_check:
            run_health_check()
        elif args.test:
            run_test_scenarios()
        elif args.interactive:
            run_interactive_mode()
        elif args.subject or args.description:
            run_single_ticket(args.subject or "", args.description or "", args.debug)
        else:
            # Default to example ticket
            run_example_ticket(args.debug)
    
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        return 1
    
    return 0

def run_single_ticket(subject: str, description: str, debug: bool = False) -> None:
    """
    Process a single support ticket.
    
    Args:
        subject: Subject line of the ticket
        description: Description of the issue
        debug: Whether to show debug information
    """
    print(f"\n Processing Support Ticket")
    print(f"Subject: {subject}")
    print(f"Description: {description}")
    print("-" * 50)
    
    try:
        result = run_support_workflow(subject, description, debug)
        
        print(f"\n✅ Ticket Processing Complete")
        print(f"Ticket ID: {result['ticket_id']}")
        print(f"Category: {result['category']}")
        print(f"Attempts: {result['attempts']}")
        
        if result.get('escalated'):
            print(f" Status: ESCALATED")
            if debug and result.get('debug_info', {}).get('escalation_reason'):
                print(f"Reason: {result['debug_info']['escalation_reason']}")
        else:
            print(f"✅ Status: RESOLVED")
        
        print(f"\n Response:")
        print(result['answer'])
        
        if debug and 'debug_info' in result:
            print(f"\n Debug Information:")
            debug_info = result['debug_info']
            print(f"KB Match ID: {debug_info.get('kb_match_id', 'None')}")
            print(f"AI Generated: {debug_info.get('ai_generated', False)}")
            print(f"Review Passed: {debug_info.get('review_passed', False)}")
    
    except Exception as e:
        print(f"\n❌ Error processing ticket: {str(e)}")

def run_example_ticket(debug: bool = False) -> None:
    """Run the default example ticket."""
    print("Running default example (billing issue)...")
    run_single_ticket(
        subject="password help", 
        description="Reset email not working",
        debug=debug
    )

def run_test_scenarios() -> None:
    """Run a series of predefined test scenarios."""
    print("\n Running Test Scenarios")
    print("=" * 50)
    
    test_cases = [
        {
            "name": "Billing - Double Charge",
            "subject": "Double charged",
            "description": "I was charged twice for my subscription this month"
        },
        {
            "name": "Technical - Password Reset", 
            "subject": "Can't login",
            "description": "I forgot my password and need to reset it"
        },
        {
            "name": "Security - Account Safety",
            "subject": "Account security",
            "description": "Is my account secure? I'm worried about data privacy"
        },
        {
            "name": "General - Unknown Issue",
            "subject": "Strange problem",
            "description": "Something weird is happening but I can't explain it"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['name']} ---")
        try:
            result = run_support_workflow(
                test_case['subject'], 
                test_case['description']
            )
            print(f"Category: {result['category']}")
            print(f"Status: {'ESCALATED' if result.get('escalated') else 'RESOLVED'}")
            print(f"Response: {result['answer'][:100]}...")
        except Exception as e:
            print(f" Test failed: {str(e)}")
    
    print(f"\n✅ Test scenarios completed")

def run_health_check() -> None:
    """Run system health checks."""
    print("\n Running Health Checks")
    print("=" * 30)
    
    try:
        health_status = validate_workflow_health()
        
        for component, status in health_status.items():
            status_icon = "✅" if status else "❌"
            print(f"{status_icon} {component.replace('_', ' ').title()}: {status}")
        
        overall_health = all(health_status.values())
        print(f"\n{'✅' if overall_health else '❌'} Overall Health: {'HEALTHY' if overall_health else 'ISSUES DETECTED'}")
        
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")

def run_interactive_mode() -> None:
    """Run the support agent in interactive mode."""
    print("\n Interactive Support Agent")
    print("Type 'quit' to exit")
    print("=" * 40)
    
    while True:
        try:
            print("\nEnter your support request:")
            subject = input("Subject: ").strip()
            
            if subject.lower() == 'quit':
                break
            
            description = input("Description: ").strip()
            
            if description.lower() == 'quit':
                break
            
            if not subject and not description:
                print("Please provide either a subject or description.")
                continue
            
            print("\nProcessing your request...")
            result = run_support_workflow(subject, description)
            
            print(f"\n Response (Ticket {result['ticket_id']}):")
            print(result['answer'])
            
            if result.get('escalated'):
                print("\n Your ticket has been escalated to human support.")
        
        except KeyboardInterrupt:
            print("\n\nExiting interactive mode...")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    exit(main())
