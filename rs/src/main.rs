use std::env;

use dotenv::dotenv;
use futures::future::join_all;
use ticks::projects::Project;
use ticks::tasks::Task;
use ticks::{AccessToken, TickTick, TickTickError};

async fn is_actionable(project: &Project) -> Result<bool, TickTickError> {
    Ok(true)
}

#[tokio::main]
async fn main() -> Result<(), ()> {
    println!("Collecting environment");
    dotenv().ok();
    let key: String = env::var("API_KEY").unwrap();
    // println!("{}", key);
    let token: AccessToken = AccessToken {
        expires_in: 100,
        value: key,
        token_type: "bearer".to_string(),
        scope: "tasks:read tasks:write".to_string(),
    };
    let app = TickTick::new(token).unwrap();

    println!("Collecting projects");
    let projects = Project::get_all(&app).await.unwrap();
    println!("Found {} projects", projects.len());
    let filter_futures = projects.iter().map(|p| async move {
        match is_actionable(p).await {
            Ok(true) => Some(p),
            Ok(false) => None,
            Err(_) => {
                eprintln!("Failed to access project {}", p.name);
                None
            }
        }
    });

    let filtered_projects: Vec<&Project> = join_all(filter_futures)
        .await
        .into_iter()
        .filter_map(|p| p)
        .collect();
    for project in filtered_projects {
        println!("{}", project.name);
    }

    Ok(())
}
