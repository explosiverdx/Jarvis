"""
Task Scheduler
Schedule and manage recurring tasks
"""

from loguru import logger
from typing import Callable, Dict, Any
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz


class TaskScheduler:
    """Schedule and manage automated tasks"""
    
    def __init__(self, config=None):
        """
        Initialize task scheduler
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.scheduler = BackgroundScheduler()
        self.scheduled_tasks = {}
        logger.info("TaskScheduler initialized")
    
    def start(self):
        """Start the scheduler"""
        try:
            if not self.scheduler.running:
                self.scheduler.start()
                logger.info("TaskScheduler started")
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
    
    def stop(self):
        """Stop the scheduler"""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                logger.info("TaskScheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")
    
    def schedule_task(self, task_name: str, handler: Callable, 
                     schedule_type: str, **kwargs) -> str:
        """
        Schedule a task
        
        Args:
            task_name: Name of the task
            handler: Function to execute
            schedule_type: Type of schedule ('once', 'hourly', 'daily', 'weekly', 'custom')
            **kwargs: Additional parameters depending on schedule type
        
        Returns:
            Job ID
        """
        try:
            job_id = f"task_{task_name}_{len(self.scheduled_tasks)}"
            
            if schedule_type == "once":
                run_date = kwargs.get("run_date")
                job = self.scheduler.add_job(handler, "date", run_date=run_date, id=job_id)
            
            elif schedule_type == "hourly":
                job = self.scheduler.add_job(handler, "interval", hours=1, id=job_id)
            
            elif schedule_type == "daily":
                hour = kwargs.get("hour", 9)
                minute = kwargs.get("minute", 0)
                job = self.scheduler.add_job(
                    handler, "cron", hour=hour, minute=minute, id=job_id
                )
            
            elif schedule_type == "weekly":
                day_of_week = kwargs.get("day_of_week", "mon")
                hour = kwargs.get("hour", 9)
                minute = kwargs.get("minute", 0)
                job = self.scheduler.add_job(
                    handler, "cron", day_of_week=day_of_week,
                    hour=hour, minute=minute, id=job_id
                )
            
            elif schedule_type == "custom":
                cron_expression = kwargs.get("cron_expression")
                job = self.scheduler.add_job(
                    handler, CronTrigger.from_crontab(cron_expression), id=job_id
                )
            
            else:
                raise ValueError(f"Unknown schedule type: {schedule_type}")
            
            self.scheduled_tasks[job_id] = {
                "name": task_name,
                "handler": handler,
                "schedule_type": schedule_type,
                "job": job
            }
            
            logger.info(f"Task scheduled: {task_name} (ID: {job_id})")
            return job_id
            
        except Exception as e:
            logger.error(f"Error scheduling task: {e}")
            raise
    
    def cancel_task(self, job_id: str) -> bool:
        """
        Cancel a scheduled task
        
        Args:
            job_id: ID of the job to cancel
        
        Returns:
            True if cancelled, False otherwise
        """
        try:
            if job_id in self.scheduled_tasks:
                self.scheduler.remove_job(job_id)
                del self.scheduled_tasks[job_id]
                logger.info(f"Task cancelled: {job_id}")
                return True
            else:
                logger.warning(f"Task not found: {job_id}")
                return False
        except Exception as e:
            logger.error(f"Error cancelling task: {e}")
            return False
    
    def list_tasks(self) -> Dict[str, Any]:
        """
        Get list of scheduled tasks
        
        Returns:
            Dictionary of scheduled tasks
        """
        return self.scheduled_tasks
    
    def get_task(self, job_id: str) -> Dict[str, Any]:
        """
        Get details of a scheduled task
        
        Args:
            job_id: ID of the task
        
        Returns:
            Task details or None
        """
        return self.scheduled_tasks.get(job_id)
    
    def reschedule_task(self, job_id: str, **kwargs) -> bool:
        """
        Reschedule an existing task
        
        Args:
            job_id: ID of the task
            **kwargs: New schedule parameters
        
        Returns:
            True if rescheduled, False otherwise
        """
        try:
            if job_id in self.scheduled_tasks:
                job = self.scheduled_tasks[job_id]["job"]
                job.reschedule(**kwargs)
                logger.info(f"Task rescheduled: {job_id}")
                return True
            else:
                logger.warning(f"Task not found: {job_id}")
                return False
        except Exception as e:
            logger.error(f"Error rescheduling task: {e}")
            return False
