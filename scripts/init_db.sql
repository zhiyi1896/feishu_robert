CREATE DATABASE IF NOT EXISTS feishu_task_bot
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE feishu_task_bot;

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS employees (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT 'employee primary key',
    employee_no VARCHAR(64) NOT NULL COMMENT 'employee code',
    name VARCHAR(128) NOT NULL COMMENT 'employee name',
    feishu_open_id VARCHAR(128) DEFAULT NULL COMMENT 'feishu open id',
    feishu_user_id VARCHAR(128) DEFAULT NULL COMMENT 'feishu user id',
    job_level VARCHAR(64) DEFAULT NULL COMMENT 'job level such as P5 or M1',
    department_name VARCHAR(128) DEFAULT NULL COMMENT 'department name',
    manager_id BIGINT DEFAULT NULL COMMENT 'direct manager employee id',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'whether employee is active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'created time',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'updated time',
    PRIMARY KEY (id),
    UNIQUE KEY uk_employees_employee_no (employee_no),
    UNIQUE KEY uk_employees_feishu_open_id (feishu_open_id),
    UNIQUE KEY uk_employees_feishu_user_id (feishu_user_id),
    KEY idx_employees_manager_id (manager_id),
    KEY idx_employees_name (name),
    KEY idx_employees_department_name (department_name),
    CONSTRAINT fk_employees_manager_id
        FOREIGN KEY (manager_id) REFERENCES employees(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='employee master table';

CREATE TABLE IF NOT EXISTS projects (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT 'project primary key',
    project_code VARCHAR(64) NOT NULL COMMENT 'project code',
    project_name VARCHAR(128) NOT NULL COMMENT 'project name',
    owner_id BIGINT DEFAULT NULL COMMENT 'project owner employee id',
    status VARCHAR(32) NOT NULL DEFAULT 'active' COMMENT 'project status',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'created time',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'updated time',
    PRIMARY KEY (id),
    UNIQUE KEY uk_projects_project_code (project_code),
    KEY idx_projects_project_name (project_name),
    KEY idx_projects_owner_id (owner_id),
    CONSTRAINT fk_projects_owner_id
        FOREIGN KEY (owner_id) REFERENCES employees(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='project master table';

CREATE TABLE IF NOT EXISTS project_members (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT 'project member primary key',
    project_id BIGINT NOT NULL COMMENT 'project id',
    employee_id BIGINT NOT NULL COMMENT 'employee id',
    role_name VARCHAR(64) DEFAULT NULL COMMENT 'member role name',
    joined_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'join time',
    PRIMARY KEY (id),
    UNIQUE KEY uk_project_members_project_employee (project_id, employee_id),
    KEY idx_project_members_employee_id (employee_id),
    CONSTRAINT fk_project_members_project_id
        FOREIGN KEY (project_id) REFERENCES projects(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_project_members_employee_id
        FOREIGN KEY (employee_id) REFERENCES employees(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='project member table';

CREATE TABLE IF NOT EXISTS tasks (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT 'task primary key',
    task_no VARCHAR(64) NOT NULL COMMENT 'task number',
    title VARCHAR(255) NOT NULL COMMENT 'task title',
    content TEXT DEFAULT NULL COMMENT 'task content',
    task_type VARCHAR(64) NOT NULL DEFAULT 'daily' COMMENT 'task type',
    status VARCHAR(32) NOT NULL DEFAULT 'pending' COMMENT 'task status',
    priority VARCHAR(16) NOT NULL DEFAULT 'P2' COMMENT 'task priority',
    creator_id BIGINT NOT NULL COMMENT 'creator employee id',
    assignee_id BIGINT DEFAULT NULL COMMENT 'assignee employee id',
    project_id BIGINT DEFAULT NULL COMMENT 'project id',
    start_time DATETIME DEFAULT NULL COMMENT 'start time',
    due_time DATETIME DEFAULT NULL COMMENT 'due time',
    end_time DATETIME DEFAULT NULL COMMENT 'finish time',
    source_text TEXT DEFAULT NULL COMMENT 'raw source text from chat',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'created time',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'updated time',
    PRIMARY KEY (id),
    UNIQUE KEY uk_tasks_task_no (task_no),
    KEY idx_tasks_creator_id (creator_id),
    KEY idx_tasks_assignee_id (assignee_id),
    KEY idx_tasks_project_id (project_id),
    KEY idx_tasks_task_type (task_type),
    KEY idx_tasks_status (status),
    KEY idx_tasks_priority (priority),
    KEY idx_tasks_due_time (due_time),
    KEY idx_tasks_created_at (created_at),
    CONSTRAINT fk_tasks_creator_id
        FOREIGN KEY (creator_id) REFERENCES employees(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_tasks_assignee_id
        FOREIGN KEY (assignee_id) REFERENCES employees(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT fk_tasks_project_id
        FOREIGN KEY (project_id) REFERENCES projects(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='task master table';

CREATE TABLE IF NOT EXISTS task_logs (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT 'task log primary key',
    task_id BIGINT NOT NULL COMMENT 'task id',
    operator_id BIGINT DEFAULT NULL COMMENT 'operator employee id',
    action_type VARCHAR(64) NOT NULL COMMENT 'action type',
    action_detail TEXT DEFAULT NULL COMMENT 'action detail',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'created time',
    PRIMARY KEY (id),
    KEY idx_task_logs_task_id (task_id),
    KEY idx_task_logs_operator_id (operator_id),
    KEY idx_task_logs_action_type (action_type),
    KEY idx_task_logs_created_at (created_at),
    CONSTRAINT fk_task_logs_task_id
        FOREIGN KEY (task_id) REFERENCES tasks(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_task_logs_operator_id
        FOREIGN KEY (operator_id) REFERENCES employees(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='task log table';

CREATE TABLE IF NOT EXISTS push_configs (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT 'push config primary key',
    employee_id BIGINT NOT NULL COMMENT 'employee id',
    push_time VARCHAR(16) NOT NULL COMMENT 'push time such as 09:00',
    push_scope VARCHAR(32) NOT NULL DEFAULT 'self' COMMENT 'push scope',
    push_pending TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'include pending tasks',
    push_due_soon TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'include due soon tasks',
    push_overdue TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'include overdue tasks',
    is_enabled TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'whether push config is enabled',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'created time',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'updated time',
    PRIMARY KEY (id),
    KEY idx_push_configs_employee_id (employee_id),
    CONSTRAINT fk_push_configs_employee_id
        FOREIGN KEY (employee_id) REFERENCES employees(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='push config table';