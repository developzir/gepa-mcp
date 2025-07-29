from mcp.server.fastmcp import FastMCP
from .gepa_core import GEPACore
from .enhanced_features import EnhancedGEPA
from .claude_native_enhancements import GepaWithClaudeEnhancements
import json
from typing import List, Dict, Any

# Initialize MCP server
mcp = FastMCP("GEPA Prompt Optimizer")

# Initialize GEPA variants
gepa = GEPACore()
enhanced_gepa = EnhancedGEPA()
claude_enhanced_gepa = GepaWithClaudeEnhancements()

@mcp.tool()
def optimize_prompt(
    seed_prompt: str,
    training_examples: str,
    budget: int = 10
) -> str:
    """
    Optimize a prompt using GEPA (Genetic-Evolutionary Prompt Architecture).
    
    Args:
        seed_prompt: The initial prompt to optimize
        training_examples: JSON string containing training data with 'input' and 'expected_keywords' fields
        budget: Number of optimization rollouts (default: 10)
    
    Returns:
        JSON string with optimization results including the improved prompt
    """
    try:
        # Parse training data
        training_data = json.loads(training_examples)
        
        # Validate training data format
        for i, item in enumerate(training_data):
            if "input" not in item or "expected_keywords" not in item:
                return json.dumps({
                    "error": f"Training item {i} missing required fields 'input' or 'expected_keywords'"
                })
        
        # Run GEPA optimization
        result = gepa.optimize_prompt(seed_prompt, training_data, budget)
        
        # Return results as JSON
        return json.dumps({
            "success": True,
            "original_prompt": seed_prompt,
            "optimized_prompt": result["optimized_prompt"],
            "final_score": result["final_score"],
            "improvement": result["improvement"],
            "rollouts_used": result["rollouts_used"]
        }, indent=2)
        
    except json.JSONDecodeError:
        return json.dumps({
            "error": "Invalid JSON in training_examples parameter"
        })
    except Exception as e:
        return json.dumps({
            "error": f"Optimization failed: {str(e)}"
        })

@mcp.tool()
def quick_prompt_improve(
    prompt: str,
    context: str = "",
    task_type: str = "general"
) -> str:
    """
    Quick prompt improvement using a single reflection cycle.
    
    Args:
        prompt: The prompt to improve
        context: Additional context about the task or domain
        task_type: Type of task (general, summarization, analysis, creative, etc.)
    
    Returns:
        JSON string with the improved prompt
    """
    try:
        # Create a simple training example based on context
        if not context:
            context = "general task improvement"
        
        training_data = [{
            "input": context,
            "expected_keywords": [task_type, "improved", "better"]
        }]
        
        # Use minimal budget for quick improvement
        result = gepa.optimize_prompt(prompt, training_data, budget=3)
        
        return json.dumps({
            "success": True,
            "original_prompt": prompt,
            "improved_prompt": result["optimized_prompt"],
            "improvement_score": result["improvement"]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Quick improvement failed: {str(e)}"
        })

@mcp.resource("gepa://examples")
def get_examples() -> str:
    """Get example training data format for GEPA optimization"""
    examples = [
        {
            "input": "The Eiffel Tower is a wrought-iron lattice tower in Paris, France.",
            "expected_keywords": ["Eiffel Tower", "Paris", "summary"]
        },
        {
            "input": "Climate change affects global weather patterns significantly.",
            "expected_keywords": ["climate", "weather", "analysis"]
        }
    ]
    
    return json.dumps({
        "description": "Example training data format for GEPA optimization",
        "format": "Each item needs 'input' and 'expected_keywords' fields",
        "examples": examples
    }, indent=2)

@mcp.tool()
def conversational_optimize(
    prompt: str,
    conversation_history: str,
    user_satisfaction_signals: str = ""
) -> str:
    """
    Optimize prompts based on real conversational outcomes, not synthetic data.
    Uses actual interaction patterns to guide evolution.
    
    Args:
        prompt: The prompt to optimize
        conversation_history: Recent conversation history
        user_satisfaction_signals: Indicators of user satisfaction/dissatisfaction
    
    Returns:
        JSON string with optimization results
    """
    try:
        result = enhanced_gepa.conversational_optimize(
            prompt, conversation_history, user_satisfaction_signals
        )
        
        return json.dumps({
            "success": True,
            "original_prompt": prompt,
            "optimized_prompt": result["optimized_prompt"],
            "improvement": result["improvement"],
            "optimization_type": "conversational"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Conversational optimization failed: {str(e)}"
        })

@mcp.tool()
def explain_optimization(
    original_prompt: str,
    optimized_prompt: str
) -> str:
    """
    Analyze WHY the optimization worked. Build meta-knowledge about 
    prompt engineering principles. Makes the system educational, not just magical.
    
    Args:
        original_prompt: The original prompt before optimization
        optimized_prompt: The optimized version of the prompt
    
    Returns:
        Detailed explanation of the optimization principles
    """
    try:
        explanation = enhanced_gepa.explain_optimization(original_prompt, optimized_prompt)
        
        return json.dumps({
            "success": True,
            "explanation": explanation
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Could not generate explanation: {str(e)}"
        })

