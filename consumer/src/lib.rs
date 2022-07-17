use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Deserialize, Serialize, PartialEq, Debug)]
pub struct UserIn {
    pub username: String,
    pub name: String,
    pub surname: String,
    pub password: String,
    pub age: i32,
    pub job_title: Option<String>,
    pub phone_number: Option<String>,
}

#[derive(Deserialize, Serialize, PartialEq, Debug)]
pub struct UserOut {
    pub id: Uuid,
    pub username: String,
    pub name: String,
    pub surname: String,
    pub age: i32,
    pub job_title: Option<String>,
    pub phone_number: Option<String>,
}

#[allow(dead_code)]
pub async fn get_users(url: reqwest::Url) -> Result<Vec<UserOut>, Box<dyn std::error::Error>> {
    Ok(reqwest::get(url).await?.json().await?)
}

#[allow(dead_code)]
pub async fn create_user(
    url: reqwest::Url,
    user: UserIn,
) -> Result<UserOut, Box<dyn std::error::Error>> {
    Ok(reqwest::Client::new()
        .post(url)
        .json(&serde_json::json!(user))
        .send()
        .await?
        .json()
        .await?)
}
