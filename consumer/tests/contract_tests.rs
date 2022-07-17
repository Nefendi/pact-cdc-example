use pact_consumer::prelude::*;
use pact_consumer::*;
use user_consumer_service::{create_user, get_users, UserIn, UserOut};
use uuid::Uuid;

#[tokio::test]
async fn provider_returns_the_list_of_users() {
    let user = UserOut {
        id: Uuid::new_v4(),
        username: "John42".to_owned(),
        name: "John".to_owned(),
        surname: "Doe".to_owned(),
        age: 42,
        job_title: None,
        phone_number: None,
    };

    let pact = PactBuilder::new("User Consumer Service", "User Provider Service")
        .output_dir("../pact_contracts")
        .interaction("a request to list all users", "", |mut i| async {
            i.given("there exists at least one user in the database");
            i.request.path("/users");
            i.response
                .content_type("application/json")
                .json_body(each_like!(strip_null_fields(serde_json::json!(user))));

            i
        })
        .await
        .start_mock_server(None);

    let mock_server_path = pact.path("/users");

    let response = get_users(mock_server_path).await.unwrap();

    assert_eq!(response, vec![user]);
}

#[tokio::test]
async fn provider_allows_to_create_a_user_and_returns_its_serialised_representation() {
    let user_in = UserIn {
        username: "John42".to_owned(),
        password: "admin123".to_owned(),
        name: "John".to_owned(),
        surname: "Doe".to_owned(),
        age: 42,
        job_title: Some("Software Developer".to_owned()),
        phone_number: Some("+48111222333".to_owned()),
    };

    let user_out = UserOut {
        id: Uuid::new_v4(),
        username: "John42".to_owned(),
        name: "John".to_owned(),
        surname: "Doe".to_owned(),
        age: 42,
        job_title: Some("Software Developer".to_owned()),
        phone_number: Some("+48111222333".to_owned()),
    };

    let pact = PactBuilder::new("User Consumer Service", "User Provider Service")
        .interaction("a request to create a user", "", |mut i| async {
            i.given("the server allows to create users");
            i.request
                .post()
                .path("/users")
                .content_type("application/json")
                .json_body(like!(serde_json::json!(user_in)));
            i.response
                .created()
                .content_type("application/json")
                .json_body(like!(strip_null_fields(serde_json::json!(user_out))));

            i
        })
        .await
        .output_dir("../pact_contracts")
        .start_mock_server(None);

    let mock_server_path = pact.path("/users");

    let response = create_user(mock_server_path, user_in).await.unwrap();

    assert_eq!(response, user_out);
}
