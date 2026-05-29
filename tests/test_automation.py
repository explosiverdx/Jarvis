"""
Tests for Automation
"""

import pytest
from jarvis.automation.task_executor import TaskExecutor
from jarvis.automation.task_scheduler import TaskScheduler


class TestTaskExecutor:
    """Test Task Executor"""
    
    @pytest.fixture
    def executor(self):
        """Create task executor for testing"""
        return TaskExecutor()
    
    def test_initialization(self, executor):
        """Test executor initialization"""
        assert executor is not None
        assert len(executor.task_handlers) > 0
    
    def test_execute_greeting(self, executor):
        """Test executing greeting task"""
        result = executor.execute("greeting", {})
        assert result is not None
        assert len(result) > 0
    
    def test_execute_get_time(self, executor):
        """Test executing get time task"""
        result = executor.execute("get_time", {})
        assert "time" in result.lower()
    
    def test_execute_get_date(self, executor):
        """Test executing get date task"""
        result = executor.execute("get_date", {})
        assert result is not None
    
    def test_execute_unknown(self, executor):
        """Test executing unknown task"""
        result = executor.execute("unknown", {})
        assert result is not None
    
    def test_register_handler(self, executor):
        """Test registering custom handler"""
        def test_handler(entities):
            return "test result"
        
        executor.register_handler("test_intent", test_handler)
        result = executor.execute("test_intent", {})
        assert result == "test result"


class TestTaskScheduler:
    """Test Task Scheduler"""
    
    @pytest.fixture
    def scheduler(self):
        """Create scheduler for testing"""
        return TaskScheduler()
    
    def test_initialization(self, scheduler):
        """Test scheduler initialization"""
        assert scheduler is not None
        assert scheduler.scheduled_tasks == {}
    
    def test_schedule_task(self, scheduler):
        """Test scheduling a task"""
        def test_task():
            pass
        
        scheduler.start()
        job_id = scheduler.schedule_task("test", test_task, "hourly")
        assert job_id is not None
        assert job_id in scheduler.scheduled_tasks
        scheduler.stop()
    
    def test_list_tasks(self, scheduler):
        """Test listing tasks"""
        tasks = scheduler.list_tasks()
        assert isinstance(tasks, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
