
-- 1. Actors
CREATE TABLE IF NOT EXISTS actors (
    id BIGINT PRIMARY KEY,                          
    login VARCHAR(255) NOT NULL,                  
    gravatar_id VARCHAR(100),                       
    url VARCHAR(500),                              
    avatar_url VARCHAR(500),                        
    INDEX idx_actor_login (login)                   
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Repositories
CREATE TABLE IF NOT EXISTS repositories (
    id BIGINT PRIMARY KEY,                           
    name VARCHAR(255) NOT NULL,                     
    url VARCHAR(500),                              
    INDEX idx_repo_name (name)                     
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Organizations 
CREATE TABLE IF NOT EXISTS organizations (
    id BIGINT PRIMARY KEY,                          
    login VARCHAR(255) NOT NULL,                    
    gravatar_id VARCHAR(100),
    url VARCHAR(500),
    avatar_url VARCHAR(500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. GitHub Events Table
CREATE TABLE IF NOT EXISTS github_events (
    id BIGINT PRIMARY KEY,                          
    type VARCHAR(50) NOT NULL,                       
    actor_id BIGINT NOT NULL,                        
    repo_id BIGINT NOT NULL,                         
    org_id BIGINT NULL,                            
    is_public BOOLEAN DEFAULT TRUE,                  
    payload JSON NOT NULL,                           
    created_at DATETIME NOT NULL,                   

    -- Foreign Keys
    CONSTRAINT fk_events_actor FOREIGN KEY (actor_id) REFERENCES actors(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_events_repo FOREIGN KEY (repo_id) REFERENCES repositories(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_events_org FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_events_type ON github_events(type);
CREATE INDEX idx_events_created_at ON github_events(created_at);