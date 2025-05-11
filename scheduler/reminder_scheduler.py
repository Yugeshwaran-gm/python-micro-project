from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.mail_utils import EmailSender
from datetime import datetime, timedelta

class ReminderScheduler:
    def __init__(self, app):
        self.app = app
        self.scheduler = BackgroundScheduler()
        self.email_sender = EmailSender(app.config)
        
    def send_daily_timetable(self):
        """Send complete timetable to all students at 8 AM"""
        with self.app.app_context():
            students = self.app.mongodb.db.students.find()
            timetables = list(self.app.mongodb.db.timetables.find())
            
            for student in students:
                message = self.create_daily_timetable_message(student, timetables)
                self.email_sender.send_email(
                    student['email'],
                    "Daily Timetable",
                    message
                )
    
    def send_period_reminders(self):
        """Send reminders 5 minutes before each period"""
        with self.app.app_context():
            current_time = datetime.now()
            # Get the current time slot
            current_hour = current_time.hour
            current_minute = current_time.minute
            
            # Find the next period
            timetables = list(self.app.mongodb.db.timetables.find())
            students = list(self.app.mongodb.db.students.find())
            
            for timetable in timetables:
                period_time = datetime.strptime(timetable['time'], '%H:%M').time()
                # Calculate time difference
                time_diff = datetime.combine(current_time.date(), period_time) - current_time
                
                # If the period is in the next 5 minutes
                if timedelta(minutes=0) <= time_diff <= timedelta(minutes=5):
                    for student in students:
                        message = self.create_period_reminder_message(
                            student, 
                            timetable,
                            period_time
                        )
                        self.email_sender.send_email(
                            student['email'],
                            f"Reminder: {timetable['time']} Period",
                            message
                        )
    
    def create_daily_timetable_message(self, student, timetables):
        """Create HTML message for daily timetable"""
        message = f"""
        <html>
            <body>
                <h2>Daily Timetable</h2>
                <p>Hello {student['name']},</p>
                <p>Here is your timetable for today:</p>
                <table border="1" style="border-collapse: collapse; width: 100%;">
                    <tr>
                        <th style="padding: 8px;">Time</th>
                        <th style="padding: 8px;">Monday</th>
                        <th style="padding: 8px;">Tuesday</th>
                        <th style="padding: 8px;">Wednesday</th>
                        <th style="padding: 8px;">Thursday</th>
                        <th style="padding: 8px;">Friday</th>
                    </tr>
        """
        
        for timetable in timetables:
            message += f"""
                    <tr>
                        <td style="padding: 8px;">{timetable['time']}</td>
                        <td style="padding: 8px;">{timetable['monday']}</td>
                        <td style="padding: 8px;">{timetable['tuesday']}</td>
                        <td style="padding: 8px;">{timetable['wednesday']}</td>
                        <td style="padding: 8px;">{timetable['thursday']}</td>
                        <td style="padding: 8px;">{timetable['friday']}</td>
                    </tr>
            """
        
        message += """
                </table>
                <p>Best regards,<br>Timetable System</p>
            </body>
        </html>
        """
        return message
    
    def create_period_reminder_message(self, student, timetable, period_time):
        """Create HTML message for period reminder"""
        # Get the current day of the week (0 = Monday, 6 = Sunday)
        current_day = datetime.now().weekday()
        day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        
        if current_day < 5:  # Only send reminders on weekdays
            current_day_name = day_names[current_day]
            subject = timetable[current_day_name]
            
            message = f"""
            <html>
                <body>
                    <h2>Period Reminder</h2>
                    <p>Hello {student['name']},</p>
                    <p>Your next period is starting in 5 minutes:</p>
                    <p><strong>Time:</strong> {timetable['time']}</p>
                    <p><strong>Subject:</strong> {subject}</p>
                    <p>Please make sure you're prepared for the class.</p>
                    <p>Best regards,<br>Timetable System</p>
                </body>
            </html>
            """
            return message
        return None
    
    def start(self):
        # Schedule daily timetable at 8 AM
        self.scheduler.add_job(
            func=self.send_daily_timetable,
            trigger=CronTrigger(hour=8, minute=0),
            id='daily_timetable',
            name='Send daily timetable',
            replace_existing=True
        )
        
        # Schedule period reminders every minute
        self.scheduler.add_job(
            func=self.send_period_reminders,
            trigger=CronTrigger(minute='*'),  # Run every minute
            id='period_reminders',
            name='Send period reminders',
            replace_existing=True
        )
        
        self.scheduler.start()
