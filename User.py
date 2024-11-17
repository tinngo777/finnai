class User:
    def __init__(self, username="User", current_savings=1000, monthly_income=3000, estimate_monthly_expenses=2000, saving_goal=10000, current_expenses=0, saving_history=[], dialogs=[]):
        self.username = username
        self.current_savings = current_savings
        self.monthly_income = monthly_income
        self.estimated_monthly_expenses = estimate_monthly_expenses
        self.saving_goal = saving_goal
        self.current_expenses = current_expenses
        self.dialogs = dialogs
        self.saving_history = saving_history
    
    def user_data(self):
        return f"User data: username: {self.username}, current_savings: {self.current_savings}, monthly income: {self.monthly_income}, estimate monthly expenses: {self.current_expenses}, estimate monthly expenses: {self.estimated_monthly_expenses}, saving goal: {self.saving_goal}, saving history (last item is money saved last month): {self.saving_history}"
    
    def dict_data(self):
        return self.__dict__