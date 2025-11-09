class Customer:
    """Класс для хранения данных пользователя"""
    
    def __init__(self):
        self.platform = ""
        self.user_step = {}
        self.login = ""
        self.password = ""
        self.order_des = {
            "version": "не задано",
            "amount": "не задано",
            "levels": "не задано",
            "unlocks": "не задано"
        }
        self.app_list = []
        self.type_of_soft = ""
        self.clicker = None
        self.is_changing_data = False
    
    def reset(self):
        """Сбросить все данные пользователя"""
        self.__init__()
    
    def set_step(self, step: str):
        """Установить текущий шаг"""
        self.user_step = {"step": step}
    
    def get_step(self) -> str:
        """Получить текущий шаг"""
        return self.user_step.get("step", "")
    
    def get_order_summary(self) -> str:
        """Получить сводку заказа"""
        summary = "Вы выбрали:\n"
        for key, value in self.order_des.items():
            summary += f"{key}: {value}\n"
        return summary
