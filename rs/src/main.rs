use std::env;

use dotenv::dotenv;
use futures::future::join_all;
use std::sync::Arc;
use ticks::projects::{Project, ProjectID};
use ticks::tasks::Task;
use ticks::{AccessToken, TickTick, TickTickError};

enum Actionability {
    Empty,
    Actionable,
    NotActionable,
}
fn is_task_actionable(task: &Task) -> bool {
    let actionable_tags: Vec<String> = task
        .tags
        .iter()
        .map(|t| t.to_string())
        .filter(|t| t.to_string() == "next".to_string())
        .collect();
    // actionable_tags
    actionable_tags.len() != 0
}
async fn read_actionable(project: &Project) -> Result<Actionability, TickTickError> {
    let tasks = Project::get_tasks(project).await.unwrap();
    if tasks.len() == 0 {
        return Ok(Actionability::Empty);
    }

    let any_actionable: bool = tasks.iter().any(|t| is_task_actionable(t));
    if any_actionable {
        Ok(Actionability::Actionable)
    } else {
        Ok(Actionability::NotActionable)
    }
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
    print!("Found {} projects", projects.len());
    let filter_futures = projects.into_iter().map(|p| async move {
        match read_actionable(&p).await {
            Ok(Actionability::Empty) => None,
            Ok(Actionability::NotActionable) => Some(p),
            Ok(Actionability::Actionable) => None,
            Err(_) => {
                eprintln!("Failed to access project {}", p.name);
                None
            }
        }
    });

    let filtered_projects: Vec<Project> = join_all(filter_futures)
        .await
        .into_iter()
        .filter_map(|p| p)
        .collect();
    println!(" of which {} are not actionable", &filtered_projects.len());
    for project in &filtered_projects {
        println!(" - {}", project.name);
    }

    if filtered_projects.len() == 0 {
        println!("Nothing to do");
        return Ok(());
    }

    println!("Assigning actionability");
    let app_arc = Arc::new(app);

    let actions_futures: Vec<_> = filtered_projects
        .into_iter()
        .map(|p| {
            let app_clone = Arc::clone(&app_arc);
            async move {
                let tags = vec!["next".to_string()];
                let title: String = "Set #next action for: ".to_string() + &p.name;
                let new_task = Task::builder(&app_clone, &title)
                    .project_id(p.get_id())
                    .tags(tags);
                new_task.build_and_publish().await.unwrap();
            }
        })
        .collect();
    join_all(actions_futures).await;

    Ok(())
}
