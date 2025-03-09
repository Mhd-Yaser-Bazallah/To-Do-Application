import pytest
from unittest.mock import Mock, patch
from To_Do.task.service import TaskService   
from To_Do.task.Dtos.create_task_dto import TaskCreate
from To_Do.task.Dtos.update_task_dto import TaskUpdate
from To_Do.task.models import Task
from To_Do.user.models import User   
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from To_Do.base import Base

 
engine = create_engine('sqlite:///:memory:') 
TestingSessionLocal = sessionmaker(bind=engine)

 
Base.metadata.create_all(engine)

# Test fixtures
@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def mock_task_repo(mock_db):
    return Mock()

@pytest.fixture
def task_service(mock_db, mock_task_repo):
    with patch('To_Do.task.service.TaskRepository', return_value=mock_task_repo):
        with patch('To_Do.task.service.get_db_instance', return_value=mock_db):
            return TaskService()

@pytest.fixture
def sample_user(): 
    user = User(id=1, name="Test User")
    return user

@pytest.fixture
def sample_task_create(sample_user): 
    return TaskCreate(
        title="Test Task",
        description="Test Description",
        owner_id=sample_user.id
    )

@pytest.fixture
def sample_task_update():
    return TaskUpdate(
        title="Updated Task",
        description="Updated Description",
        completion_status=True
    )

@pytest.fixture
def sample_task(sample_user):
    # Create a simple Task object with the sample user as the owner
    return Task(
        id=1,
        title="Test Task",
        description="Test Description",
        owner_id=sample_user.id,
        completion_status=False
    )

# Tests
def test_task_service_init(task_service, mock_db, mock_task_repo):
    assert task_service.db == mock_db
    assert task_service.task_repo == mock_task_repo

def test_create_task(task_service, mock_task_repo, sample_task_create, sample_task):
    mock_task_repo.create_task.return_value = sample_task
    result = task_service.create_task(sample_task_create)
    
    mock_task_repo.create_task.assert_called_once_with(sample_task_create)
    assert result == sample_task

def test_get_task(task_service, mock_task_repo, sample_task):
    mock_task_repo.get_task.return_value = sample_task
    result = task_service.get_task(1)
    
    mock_task_repo.get_task.assert_called_once_with(1)
    assert result == sample_task

def test_get_task_by_user_id(task_service, mock_task_repo, sample_task):
    mock_task_repo.get_tasks_by_user_id.return_value = [sample_task]
    result = task_service.get_task_by_user_id(1)
    
    mock_task_repo.get_tasks_by_user_id.assert_called_once_with(1)
    assert result == [sample_task]

def test_get_tasks(task_service, mock_task_repo, sample_task):
    mock_task_repo.get_tasks.return_value = [sample_task]
    result = task_service.get_tasks(skip=0, limit=100)
    
    mock_task_repo.get_tasks.assert_called_once_with(0, 100)
    assert result == [sample_task]

def test_update_task_success(task_service, mock_task_repo, sample_task_update, sample_task):
    mock_task_repo.update_task.return_value = sample_task
    result = task_service.update_task(1, sample_task_update)
    
    mock_task_repo.update_task.assert_called_once_with(1, sample_task_update)
    assert result == sample_task

def test_update_task_not_found(task_service, mock_task_repo, sample_task_update):
    mock_task_repo.update_task.side_effect = HTTPException(status_code=404, detail="Task not found")
    with pytest.raises(HTTPException) as exc:
        task_service.update_task(1, sample_task_update)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Task not found"

def test_delete_task_success(task_service, mock_task_repo, sample_task):
    mock_task_repo.delete_task.return_value = sample_task
    result = task_service.delete_task(1)
    
    mock_task_repo.delete_task.assert_called_once_with(1)
    assert result == sample_task

def test_delete_task_not_found(task_service, mock_task_repo):
    mock_task_repo.delete_task.return_value = None
    result = task_service.delete_task(999)
    
    mock_task_repo.delete_task.assert_called_once_with(999)
    assert result is None

def test_get_tasks_with_custom_pagination(task_service, mock_task_repo, sample_task):
    mock_task_repo.get_tasks.return_value = [sample_task]
    result = task_service.get_tasks(skip=5, limit=10)
    
    mock_task_repo.get_tasks.assert_called_once_with(5, 10)
    assert result == [sample_task]
