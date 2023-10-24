from pydantic import BaseModel, Field
from src.core.org import Org


class SoftwareOrg(Org):
    pass
    # """
    # Software Company: Possesses a team, SOP (Standard Operating Procedures), and a platform for instant messaging,
    # dedicated to writing executable code.
    # """
    # environment: Environment = Field(default_factory=Environment)
    # investment: float = Field(default=10.0)
    # idea: str = Field(default="")

    # class Config:
    #     arbitrary_types_allowed = True

    # def hire(self, roles: list[Role]):
    #     """Hire roles to cooperate"""
    #     self.environment.add_roles(roles)

    # def invest(self, investment: float):
    #     """Invest company. raise NoMoneyException when exceed max_budget."""
    #     self.investment = investment
    #     CONFIG.max_budget = investment
    #     logger.info(f'Investment: ${investment}.')

    # def _check_balance(self):
    #     if CONFIG.total_cost > CONFIG.max_budget:
    #         raise NoMoneyException(CONFIG.total_cost, f'Insufficient funds: {CONFIG.max_budget}')

    # def start_project(self, idea):
    #     """Start a project from publishing boss requirement."""
    #     self.idea = idea
    #     self.environment.publish_message(Message(role="BOSS", content=idea, cause_by=BossRequirement))

    # def _save(self):
    #     logger.info(self.json())

    # async def run(self, n_round=3):
    #     """Run company until target round or no money"""
    #     while n_round > 0:
    #         # self._save()
    #         n_round -= 1
    #         logger.debug(f"{n_round=}")
    #         self._check_balance()
    #         await self.environment.run()
    #     return self.environment.history
