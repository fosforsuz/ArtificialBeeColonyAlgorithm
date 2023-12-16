import random
import numpy as np
import pandas as pd

lessons = {
    "Mühendislik Etiği": "2",
    "Bilgisayar Mühendisliğine Giriş": "4",
    "Programlama Dilleri Temelleri": "4",
    "Ayrık Matematik": "5",
    "Kablosuz Algılayıcı Ağlar": "3",
    "Web Programlama": "3",
    "İşletim Sistemleri": "5",
    "Algortima Analizi": "5",
    "Mikroişlemciler": "5",
    "Bitirme Projesi": "5",
    "Sensörler Ağları": "3",
    "Fizik": "5",
    "AIIT": "3",
    "Türk Dili": "3",
    "Diferansiyel Denklemler": "5",
    "Nesne Tabanlı Programlama": "5",
    "Doğal Dil İşleme": "3",
    "Parallel Programlama": "3",
    "E-Ticaret": "3",
    "Nesnelerin İnterneti": "3",
    "Yapa Zeka": "5",
    "Matematik": "5",
    "Kariyer Planlama": "1",
    "Mesleki İngilizce": "3",
    "Nano Teknoloji": "3",
    "Veri Madenciliği": "5",
    "Kimya": "5",
    "Yabancı Dil": "3",
    "Elektrik Devreleri": "5",
    "Bilgisayar Mimarisi": "5",
    "Tasarım Desenleri": "5",
    "Yapay Sinir Ağları": "3",
    "Bulanık Mantık": "3",
    "Veri Yapıları": "5",
}

classes = [
    "123",
    "326",
    "227",
    "327",
]

days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
hours = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "15:00"]

days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
hours = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

class CourseScheduler:
    def __init__(self, lessons, classes, days, hours):
        self.lessons = lessons
        self.classes = classes
        self.days = days
        self.hours = hours
        self.num_classes = len(classes)
        self.num_days = len(days)
        self.num_hours = len(hours)
        self.pheromone = {
            cls: pd.DataFrame(np.ones((len(days), len(hours))), index=days, columns=hours)
            for cls in classes
        }
        self.schedule = {}
    
    def generate_schedule(self, iterations=100):
        for i in range(iterations):
            new_schedule = self._construct_schedule()
            if self._evaluate_schedule(new_schedule) > self._evaluate_schedule(self.schedule):
                self.schedule = new_schedule
            self._update_pheromones()
        return self.schedule
    
    def _construct_schedule(self):
        schedule = {}
        for lesson, hours_needed in self.lessons.items():
            for _ in range(int(hours_needed)):
                placed = False
                while not placed:
                    selected_class = random.choice(self.classes)
                    selected_day = random.choice(self.days)
                    selected_hour = random.choice(self.hours)
                    if schedule.get((selected_class, selected_day, selected_hour)) is None:
                        schedule[lesson] = (selected_class, selected_day, selected_hour)
                        placed = True
        return schedule
    
    def _evaluate_schedule(self, schedule):
        score = 0
        for lesson, schedule_info in schedule.items():
            selected_class, selected_day, selected_hour = schedule_info
            score += self.pheromone[selected_class].loc[selected_day, selected_hour]
        return score
    
    def _update_pheromones(self):
        evaporation_rate = 0.5
        for cls in self.classes:
            self.pheromone[cls] *= evaporation_rate

# Ders programını oluştur
scheduler = CourseScheduler(lessons, classes, days, hours)
schedule = scheduler.generate_schedule(iterations=1000)

# Excel'e yazdır
df = pd.DataFrame(columns=days, index=hours)

for lesson, (selected_class, selected_day, selected_hour) in schedule.items():
    df.loc[selected_hour, selected_day] = f"{lesson}\n{selected_class}"

df.to_excel('ders_programı.xlsx')
print("Ders programı başarıyla 'ders_programı.xlsx' dosyasına kaydedildi.")
