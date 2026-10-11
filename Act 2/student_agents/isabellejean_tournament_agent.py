#!/usr/bin/env python
"""
Tournament Agent: Isabelle Sentinel
Student: Isabelle Jean
Generated: 2026-10-04 14:53:47

Evolution Details:
- Generations: 250
- Final Fitness: 146.1
- Trained against: Always Invest, Random (0.5), Random (0.3), Grim Trigger, Gradual...

Strategy: Starts cooperatively, monitors recent opponent behavior, and uses evolved thresholds to defend against undercutting.
"""

from agents import Agent, INVEST, UNDERCUT
import random


class IsabelleJeanAgent(Agent):
    """
    Isabelle Sentinel

    Starts cooperatively, monitors recent opponent behavior, and uses evolved thresholds to defend against undercutting.

    Evolved Genes: [1.0, 1.0, 1.0, 0.43373272285164033, 0.29022285100878714, 0.0]
    """

    def __init__(self):
        # These genes were evolved through 250 generations
        self.genes = [1.0, 1.0, 1.0, 0.43373272285164033, 0.29022285100878714, 0.0]

        # Required for tournament compatibility
        self.student_name = "Isabelle Jean"

        super().__init__(
            name="Isabelle Sentinel",
            description="Starts cooperatively, monitors recent opponent behavior, and uses evolved thresholds to defend against undercutting."
        )

    def choose_action(self) -> bool:
        # Use the opening gene only on the first round.
        # After that, begin responding to the opponent's behavior.
        if not self.history:
            return random.random() < self.genes[0]

        memory_length = 2 + int(self.genes[4] * 18)
        recent_history = self.history[-memory_length:]

        cooperation_rate = sum(recent_history) / len(recent_history)
        defection_rate = 1.0 - cooperation_rate

        # Evolution decides how much undercutting this agent tolerates.
        retaliation_threshold = 0.10 + 0.50 * self.genes[5]

        # Two consecutive undercuts provide an additional warning,
        # even when a longer history still looks cooperative.
        repeated_undercuts = (
            len(self.history) >= 2
            and self.history[-1] == UNDERCUT
            and self.history[-2] == UNDERCUT
        )

        defensive = (
            defection_rate >= retaliation_threshold
            or repeated_undercuts
        )

        if defensive:
            # Higher gene 2 means stronger retaliation.
            # Forgiveness depends on evidence of past cooperation.
            # Against an opponent that has never invested, this is zero.
            cooperation_probability = (
                (1.0 - self.genes[2])
                * self.genes[3]
                * cooperation_rate
            )

        elif self.history[-1] == INVEST:
            # Reciprocate when the latest action and recent history
            # both support continued cooperation.
            cooperation_probability = self.genes[1]

        else:
            # Forgive an isolated undercut according to gene 3
            # and the opponent's recent cooperation.
            cooperation_probability = (
                self.genes[3] * cooperation_rate
            )

        return random.random() < cooperation_probability



# Convenience function for tournament loading
def get_agent():
    """Return an instance of this agent for tournament use"""
    return IsabelleJeanAgent()


if __name__ == "__main__":
    # Test that the agent can be instantiated
    agent = get_agent()
    print(f"✅ Agent loaded successfully: {agent.name}")
    print(f"   Genes: {agent.genes}")
    print(f"   Description: {agent.description}")
