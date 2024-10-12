use std::sync::Arc;
use tokio::sync::Mutex;

use ip_service::ip_client::Client;

mod flags;

fn main() {
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .worker_threads(2)
        .max_blocking_threads(2)
        .build()
        .expect("build tokio runtime error!");
    runtime.block_on(async_main());
}

async fn create_client(server_ip: String, port: String) -> Arc<Mutex<Client>> {
    Arc::new(Mutex::new(
        Client::new(server_ip.to_string(), port.to_string()).await,
    ))
}

async fn async_main() {
    let client = create_client(flags::IP.to_string(), flags::PORT.to_string()).await;
    let handle = ip_service::ip_common::monitor_ip(client.clone()).await;
    let _ = tokio::join!(handle);
}
