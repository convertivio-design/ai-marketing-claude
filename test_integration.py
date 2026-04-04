from marketing_wrapper import run_marketing_audit, get_social_media_plan
import json

def test_wrapper():
    print("Testing run_marketing_audit...")
    try:
        results = run_marketing_audit("https://example.com")
        print(f"Success: Overall score is {results['analysis']['overall_score']}")
    except Exception as e:
        print(f"Error in run_marketing_audit: {e}")

    print("\nTesting get_social_media_plan...")
    plan = get_social_media_plan("AI Marketing", platforms=["linkedin"], days=7)
    print(f"Success: Generated {len(plan['calendar'])} days of content for {plan['platforms']}")

if __name__ == "__main__":
    test_wrapper()