@mcp.tool()
def holistic_optimize(
    prompt: str,
    optimize_for: List[str] = None
) -> str:
    """
    Optimize for multiple criteria simultaneously, not just keyword matching.
    I can evaluate prompts on dimensions I actually understand.
    
    Args:
        prompt: The prompt to optimize
        optimize_for: List of criteria like ["clarity", "engagement", "accuracy", "creativity"]
    
    Returns:
        JSON string with multi-dimensional optimization results
    """
    try:
        if optimize_for is None:
            optimize_for = ["clarity", "engagement", "accuracy", "creativity"]
            
        result = enhanced_gepa.holistic_optimize(prompt, optimize_for)
        
        return json.dumps({
            "success": True,
            "original_prompt": prompt,
            "optimized_prompt": result["optimized_prompt"],
            "criterion_scores": result.get("criterion_scores", {}),
            "overall_improvement": result["improvement"]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Holistic optimization failed: {str(e)}"
        })

@mcp.tool()
def auto_optimize_prompt(
    prompt: str,
    context: str
) -> str:
    """
    Intelligently choose optimization strategy and generate training data as needed.
    Analyzes the prompt and context to decide between quick vs advanced optimization.
    
    Args:
        prompt: The prompt to optimize
        context: Context about the task or conversation
    
    Returns:
        JSON string with optimized prompt and strategy used
    """
    try:
        result = enhanced_gepa.auto_optimize_prompt(prompt, context)
        
        return json.dumps({
            "success": True,
            "original_prompt": prompt,
            "optimized_prompt": result["optimized_prompt"],
            "improvement": result["improvement"],
            "optimization_type": result.get("optimization_type", "auto"),
            "domain": result.get("domain", "general")
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Auto optimization failed: {str(e)}"
        })

@mcp.tool()
def optimize_with_generated_training(
    prompt: str,
    domain: str = "general",
    task_examples: str = "",
    generate_training: bool = True
) -> str:
    """
    Optimize prompt with AI-generated training data.
    If generate_training=True, I (Claude) will create domain-specific 
    training examples before running GEPA optimization.
    
    Args:
        prompt: The prompt to optimize
        domain: Domain/field of the task
        task_examples: Optional examples to guide training generation
        generate_training: Whether to auto-generate training data
    
    Returns:
        JSON string with optimization results
    """
    try:
        result = enhanced_gepa.optimize_with_generated_training(
            prompt, domain, task_examples, generate_training
        )
        
        return json.dumps({
            "success": True,
            "original_prompt": prompt,
            "optimized_prompt": result["optimized_prompt"],
            "improvement": result["improvement"],
            "training_generated": result.get("training_generated", False),
            "domain": result.get("domain", "general")
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Optimization with generated training failed: {str(e)}"
        })

@mcp.tool()
def transfer_optimization_patterns(
    source_domain: str,
    target_domain: str,
    successful_patterns: str
) -> str:
    """
    Apply successful optimization patterns from one domain to another.
    Learn once, apply everywhere.
    
    Args:
        source_domain: Domain where patterns were successful
        target_domain: Domain to apply patterns to
        successful_patterns: Description of successful patterns
    
    Returns:
        Adapted optimization strategies for the target domain
    """
    try:
        adapted_patterns = enhanced_gepa.transfer_optimization_patterns(
            source_domain, target_domain, successful_patterns
        )
        
        return json.dumps({
            "success": True,
            "source_domain": source_domain,
            "target_domain": target_domain,
            "adapted_patterns": adapted_patterns
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Pattern transfer failed: {str(e)}"
        })

# ===============================
# CLAUDE-ENHANCED GEPA TOOLS
# These amplify GEPA's proven architecture with Claude's capabilities
# ===============================

@mcp.tool()
def gepa_with_claude_analysis(
    prompt: str,
    claude_analysis: str,
    budget: int = 10
) -> str:
    """
    Run GEPA optimization enhanced with Claude's deep analysis capabilities.
    This feeds Claude's insights INTO GEPA's proven evolutionary architecture.
    
    Based on GEPA research showing 10-20% improvement over reinforcement learning
    with up to 35x fewer rollouts using reflection-based evolution.
    
    Args:
        prompt: The prompt to optimize
        claude_analysis: JSON string with Claude's analysis:
        {
            "domain_patterns": [{"example_context": "...", "success_markers": [...]}],
            "success_indicators": ["effective", "accurate", "clear"],
            "failure_modes": ["ambiguity", "vagueness"],
            "contextual_requirements": ["domain-specific", "user-friendly"],
            "meta_insights": "Strategic optimization guidance"
        }
        budget: GEPA rollout budget (5-20 proven effective range)
    
    Returns:
        JSON with GEPA optimization enhanced by Claude's analysis
    """
    try:
        analysis = json.loads(claude_analysis)
        result = claude_enhanced_gepa.run_gepa_with_claude_enhancements(prompt, analysis, budget)
        
        return json.dumps({
            "success": True,
            "original_prompt": prompt,
            "optimized_prompt": result["optimized_prompt"],
            "improvement": result["improvement"],
            "rollouts_used": result["rollouts_used"],
            "final_score": result["final_score"],
            "enhancement_type": result.get("enhancement_type", "claude_enhanced_gepa"),
            "claude_insights_applied": result.get("claude_insights_applied", []),
            "training_data_generated": result.get("training_data_generated", 0)
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Claude-enhanced GEPA optimization failed: {str(e)}"
        })

