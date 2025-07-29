from mcp.server.fastmcp import FastMCP
from .gepa_core import GEPACore
import json
from typing import List, Dict, Any

# Initialize MCP server
mcp = FastMCP("GEPA Prompt Optimizer")

# Initialize core GEPA
gepa = GEPACore()

@mcp.tool()
def optimize_prompt(
    seed_prompt: str,
    training_examples: str,
    budget: int = 10
) -> str:
    """
    Optimize a prompt using GEPA (Genetic-Evolutionary Prompt Architecture).
    
    This is the core GEPA algorithm from the research paper that uses genetic-evolutionary
    methods to optimize prompts through multiple generations of variation and selection.
    
    Args:
        seed_prompt: The initial prompt to optimize
        training_examples: JSON string containing training data with 'input' and 'expected_keywords' fields
        budget: Number of optimization rollouts (default: 10)
    
    Returns:
        JSON string with optimization results including the improved prompt
        
    Example:
        training_examples = '[{"input": "summarize article", "expected_keywords": ["concise", "key_points", "clear"]}]'
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
    Quick prompt improvement using GEPA principles with a single optimization cycle.
    
    Ideal for fast improvements when you don't have specific training data or need
    immediate results. Uses the same core GEPA algorithm but with minimal budget.
    
    Args:
        prompt: The prompt to improve
        context: Additional context about the task or domain
        task_type: Type of task (general, summarization, analysis, creative, etc.)
    
    Returns:
        JSON string with the improved prompt
        
    Example:
        quick_prompt_improve("Write a summary", "for technical documentation", "summarization")
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

@mcp.tool()
def conversational_optimize(
    prompt: str,
    conversation_history: str,
    user_satisfaction_signals: str = ""
) -> str:
    """
    Optimize prompts based on conversation context and user feedback patterns.
    
    Uses conversation history to understand what works well and adapts the prompt
    optimization accordingly. This is particularly useful for mid-conversation
    prompt improvements.
    
    Args:
        prompt: The prompt to optimize
        conversation_history: Recent conversation context (what has been discussed)
        user_satisfaction_signals: Optional signals about what the user liked/disliked
    
    Returns:
        JSON string with the context-optimized prompt
        
    Example:
        conversational_optimize(
            "Help me with this code", 
            "User has been asking about Python functions and seems confused about return values",
            "User preferred simple examples over complex explanations"
        )
    """
    try:
        # Extract conversation insights for training
        conversation_keywords = []
        if "confused" in conversation_history.lower():
            conversation_keywords.extend(["clear", "simple", "step-by-step"])
        if "example" in conversation_history.lower() or "example" in user_satisfaction_signals.lower():
            conversation_keywords.extend(["example", "demonstration", "practical"])
        if "technical" in conversation_history.lower():
            conversation_keywords.extend(["technical", "detailed", "specific"])
        
        # Default keywords if no specific context detected
        if not conversation_keywords:
            conversation_keywords = ["helpful", "relevant", "clear"]
        
        # Create training data based on conversation context
        training_data = [{
            "input": conversation_history or "conversation context",
            "expected_keywords": conversation_keywords[:5]  # Limit to top 5 keywords
        }]
        
        # Optimize with moderate budget for conversational context
        result = gepa.optimize_prompt(prompt, training_data, budget=7)
        
        return json.dumps({
            "success": True,
            "original_prompt": prompt,
            "context_optimized_prompt": result["optimized_prompt"],
            "conversation_insights": conversation_keywords,
            "improvement_score": result["improvement"]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Conversational optimization failed: {str(e)}"
        })