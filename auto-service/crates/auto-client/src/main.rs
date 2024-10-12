use ip_service::ip_client::Client;
use std::sync::Arc;
use tokio::sync::Mutex;

const IP: &str = "192.168.99.3";
const PORT: &str = "10086";

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
    let client = create_client(IP.to_string(), PORT.to_string()).await;
    let handle = ip_service::ip_common::monitor_ip::<String>(client.clone()).await;
    let _ = tokio::join!(handle);
}