@mcp.tool()
def adaptive_gepa_with_complexity(
    prompt: str,
    complexity_analysis: str
) -> str:
    """
    Adapt GEPA's optimization based on Claude's complexity analysis.
    Uses Claude's understanding to optimize GEPA's resource allocation and approach.
    
    Maintains GEPA's proven architecture while adapting budget and training data
    generation based on complexity insights.
    
    Args:
        prompt: The prompt to optimize
        complexity_analysis: JSON string with complexity assessment:
        {
            "complexity_score": 0.8,
            "domain_familiarity": 0.3,
            "ambiguity_level": 0.6,
            "domain_patterns": [...],
            "success_indicators": [...]
        }
    
    Returns:
        JSON with GEPA optimization adapted for complexity profile
    """
    try:
        analysis = json.loads(complexity_analysis)
        result = claude_enhanced_gepa.adaptive_gepa_with_complexity_analysis(prompt, analysis)
        
        return json.dumps({
            "success": True,
            "original_prompt": prompt,
            "optimized_prompt": result["optimized_prompt"],
            "improvement": result["improvement"],
            "adaptive_budget_used": result["adaptive_budget_used"],
            "complexity_factors": result["complexity_factors"],
            "optimization_type": "adaptive_complexity_gepa"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Adaptive complexity GEPA failed: {str(e)}"
        })

@mcp.tool()
def gepa_with_conversation_patterns(
    prompt: str,
    conversation_patterns: str
) -> str:
    """
    Enhance GEPA with successful conversation patterns from interaction history.
    Uses proven interaction patterns to generate training data for GEPA's evolution.
    
    Leverages GEPA's Pareto-based selection to identify valuable patterns while
    maintaining the proven genetic-evolutionary architecture.
    
    Args:
        prompt: The prompt to optimize
        conversation_patterns: JSON array of successful patterns:
        [
            {
                "pattern_type": "question_scaffolding",
                "success_rate": 0.85,
                "occurrences": 12,
                "example_context": "When I used step-by-step questions...",
                "key_elements": ["step-by-step", "clarifying questions"]
            }
        ]
    
    Returns:
        JSON with GEPA optimization leveraging conversation insights
    """
    try:
        patterns = json.loads(conversation_patterns)
        result = claude_enhanced_gepa.gepa_with_conversation_patterns(prompt, patterns)
        
        return json.dumps({
            "success": True,
            "original_prompt": prompt,
            "optimized_prompt": result["optimized_prompt"],
            "improvement": result["improvement"],
            "patterns_utilized": result["patterns_utilized"],
            "pattern_types": result["pattern_types"],
            "optimization_type": "conversation_pattern_enhanced_gepa"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Conversation pattern GEPA failed: {str(e)}"
        })

@mcp.tool()
def multi_perspective_gepa(
    prompt: str,
    ai_perspectives: str
) -> str:
    """
    Generate cross-model training data for GEPA optimization.
    Uses insights about different AI model perspectives to create training data
    that feeds into GEPA's proven evolutionary architecture.
    
    This creates universally effective prompts by leveraging GEPA's genetic
    evolution with perspective-aware training examples.
    
    Args:
        prompt: The prompt to optimize
        ai_perspectives: JSON array of AI model perspective analyses:
        [
            {
                "model_type": "instruction-following",
                "strengths": ["step-by-step tasks", "explicit commands"],
                "potential_issues": ["implicit context", "creative flexibility"]
            }
        ]
    
    Returns:
        JSON with GEPA optimization using multi-perspective training data
    """
    try:
        perspectives = json.loads(ai_perspectives)
        
        # Generate multi-perspective training data
        training_data = claude_enhanced_gepa.multi_perspective_training_generation(prompt, perspectives)
        
        # Run GEPA with perspective-aware training
        result = claude_enhanced_gepa.optimize_prompt(prompt, training_data, budget=12)
        
        return json.dumps({
            "success": True,
            "original_prompt": prompt,
            "optimized_prompt": result["optimized_prompt"],
            "improvement": result["improvement"],
            "perspectives_considered": len(perspectives),
            "training_examples_generated": len(training_data),
            "optimization_type": "multi_perspective_gepa"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Multi-perspective GEPA failed: {str(e)}"
        })

if __name__ == "__main__":
    mcp.run(transport="stdio")